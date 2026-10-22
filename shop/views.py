from django.shortcuts import render

from .models import Category, Fabric, Fact, Testimonial


def index(request):
    fabrics = Fabric.objects.filter(is_available=True).select_related("category")
    categories = Category.objects.filter(fabrics__is_available=True).distinct()
    return render(
        request,
        "shop/index.html",
        {
            "fabrics": fabrics,
            "categories": categories,
            "testimonials": Testimonial.objects.filter(is_published=True),
            "facts": Fact.objects.all(),
        },
    )
