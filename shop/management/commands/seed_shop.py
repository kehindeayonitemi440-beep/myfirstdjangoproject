from django.core.management.base import BaseCommand

from shop.models import Category, Fabric, Fact, SiteSettings, Testimonial

CATEGORIES = ["Ankara", "Lace", "Aso-oke", "Adire"]

# name, category, pattern, description
FABRICS = [
    ("Royal Garden", "Ankara", "p1", "Bold floral, real wax"),
    ("Sunburst", "Ankara", "p2", "Geometric, high contrast"),
    ("Savannah Stripe", "Ankara", "p3", "Green and cream stripes"),
    ("Crimson Scallop", "Ankara", "p4", "Scallop motif, rich red"),
    ("Ife Checker", "Adire", "p5", "Hand-dyed look, indigo"),
    ("Ocean Leaf", "Lace", "p6", "Soft teal, gold leaves"),
    ("Plum Lattice", "Aso-oke", "p7", "Woven feel, ceremonial"),
    ("Ripple", "Adire", "p8", "Ripple resist-dye pattern"),
]

TESTIMONIALS = [
    "The colours looked even better in person. My aso-ebi group was thrilled.",
    "Fast replies, honest prices, and the fabric didn't fade after washing.",
    "I ordered some bundles for an event and everything arrived on time.",
]

FACTS = [
    ("500+", "happy customers"),
    ("6 yards", "every bundle, measured"),
    ("36", "states delivered to"),
]


class Command(BaseCommand):
    help = "Load the sample content from the original one-page site (safe to re-run)."

    def handle(self, *args, **options):
        SiteSettings.load()

        cats = {}
        for i, name in enumerate(CATEGORIES):
            cats[name], _ = Category.objects.get_or_create(
                name=name, defaults={"order": i}
            )

        for i, (name, cat, pattern, desc) in enumerate(FABRICS):
            Fabric.objects.get_or_create(
                name=name,
                defaults={
                    "category": cats[cat],
                    "pattern": pattern,
                    "description": desc,
                    "order": i,
                },
            )

        for i, quote in enumerate(TESTIMONIALS):
            Testimonial.objects.get_or_create(quote=quote, defaults={"order": i})

        for i, (value, label) in enumerate(FACTS):
            Fact.objects.get_or_create(
                value=value, label=label, defaults={"order": i}
            )

        self.stdout.write(self.style.SUCCESS("Sample shop content loaded."))
