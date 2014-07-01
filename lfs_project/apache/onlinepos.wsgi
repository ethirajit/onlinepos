import os, sys, site

site.addsitedir('/usr/local/lib/python2.7/site-packages/')
sys.path.insert(0, '/usr/local/lib/python2.7/site-packages')

sys.path[0:0] = [
  '/home/onlinepos_django-lfs/eggs/django_lfs-0.9.0a1-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/djangorecipe-1.9-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/Django-1.6.5-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/zc.recipe.egg-2.0.1-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/zc.buildout-2.2.1-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/South-0.8.4-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/Pillow-2.4.0-py2.7-linux-x86_64.egg',
  '/home/onlinepos_django-lfs/eggs/lfs_theme-0.9.0a1-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/lfs_paypal-1.2-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/lfs_order_numbers-1.0b1-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/lfs_contact-1.1-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/django_reviews-1.0-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/django_postal-0.95-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/django_portlets-1.1.1-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/django_pagination-1.0.7-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/django_paypal-0.1.2.lfs_1-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/django_localflavor-1.0-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/django_compressor-1.4-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/setuptools-5.1-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/django_piston-0.2.3-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/django_countries-2.1.2-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/six-1.7.2-py2.7.egg',
  '/home/onlinepos_django-lfs/eggs/django_appconf-0.6-py2.7.egg',
  '/home/onlinepos_django-lfs',
  '/home/onlinepos_django-lfs/lfs_project',
  ]

os.environ['PATH'] = '%s:%s' % ('/home/onlinepos_django-lfs/bin', os.environ['PATH']) 
os.environ['DJANGO_SETTINGS_MODULE'] = 'lfs_project.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
