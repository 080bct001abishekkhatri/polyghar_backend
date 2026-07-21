from urllib.parse import quote
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class SiteSettings(models.Model):
    """Your store's identity — edit it in the admin under 'Site settings'.
    There is only ever one row of this."""

    brand_name = models.CharField(max_length=60, default="PolyGhar")
    tagline = models.CharField(max_length=120, default="3D models handcrafted in Blender")
    location = models.CharField(max_length=80, default="Kathmandu, Nepal")
    whatsapp_number = models.CharField(
        max_length=20,
        default="9779XXXXXXXXX",
        help_text="Digits only, starting with country code. Nepal example: 9779812345678 — no +, no spaces.",
    )
    custom_build_message = models.CharField(
        max_length=300,
        default="Hi! I'd like a custom 3D build. Here's what I need: ",
        help_text="Pre-filled WhatsApp text for the 'Request Custom Build' button.",
    )
    about_text = models.TextField(
        blank=True,
        default=(
            "I'm a 3D artist working entirely in Blender. Everything in the shop is "
            "modeled, textured and lit by me. Order over WhatsApp and you're talking "
            "directly to the person who built the model."
        ),
        help_text="Your bio on the About page. Blank lines create new paragraphs.",
    )
    instagram_url = models.URLField(blank=True)
    artstation_url = models.URLField(blank=True)
    sketchfab_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce a single row
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def wa_link(self, message: str) -> str:
        return f"https://wa.me/{self.whatsapp_number}?text={quote(message)}"

    @property
    def custom_build_link(self):
        return self.wa_link(self.custom_build_message)

    @property
    def socials(self):
        return [
            (label, url)
            for label, url in (
                ("Instagram", self.instagram_url),
                ("ArtStation", self.artstation_url),
                ("Sketchfab", self.sketchfab_url),
            )
            if url
        ]


class Product(models.Model):
    class Category(models.TextChoices):
        PRE_MADE = "pre-made", "Pre-made"
        CUSTOM_SAMPLE = "custom-sample", "Custom work"

    name = models.CharField(max_length=100, help_text="Product name shown everywhere.")
    slug = models.SlugField(
        max_length=120, unique=True, blank=True,
        help_text="Auto-filled from the name — leave blank.",
    )
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.PRE_MADE
    )
    price_npr = models.PositiveIntegerField(
        verbose_name="Price (NPR)", help_text="Numbers only, e.g. 1500"
    )
    starting_from = models.BooleanField(
        default=False,
        help_text="Tick to show the price as 'Starting from NPR …' (for custom work).",
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="How many you have. At 0 the product shows as 'Sold out'.",
    )
    build_time = models.CharField(
        max_length=60, blank=True,
        help_text="How long it takes to build/deliver, e.g. '3 days'. Optional.",
    )
    short_description = models.CharField(
        max_length=160, help_text="One line shown on the product card."
    )
    description = models.TextField(help_text="Full text shown on the product page.")

    # specs
    poly_count = models.CharField(max_length=60, blank=True, help_text="e.g. 12k tris")
    formats = models.CharField(
        max_length=100, default="blend, fbx, obj",
        help_text="File formats, separated by commas.",
    )
    textures = models.CharField(max_length=100, blank=True, help_text="e.g. 2K PBR full set")
    license_terms = models.CharField(
        max_length=200, blank=True,
        default="Personal & commercial use. No resale of the raw model files.",
    )

    featured = models.BooleanField(
        default=False, help_text="Tick to show this product on the Home page."
    )
    published = models.BooleanField(
        default=True, help_text="Untick to hide this product from the site without deleting it."
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug, n = base, 2
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.slug])

    @property
    def sold_out(self):
        return self.quantity == 0

    @property
    def price_display(self):
        price = f"NPR {self.price_npr:,}"
        return f"Starting from {price}" if self.starting_from else price

    @property
    def formats_display(self):
        return "  ·  ".join(
            f".{f.strip().lstrip('.')}" for f in self.formats.split(",") if f.strip()
        )

    @property
    def main_image(self):
        # Iterates instead of .first() so it reuses prefetched images
        # (avoids one extra query per product on the list API).
        for image in self.images.all():
            return image
        return None

    def whatsapp_link(self, request=None):
        settings_obj = SiteSettings.load()
        url = self.get_absolute_url()
        if request is not None:
            url = request.build_absolute_uri(url)
        message = f"Hi! I'm interested in this 3D model: {self.name} ({self.price_display}) — {url}"
        return settings_obj.wa_link(message)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="products/",
        help_text="JPG or PNG. Around 1200×900 px looks best.",
    )
    sort_order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers show first. The first image is the thumbnail."
    )

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"Photo of {self.product.name}"
