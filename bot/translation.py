from modeltranslation.translator import translator, TranslationOptions
from .models import Branch, Categories, Product, City


class BranchTranslationOptions(TranslationOptions):
    fields = ('title', 'location', 'target')
    required_languages = ('uz', 'en')


class CategoriesTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('uz', 'en')


class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    required_languages = ('uz', 'en')


class CityTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('uz', 'en')


translator.register(Branch, BranchTranslationOptions)
translator.register(Categories, CategoriesTranslationOptions)
translator.register(Product, ProductTranslationOptions)
translator.register(City, CityTranslationOptions)