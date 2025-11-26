from asgiref.sync import sync_to_async

from bot.models import Branch, Categories, Product, City


@sync_to_async
def get_all_regions():
    return list(City.objects.all())

@sync_to_async
def get_all_branches():
    return list(Branch.objects.all())

@sync_to_async
def get_branch_by_title(title):
    return Branch.objects.filter(title=title).first()

@sync_to_async
def get_all_categories():
    return list(Categories.objects.all())

@sync_to_async
def get_products_by_category(category_title):
    return list(Product.objects.filter(category__title=category_title))

@sync_to_async
def get_product_by_title(title):
    return Product.objects.filter(title=title).first()
