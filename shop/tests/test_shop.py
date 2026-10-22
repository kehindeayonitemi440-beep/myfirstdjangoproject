from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from shop.models import Category, Fabric, SiteSettings, Testimonial


class SiteSettingsTests(TestCase):
    def test_singleton(self):
        a = SiteSettings.load()
        SiteSettings(brand_name="Other").save()
        self.assertEqual(SiteSettings.objects.count(), 1)
        self.assertEqual(SiteSettings.load().pk, a.pk)

    def test_whatsapp_digits_strip_formatting(self):
        s = SiteSettings.load()
        self.assertEqual(s.whatsapp_digits, "2348156589089")
        self.assertEqual(s.whatsapp_url, "https://wa.me/2348156589089")

    def test_initials(self):
        self.assertEqual(SiteSettings.load().initials, "KO")


class IndexTests(TestCase):
    def setUp(self):
        self.ankara = Category.objects.create(name="Ankara")
        self.lace = Category.objects.create(name="Lace")
        Fabric.objects.create(
            name="Royal Garden", category=self.ankara, price=Decimal("12500")
        )
        Fabric.objects.create(name="Hidden", category=self.lace, is_available=False)

    def test_index_renders(self):
        r = self.client.get(reverse("shop:index"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Royal Garden")
        self.assertContains(r, "₦12,500")
        self.assertContains(r, "https://wa.me/2348156589089?text=")

    def test_unavailable_fabric_and_empty_category_hidden(self):
        r = self.client.get(reverse("shop:index"))
        self.assertNotContains(r, "Hidden")
        self.assertNotContains(r, 'data-f="lace"')

    def test_missing_price_shows_ask(self):
        Fabric.objects.create(name="No Price", category=self.ankara)
        self.assertContains(self.client.get(reverse("shop:index")), "Ask for price")

    def test_unpublished_testimonial_hidden(self):
        Testimonial.objects.create(quote="Secret draft", is_published=False)
        Testimonial.objects.create(quote="Lovely cloth")
        r = self.client.get(reverse("shop:index"))
        self.assertContains(r, "Lovely cloth")
        self.assertNotContains(r, "Secret draft")
