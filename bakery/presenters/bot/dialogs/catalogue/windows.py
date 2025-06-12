from bakery.domains.entities.product import ProductCategory
from bakery.presenters.bot.content.buttons.catalogue import common as category_btn

CATEGORY_ITEMS = [
    dict(id=ProductCategory.BREAD, text=category_btn.BREAD),
    dict(id=ProductCategory.OIL, text=category_btn.OIL),
    dict(id=ProductCategory.FLOUR, text=category_btn.FLOUR),
    dict(id=ProductCategory.DESSERT, text=category_btn.DESSERT),
    dict(id=ProductCategory.NOODLE, text=category_btn.NOODLE),
    dict(id=ProductCategory.OTHER, text=category_btn.OTHER),
]
