# django imports
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from lfs.catalog.models import Category, Product, Property, ProductsPropertiesRelation, PropertyOption, ProductPropertyValue
from lfs.catalog.settings import PRODUCT_WITH_VARIANTS, PROPERTY_SELECT_FIELD, VARIANT, PROPERTY_VALUE_TYPE_VARIANT


class ManageTestCase(TestCase):
    """Tests manage interface
    """
    fixtures = ['lfs_shop.xml']

    def setUp(self):
        for i in range(1, 4):
            cat, created = Category.objects.get_or_create(pk=i, name="cat" + str(i), slug="cat" + str(i), position=10,
                                                          parent=None)

        self.username = 'joe'
        self.password = 'bloggs'
        self.email = 'joe@example.com'

        new_user = User(username=self.username, email=self.email, is_active=True, is_superuser=True)
        new_user.set_password(self.password)
        new_user.save()

    # def test_category_sorting(self):
    #     """
    #     Test we get correct sorting of categories from json api
    #     """
    #
    #     self.assertEqual(3, Category.objects.count())
    #     csv = CategorySortView()
    #
    #     js = 'category[3]=root&category[1]=root&category[2]=1'
    #     csv.sort_categories(js)
    #     cat1 = Category.objects.get(pk=1)
    #     cat2 = Category.objects.get(pk=2)
    #     cat3 = Category.objects.get(pk=3)
    #
    #     # check positions are correct
    #     self.assertEqual(cat1.position, 20)
    #     self.assertEqual(cat2.position, 30)
    #     self.assertEqual(cat3.position, 10)
    #
    #     # check parents are correct
    #     self.assertEqual(cat1.parent, None)
    #     self.assertEqual(cat2.parent, cat1)
    #     self.assertEqual(cat3.parent, None)
    #
    #     js = 'category[1]=root&category[2]=root&category[3]=2'
    #     csv.sort_categories(js)
    #     cat1 = Category.objects.get(pk=1)
    #     cat2 = Category.objects.get(pk=2)
    #     cat3 = Category.objects.get(pk=3)
    #
    #     # check positions are correct
    #     self.assertEqual(cat1.position, 10)
    #     self.assertEqual(cat2.position, 20)
    #     self.assertEqual(cat3.position, 30)
    #
    #     # check parents are correct
    #     self.assertEqual(cat1.parent, None)
    #     self.assertEqual(cat2.parent, None)
    #     self.assertEqual(cat3.parent, cat2)

    def test_add_product(self):
        logged_in = self.client.login(username=self.username, password=self.password)
        products_count = Product.objects.count()
        url = reverse('lfs_manage_add_product')
        response = self.client.post(url, {'name': 'Product name', 'slug': 'productslug'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(products_count + 1, Product.objects.count())

    def test_change_product_subtype(self):
        p = Product.objects.create(name='Product1', slug='product1')

        logged_in = self.client.login(username=self.username, password=self.password)
        url = reverse('lfs_change_product_subtype', kwargs={'product_id': p.pk})
        response = self.client.post(url, {'sub_type': PRODUCT_WITH_VARIANTS}, follow=True)
        self.assertEqual(response.status_code, 200)
        p = Product.objects.get(pk=p.pk)
        self.assertEqual(p.sub_type, PRODUCT_WITH_VARIANTS)

    def test_manage_add_property(self):
        p = Product.objects.create(name='Product1', slug='product1', sub_type=PRODUCT_WITH_VARIANTS)
        logged_in = self.client.login(username=self.username, password=self.password)
        url = reverse('lfs_manage_add_property', kwargs={'product_id': p.pk})
        response = self.client.post(url, {'name': 'testproperty'}, follow=True)
        self.assertEqual(response.status_code, 200)
        new_property = Property.objects.latest('id')
        self.assertEqual(new_property.name, 'testproperty')
        self.assertTrue(new_property.local)
        self.assertTrue(ProductsPropertiesRelation.objects.filter(product=p, property=new_property).exists())

    def test_manage_add_property_option(self):
        product = Product.objects.create(name='Product1', slug='product1', sub_type=PRODUCT_WITH_VARIANTS)
        pproperty = Property.objects.create(name='property 1', type=PROPERTY_SELECT_FIELD, local=True, filterable=False)
        product_property = ProductsPropertiesRelation.objects.create(product=product, property=pproperty, position=10)

        self.client.login(username=self.username, password=self.password)
        url = reverse('lfs_manage_add_property_option', kwargs={'product_id': product.pk})
        response = self.client.post(url, {'name': 'testpropertyoption', 'property_id': pproperty.pk}, follow=True)
        self.assertEqual(response.status_code, 200)
        new_property_option = PropertyOption.objects.latest('id')
        self.assertEqual(new_property_option.name, 'testpropertyoption')

    def test_manage_variants(self):
        product = Product.objects.create(name='Product1', slug='product1', sub_type=PRODUCT_WITH_VARIANTS)
        pproperty = Property.objects.create(name='property1', type=PROPERTY_SELECT_FIELD, local=True, filterable=False)
        product_property = ProductsPropertiesRelation.objects.create(product=product, property=pproperty, position=10)
        property_option = PropertyOption.objects.create(name='property option 1', property=pproperty, position=10)

        variant = Product.objects.create(name='variant', slug='vslug', parent=product, variant_position=10,
                                         sub_type=VARIANT)
        ppv = ProductPropertyValue.objects.create(product=variant, property_id=pproperty.pk,
                                                  value=property_option.pk, type=PROPERTY_VALUE_TYPE_VARIANT)

        self.client.login(username=self.username, password=self.password)
        url = reverse('lfs_manage_variants', kwargs={'product_id': product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        outvariants = response.context['variants']
        self.assertEqual(len(outvariants), 1)
        self.assertEqual(len(outvariants[0]['properties']), 1)
        self.assertEqual(outvariants[0]['properties'][0]['name'], pproperty.name)
        self.assertEqual(outvariants[0]['properties'][0]['options'][0]['name'], property_option.name)