from django.contrib import admin

from .models import Category, Fabric, Fact, SiteSettings, Testimonial

admin.site.site_header = "Fabric shop admin"
admin.site.site_title = "Fabric shop"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Fabric)
class FabricAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available", "order")
    list_editable = ("price", "is_available", "order")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("quote", "author", "is_published", "order")
    list_editable = ("is_published", "order")


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "order")
    list_editable = ("order",)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
