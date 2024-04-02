from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from app.address.models import Branch, Address


@admin.register(Branch)
class BranchAdmin(TabbedTranslationAdmin):
    ...


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    ...
