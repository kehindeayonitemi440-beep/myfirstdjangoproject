import django.db.models.deletion
from django.db import migrations, models

from shop import defaults as d


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=60, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=70, unique=True)),
                ("order", models.PositiveSmallIntegerField(default=0)),
            ],
            options={"verbose_name_plural": "categories", "ordering": ["order", "name"]},
        ),
        migrations.CreateModel(
            name="Fact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.CharField(max_length=30)),
                ("label", models.CharField(max_length=60)),
                ("order", models.PositiveSmallIntegerField(default=0)),
            ],
            options={"ordering": ["order", "id"]},
        ),
        migrations.CreateModel(
            name="SiteSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("brand_name", models.CharField(default=d.BRAND_NAME, max_length=80)),
                ("whatsapp_number", models.CharField(default=d.WHATSAPP_NUMBER, help_text="With country code, e.g. +234 815 658 9089.", max_length=25)),
                ("email", models.EmailField(default=d.EMAIL, max_length=254)),
                ("instagram_url", models.URLField(default=d.INSTAGRAM_URL)),
                ("hero_heading", models.CharField(default=d.HERO_HEADING, max_length=120)),
                ("hero_text", models.TextField(default=d.HERO_TEXT)),
                ("shop_intro", models.TextField(default=d.SHOP_INTRO)),
                ("about_heading", models.CharField(default=d.ABOUT_HEADING, max_length=120)),
                ("about_text", models.TextField(default=d.ABOUT_TEXT, help_text="Separate paragraphs with a blank line.")),
                ("portrait", models.ImageField(blank=True, upload_to="site/")),
                ("contact_text", models.TextField(default=d.CONTACT_TEXT)),
            ],
            options={"verbose_name": "site settings", "verbose_name_plural": "site settings"},
        ),
        migrations.CreateModel(
            name="Testimonial",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quote", models.TextField()),
                ("author", models.CharField(blank=True, max_length=80)),
                ("is_published", models.BooleanField(default=True)),
                ("order", models.PositiveSmallIntegerField(default=0)),
            ],
            options={"ordering": ["order", "id"]},
        ),
        migrations.CreateModel(
            name="Fabric",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("description", models.CharField(blank=True, max_length=140)),
                ("image", models.ImageField(blank=True, help_text="Optional photo. If empty, the CSS pattern swatch below is shown.", upload_to="fabrics/")),
                ("pattern", models.CharField(choices=[("p1", "Indigo floral (red, gold, white)"), ("p2", "Sunburst geometric"), ("p3", "Green and cream stripes"), ("p4", "Red scallop"), ("p5", "Black and cream checker"), ("p6", "Teal with gold leaves"), ("p7", "Plum lattice"), ("p8", "Indigo ripple")], default="p1", max_length=2, verbose_name="swatch pattern")),
                ("price", models.DecimalField(blank=True, decimal_places=2, help_text="Leave empty to show 'Ask for price'.", max_digits=10, null=True, verbose_name="price per 6-yard bundle (₦)")),
                ("is_available", models.BooleanField(default=True)),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="fabrics", to="shop.category")),
            ],
            options={"ordering": ["order", "name"]},
        ),
    ]
