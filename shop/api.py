"""Read-only JSON API consumed by the Next.js frontend."""
from django.http import JsonResponse, Http404
from .models import Product, SiteSettings


def _image_url(request, image_field):
    return request.build_absolute_uri(image_field.url)


def _product_summary(request, p):
    return {
        "slug": p.slug,
        "name": p.name,
        "category": p.category,
        "categoryLabel": p.get_category_display(),
        "priceDisplay": p.price_display,
        "priceNpr": p.price_npr,
        "startingFrom": p.starting_from,
        "quantity": p.quantity,
        "soldOut": p.sold_out,
        "buildTime": p.build_time,
        "shortDescription": p.short_description,
        "featured": p.featured,
        "thumbnail": _image_url(request, p.main_image.image) if p.main_image else None,
    }


def product_list(request):
    products = Product.objects.filter(published=True).prefetch_related("images")
    return JsonResponse({
        "products": [_product_summary(request, p) for p in products]
    })


def product_detail(request, slug):
    try:
        p = Product.objects.prefetch_related("images").get(slug=slug, published=True)
    except Product.DoesNotExist:
        raise Http404
    data = _product_summary(request, p)
    data.update({
        "description": p.description,
        "specs": {
            "polyCount": p.poly_count,
            "formats": p.formats_display,
            "textures": p.textures,
            "buildTime": p.build_time,
            "license": p.license_terms,
        },
        "gallery": [_image_url(request, img.image) for img in p.images.all()],
    })
    return JsonResponse(data)


def settings_view(request):
    s = SiteSettings.load()
    return JsonResponse({
        "brandName": s.brand_name,
        "tagline": s.tagline,
        "location": s.location,
        "whatsappNumber": s.whatsapp_number,
        "customBuildMessage": s.custom_build_message,
        "aboutText": s.about_text,
        "socials": [{"label": l, "url": u} for l, u in s.socials],
    })


def health(request):
    return JsonResponse({"status": "ok", "service": "polyghar-backend"})
