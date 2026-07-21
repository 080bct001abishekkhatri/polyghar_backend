"""Loads 4 demo products with placeholder images so you can preview the site.
Run:  python manage.py seed_demo
Safe to run once; it skips products that already exist."""
from pathlib import Path
from django.core.files import File
from django.core.management.base import BaseCommand
from shop.models import Product, ProductImage, SiteSettings

SEED_DIR = Path(__file__).resolve().parents[3] / "seed_images"

DEMO = [
    dict(name="Medieval Castle Kit", category="pre-made", price_npr=1500,
         quantity=3, build_time="Ready now", featured=True,
         short_description="Modular castle kit — towers, walls, gates and keep, game-ready.",
         description=("A modular medieval castle kit built in Blender. Includes separate tower, "
                      "wall, gate and keep pieces so you can assemble your own layouts. Clean quads, "
                      "non-overlapping UVs, and a 2K stone texture set."),
         poly_count="12k tris (full assembly)", textures="2K PBR (albedo, normal, roughness)",
         images=["castle-thumb.jpg", "castle-1.jpg", "castle-2.jpg"]),
    dict(name="Newari Carved Window (Ankhi Jhyal)", category="pre-made", price_npr=900,
         quantity=5, build_time="Ready now", featured=True,
         short_description="Traditional carved wooden window, modeled from Bhaktapur references.",
         description=("A detailed traditional Newari lattice window modeled from real references in "
                      "Bhaktapur. High-detail carved frame with a separate low-poly version included."),
         poly_count="28k tris (hi) / 4k tris (lo)", textures="2K PBR wood set",
         images=["window-thumb.jpg", "window-1.jpg", "window-2.jpg"]),
    dict(name="Stylized Pagoda Temple", category="pre-made", price_npr=2000,
         quantity=0, build_time="Ready now", featured=True,
         short_description="Hand-painted style multi-tier temple inspired by Nyatapola.",
         description=("A stylized multi-tiered pagoda temple inspired by Nyatapola, with hand-painted "
                      "style textures. Optimized for real-time engines — tested in Unity and Unreal."),
         poly_count="18k tris", textures="2K hand-painted albedo + normal",
         images=["temple-thumb.jpg", "temple-1.jpg", "temple-2.jpg"]),
    dict(name="Sci-Fi Hover Drone", category="custom-sample", price_npr=3500,
         starting_from=True, quantity=1, build_time="About 1 week", featured=False,
         short_description="Client commission — hard-surface drone with rigged rotors.",
         description=("A hard-surface hover drone built as a client commission — shown here as an "
                      "example of custom work. Fully rigged rotors and landing gear, baked 4K textures."),
         poly_count="35k tris", textures="4K PBR full set",
         license_terms="Commission work — license agreed per project.",
         images=["drone-thumb.jpg", "drone-1.jpg", "drone-2.jpg"]),
]


class Command(BaseCommand):
    help = "Load demo products with placeholder images"

    def handle(self, *args, **options):
        SiteSettings.load()
        for item in DEMO:
            images = item.pop("images")
            if Product.objects.filter(name=item["name"]).exists():
                self.stdout.write(f"skip (exists): {item['name']}")
                continue
            product = Product.objects.create(**item)
            for i, filename in enumerate(images):
                path = SEED_DIR / filename
                if not path.exists():
                    continue
                with open(path, "rb") as fh:
                    pi = ProductImage(product=product, sort_order=i)
                    pi.image.save(filename, File(fh), save=True)
            self.stdout.write(self.style.SUCCESS(f"created: {product.name}"))
        self.stdout.write(self.style.SUCCESS("Done — demo data loaded."))
