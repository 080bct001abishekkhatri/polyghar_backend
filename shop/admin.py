from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductImage, SiteSettings

admin.site.site_header = "PolyGhar — store manager"
admin.site.site_title = "PolyGhar admin"
admin.site.index_title = "Manage your store"


class ProductImageInline(admin.TabularInline):
    """Photo rows inside the product form — add as many as you like,
    tick 'Delete' on a row and save to remove a photo."""
    model = ProductImage
    extra = 1
    fields = ("preview", "image", "sort_order")
    readonly_fields = ("preview",)

    @admin.display(description="Preview")
    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="height:70px;border-radius:4px" />', obj.image.url
            )
        return "—"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "category", "price_col", "quantity",
                    "build_time", "featured", "published")
    list_display_links = ("thumb", "name")
    list_editable = ("quantity", "featured", "published")
    list_filter = ("category", "featured", "published")
    search_fields = ("name", "description")
    readonly_fields = ("slug",)
    inlines = [ProductImageInline]
    fieldsets = (
        ("The basics", {
            "fields": ("name", "category", "price_npr", "starting_from",
                       "quantity", "build_time"),
        }),
        ("Text", {"fields": ("short_description", "description")}),
        ("Specs (shown on the product page)", {
            "fields": ("poly_count", "formats", "textures", "license_terms"),
        }),
        ("Visibility", {"fields": ("featured", "published", "slug")}),
    )

    @admin.display(description="")
    def thumb(self, obj):
        img = obj.main_image
        if img:
            return format_html(
                '<img src="{}" style="height:44px;width:58px;object-fit:cover;border-radius:4px" />',
                img.image.url,
            )
        return "—"

    @admin.display(description="Price")
    def price_col(self, obj):
        return obj.price_display


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Brand", {"fields": ("brand_name", "tagline", "location")}),
        ("WhatsApp", {"fields": ("whatsapp_number", "custom_build_message")}),
        ("About page", {"fields": ("about_text",)}),
        ("Social links (leave blank to hide)", {
            "fields": ("instagram_url", "artstation_url", "sketchfab_url"),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
