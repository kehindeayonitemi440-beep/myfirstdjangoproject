import re

from django.db import models
from django.utils.text import slugify

from . import defaults as d


class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Fabric(models.Model):
    PATTERN_CHOICES = [
        ("p1", "Indigo floral (red, gold, white)"),
        ("p2", "Sunburst geometric"),
        ("p3", "Green and cream stripes"),
        ("p4", "Red scallop"),
        ("p5", "Black and cream checker"),
        ("p6", "Teal with gold leaves"),
        ("p7", "Plum lattice"),
        ("p8", "Indigo ripple"),
    ]

    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="fabrics"
    )
    description = models.CharField(max_length=140, blank=True)
    image = models.ImageField(
        upload_to="fabrics/",
        blank=True,
        help_text="Optional photo. If empty, the CSS pattern swatch below is shown.",
    )
    pattern = models.CharField(
        "swatch pattern", max_length=2, choices=PATTERN_CHOICES, default="p1"
    )
    price = models.DecimalField(
        "price per 6-yard bundle (₦)",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Leave empty to show 'Ask for price'.",
    )
    is_available = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    @property
    def order_message(self):
        return (
            f"Hello Kehinde, I'd like to order {self.name} "
            f"({self.category.name}). How many bundles are available?"
        )


class Testimonial(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=80, blank=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.quote[:50]


class Fact(models.Model):
    """Headline numbers in the About section (e.g. '500+' / 'happy customers')."""

    value = models.CharField(max_length=30)
    label = models.CharField(max_length=60)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.value} {self.label}"


class SiteSettings(models.Model):
    """Single-row table holding the editable copy and contact details."""

    brand_name = models.CharField(max_length=80, default=d.BRAND_NAME)
    whatsapp_number = models.CharField(
        max_length=25,
        default=d.WHATSAPP_NUMBER,
        help_text="With country code, e.g. +234 815 658 9089.",
    )
    email = models.EmailField(default=d.EMAIL)
    instagram_url = models.URLField(default=d.INSTAGRAM_URL)

    hero_heading = models.CharField(max_length=120, default=d.HERO_HEADING)
    hero_text = models.TextField(default=d.HERO_TEXT)
    shop_intro = models.TextField(default=d.SHOP_INTRO)

    about_heading = models.CharField(max_length=120, default=d.ABOUT_HEADING)
    about_text = models.TextField(
        default=d.ABOUT_TEXT, help_text="Separate paragraphs with a blank line."
    )
    portrait = models.ImageField(upload_to="site/", blank=True)

    contact_text = models.TextField(default=d.CONTACT_TEXT)

    class Meta:
        verbose_name = "site settings"
        verbose_name_plural = "site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce a single row
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # never delete the singleton

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def initials(self):
        return "".join(w[0] for w in self.brand_name.split()[:2]).upper()

    @property
    def whatsapp_digits(self):
        return re.sub(r"\D", "", self.whatsapp_number)

    @property
    def whatsapp_url(self):
        return f"https://wa.me/{self.whatsapp_digits}"
