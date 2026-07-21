import json
from django.test import TestCase
from shop.models import Product, SiteSettings


class ApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        s = SiteSettings.load()
        s.whatsapp_number = "9779800000000"
        s.save()
        cls.product = Product.objects.create(
            name="Test Robot", price_npr=2500, quantity=2, build_time="3 days",
            short_description="A robot.", description="A test robot.",
        )
        Product.objects.create(
            name="Hidden", price_npr=1, published=False,
            short_description="x", description="x",
        )
        Product.objects.create(
            name="Gone", price_npr=1, quantity=0,
            short_description="x", description="x",
        )

    def get_json(self, url):
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200, url)
        return json.loads(r.content)

    def test_product_list(self):
        data = self.get_json("/api/products/")
        names = [p["name"] for p in data["products"]]
        self.assertIn("Test Robot", names)
        self.assertNotIn("Hidden", names)

    def test_sold_out_flag(self):
        data = self.get_json("/api/products/")
        gone = next(p for p in data["products"] if p["name"] == "Gone")
        self.assertTrue(gone["soldOut"])

    def test_product_detail(self):
        data = self.get_json("/api/products/test-robot/")
        self.assertEqual(data["priceDisplay"], "NPR 2,500")
        self.assertEqual(data["specs"]["buildTime"], "3 days")
        self.assertEqual(data["specs"]["formats"], ".blend  ·  .fbx  ·  .obj")

    def test_detail_404s(self):
        self.assertEqual(self.client.get("/api/products/nope/").status_code, 404)
        self.assertEqual(self.client.get("/api/products/hidden/").status_code, 404)

    def test_settings_endpoint(self):
        data = self.get_json("/api/settings/")
        self.assertEqual(data["whatsappNumber"], "9779800000000")
        self.assertEqual(data["brandName"], "PolyGhar")

    def test_cors_header(self):
        r = self.client.get("/api/products/")
        self.assertEqual(r["Access-Control-Allow-Origin"], "*")

    def test_health(self):
        self.assertEqual(self.get_json("/api/health/")["status"], "ok")
