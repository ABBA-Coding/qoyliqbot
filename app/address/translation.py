from modeltranslation.translator import translator, TranslationOptions

from .models import Branch


class BranchTranslationOptions(TranslationOptions):
    fields = ['name', 'description']


translator.register(Branch, BranchTranslationOptions)
