# from django.contrib import admin
from admin_confirm.admin import confirm_action
from admin_confirm import AdminConfirmMixin
class MyProductAdmin(AdminConfirmMixin):
    actions = [
        "activate","deactivate","make_special","make_unspecial"]
    
    @confirm_action
    def activate(modeladmin, request, queryset):
        queryset.update(is_active = True)

    @confirm_action
    def deactivate(modeladmin, request, queryset):
        queryset.update(is_active = False)

    @confirm_action
    def make_special(modeladmin, request, queryset):
        queryset.update(is_special = True)

    @confirm_action
    def make_unspecial(modeladmin, request, queryset):
        queryset.update(is_special = False)
        
    activate.allowed_permissions = ('change',)
    deactivate.allowed_permissions = ('change',)
    make_special.allowed_permissions = ('change',)
    make_unspecial.allowed_permissions = ('change',)