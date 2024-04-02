from modeltranslation.translator import translator, TranslationOptions

from .models import Category, Product


class CategoryTranslationOptions(TranslationOptions):
    fields = ['name', ]


translator.register(Category, CategoryTranslationOptions)


class ProductTranslationOptions(TranslationOptions):
    fields = ['name', ]


translator.register(Product, ProductTranslationOptions)
