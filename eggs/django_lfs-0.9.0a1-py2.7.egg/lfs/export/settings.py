# django imports
from django.utils.translation import ugettext_lazy as _

CATEGORY_VARIANTS_NONE = 0
CATEGORY_VARIANTS_DEFAULT = 1
CATEGORY_VARIANTS_CHEAPEST = 2
CATEGORY_VARIANTS_ALL = 3

CATEGORY_VARIANTS_CHOICES = (
    (CATEGORY_VARIANTS_NONE, _(u"---")),
    (CATEGORY_VARIANTS_DEFAULT, _(u"Default")),
    (CATEGORY_VARIANTS_CHEAPEST, _(u"Cheapest")),
    (CATEGORY_VARIANTS_ALL, _(u"All")),
)
