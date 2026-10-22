# Kehinde Oluwaseun – Ankara and fine fabrics (Django)

The original one-page site, converted to a Django project. Fabrics, testimonials,
facts, contact details and page copy are all editable from the Django admin.

## Quick start

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_shop        # loads the 8 sample fabrics, reviews and facts
python manage.py createsuperuser
python manage.py runserver
```

- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

If Django reports model changes without a migration, run
`python manage.py makemigrations shop`. Run the tests with `python manage.py test`.

## Structure

```
config/                 settings, urls, wsgi/asgi
shop/
  models.py             Category, Fabric, Testimonial, Fact, SiteSettings (singleton)
  views.py              index view
  admin.py              admin configuration
  context_processors.py exposes `site` (SiteSettings) to every template
  defaults.py           default page copy
  management/commands/seed_shop.py
  templates/shop/       base.html, index.html, partials/
  static/shop/          css/style.css, js/main.js
```

## What changed from the HTML file

- Fabrics were a JavaScript array; they are now the `Fabric` model rendered by
  Django templates. Category filter buttons are generated from the data.
- The WhatsApp number lives in **Site settings** and is reduced to digits for
  `wa.me` links (the original had `+` and spaces, which break the link).
- The original cards showed the description in the price slot and "undefined"
  in the subtitle. Fixed: fabrics now have a real `price` field (₦ per 6-yard
  bundle). Prices are blank in the seed data and show "Ask for price" until set.
- Fabrics can have an optional photo; otherwise the CSS pattern swatch is used.
- Layout, light/dark theme and styling are unchanged (`static/shop/css/style.css`).

## Deploying to Render

Use the [Render deployment guide](DEPLOY_RENDER.md). The included `render.yaml`
configures a Render web service, PostgreSQL, a persistent upload disk, static
file collection, migrations, and Gunicorn. Local SQLite data and media are not
automatically transferred to the production resources.
# myfirstdjangoproject
