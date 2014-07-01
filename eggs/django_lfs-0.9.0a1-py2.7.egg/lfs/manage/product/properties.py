# django imports
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

# lfs imports
from lfs.caching import update_product_cache
from lfs.catalog.models import Product
from lfs.catalog.models import ProductPropertyValue, PropertyOption
from lfs.catalog.models import Property
from lfs.catalog.models import PropertyGroup
from lfs.catalog.settings import PROPERTY_NUMBER_FIELD, PROPERTY_VALUE_TYPE_VARIANT
from lfs.catalog.settings import PROPERTY_TEXT_FIELD
from lfs.catalog.settings import PROPERTY_SELECT_FIELD
from lfs.catalog.settings import PROPERTY_VALUE_TYPE_DEFAULT
from lfs.catalog.settings import PROPERTY_VALUE_TYPE_FILTER
from lfs.catalog.settings import PROPERTY_VALUE_TYPE_DISPLAY
from lfs.core.signals import product_removed_property_group


@permission_required("core.manage_shop")
def manage_properties(request, product_id, template_name="manage/product/properties.html"):
    """Displays the UI for manage the properties for the product with passed
    product_id.
    """
    product = get_object_or_404(Product, pk=product_id)

    # Generate lists of properties. For entering values.
    display_configurables = False
    display_filterables = False
    display_displayables = False
    configurables = []
    filterables = []
    displayables = []
    product_variant_properties = []

    # Configurable
    if not product.is_product_with_variants():
        for property_group in product.property_groups.all():
            properties = []
            for prop in property_group.properties.filter(configurable=True).order_by("groupspropertiesrelation"):
                display_configurables = True

                try:
                    ppv = ProductPropertyValue.objects.get(property=prop, product=product,
                                                           type=PROPERTY_VALUE_TYPE_DEFAULT)
                except ProductPropertyValue.DoesNotExist:
                    ppv_id = None
                    ppv_value = ""
                else:
                    ppv_id = ppv.id
                    ppv_value = ppv.value

                # Mark selected options
                options = []
                for option in prop.options.all():
                    if str(option.id) == ppv_value:
                        selected = True
                    else:
                        selected = False

                    options.append({
                        "id": option.id,
                        "name": option.name,
                        "selected": selected,
                    })

                properties.append({
                    "id": prop.id,
                    "name": prop.name,
                    "title": prop.title,
                    "type": prop.type,
                    "options": options,
                    "display_number_field": prop.type == PROPERTY_NUMBER_FIELD,
                    "display_text_field": prop.type == PROPERTY_TEXT_FIELD,
                    "display_select_field": prop.type == PROPERTY_SELECT_FIELD,
                    "value": ppv_value,
                })

            if properties:
                configurables.append({
                    "id": property_group.id,
                    "name": property_group.name,
                    "properties": properties,
                })

        # Filterable
        for property_group in product.property_groups.all():
            properties = []
            for prop in property_group.properties.filter(filterable=True).order_by("groupspropertiesrelation"):

                display_filterables = True

                # Try to get the value, if it already exists.
                ppvs = ProductPropertyValue.objects.filter(property=prop, product=product,
                                                           type=PROPERTY_VALUE_TYPE_FILTER)
                value_ids = [ppv.value for ppv in ppvs]

                # Mark selected options
                options = []
                for option in prop.options.all():

                    if str(option.id) in value_ids:
                        selected = True
                    else:
                        selected = False

                    options.append({
                        "id": option.id,
                        "name": option.name,
                        "selected": selected,
                    })

                value = ""
                if prop.type == PROPERTY_SELECT_FIELD:
                    display_select_field = True
                else:
                    display_select_field = False
                    try:
                        value = value_ids[0]
                    except IndexError:
                        pass

                properties.append({
                    "id": prop.id,
                    "name": prop.name,
                    "title": prop.title,
                    "type": prop.type,
                    "options": options,
                    "value": value,
                    "display_on_product": prop.display_on_product,
                    "display_number_field": prop.type == PROPERTY_NUMBER_FIELD,
                    "display_text_field": prop.type == PROPERTY_TEXT_FIELD,
                    "display_select_field": display_select_field,
                })
            if properties:
                filterables.append({
                    "id": property_group.id,
                    "name": property_group.name,
                    "properties": properties,
                })

        # Displayable
        for property_group in product.property_groups.all():
            properties = []
            for prop in property_group.properties.filter(display_on_product=True).order_by("groupspropertiesrelation"):

                display_displayables = True

                # Try to get the value, if it already exists.
                ppvs = ProductPropertyValue.objects.filter(property=prop, product=product,
                                                           type=PROPERTY_VALUE_TYPE_DISPLAY)
                value_ids = [ppv.value for ppv in ppvs]

                # Mark selected options
                options = []
                for option in prop.options.all():

                    if str(option.id) in value_ids:
                        selected = True
                    else:
                        selected = False

                    options.append({
                        "id": option.id,
                        "name": option.name,
                        "selected": selected,
                    })

                value = ""
                if prop.type == PROPERTY_SELECT_FIELD:
                    display_select_field = True
                else:
                    display_select_field = False
                    try:
                        value = value_ids[0]
                    except IndexError:
                        pass

                properties.append({
                    "id": prop.id,
                    "name": prop.name,
                    "title": prop.title,
                    "type": prop.type,
                    "options": options,
                    "value": value,
                    "filterable": prop.filterable,
                    "display_number_field": prop.type == PROPERTY_NUMBER_FIELD,
                    "display_text_field": prop.type == PROPERTY_TEXT_FIELD,
                    "display_select_field": display_select_field,
                })

            if properties:
                displayables.append({
                    "id": property_group.id,
                    "name": property_group.name,
                    "properties": properties,
                })

    if product.is_variant():
        qs = ProductPropertyValue.objects.filter(product=product, type=PROPERTY_VALUE_TYPE_VARIANT)
        for ppv in qs:
            try:
                property_option = PropertyOption.objects.get(property_id=ppv.property_id, pk=ppv.value)
                product_variant_properties.append(property_option)
            except (ProductPropertyValue.DoesNotExist, PropertyOption.DoesNotExist):
                continue

    # Generate list of all property groups; used for group selection
    product_property_group_ids = [p.id for p in product.property_groups.all()]
    shop_property_groups = []
    for property_group in PropertyGroup.objects.all():

        shop_property_groups.append({
            "id": property_group.id,
            "name": property_group.name,
            "selected": property_group.id in product_property_group_ids,
        })

    return render_to_string(template_name, RequestContext(request, {
        "product": product,
        "filterables": filterables,
        "display_filterables": display_filterables,
        "configurables": configurables,
        "display_configurables": display_configurables,
        "displayables": displayables,
        "display_displayables": display_displayables,
        "product_property_groups": product.property_groups.all(),
        "shop_property_groups": shop_property_groups,
        "product_variant_properties": product_variant_properties
    }))


@permission_required("core.manage_shop")
@require_POST
def update_property_groups(request, product_id):
    """Updates property groups for the product with passed id.
    """
    selected_group_ids = request.POST.getlist("selected-property-groups")
    product = Product.objects.get(pk=product_id)

    for property_group in PropertyGroup.objects.all():
        # if the group is within selected groups we try to add it to the product
        # otherwise we try do delete it
        if str(property_group.id) in selected_group_ids:
            try:
                property_group.products.get(pk=product_id)
            except ObjectDoesNotExist:
                property_group.products.add(product_id)
        else:
            property_group.products.remove(product_id)
            product_removed_property_group.send(send=property_group, product=product)

    update_product_cache(product)

    url = reverse("lfs_manage_product", kwargs={"product_id": product_id})
    return HttpResponseRedirect(url)


@permission_required("core.manage_shop")
@require_POST
def update_properties(request, product_id):
    """Updates properties for product with passed id.
    """
    ppv_type = int(request.POST.get("type"))
    product = get_object_or_404(Product, pk=product_id)
    ProductPropertyValue.objects.filter(product=product_id, type=ppv_type).delete()

    # Update property values
    for key in request.POST.keys():
        if not key.startswith("property"):
            continue

        property_id = key.split("-")[1]
        prop = get_object_or_404(Property, pk=property_id)

        for value in request.POST.getlist(key):
            if prop.is_valid_value(value):
                # we have to use get_or_create because it is possible that we get same property values twice, eg.
                # if we have a SELECT typ property assigned to two different groups, and both these groups bound
                # to the product. In this case we will have same property shown twice at management page
                ProductPropertyValue.objects.get_or_create(product=product, property=prop, value=value, type=ppv_type)
    update_product_cache(product)

    url = reverse("lfs_manage_product", kwargs={"product_id": product_id})
    return HttpResponseRedirect(url)
