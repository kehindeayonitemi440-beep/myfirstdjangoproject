# Deploying to Render

This project is configured for a Render web service, managed PostgreSQL, and a
persistent disk for uploaded product and portrait images. The included
`render.yaml` is a Render Blueprint: it provisions those resources, installs
the Python dependencies, collects static assets, applies database migrations,
and starts Gunicorn.

## Before you deploy

1. Put the project in a GitHub, GitLab, or Bitbucket repository that Render can
   access. Include `render.yaml`, `requirements.txt`, and the `config/` and
   `shop/` directories. Do not commit `.env`, credentials, or your local
   `db.sqlite3`.
2. Check that the content and images you want to publish are ready. The
   Blueprint creates an empty production database; local SQLite data and the
   ignored `media/` directory are not copied automatically.
3. Review the selected Render plans in the Blueprint before creating resources.
   This configuration uses a paid Starter web service, a Basic PostgreSQL
   instance, and a 1 GB persistent disk. Render displays current pricing and
   resource terms during setup.

## Create the Render services

1. Sign in to [Render](https://dashboard.render.com/) and choose **New →
   Blueprint**.
2. Connect the repository and select the branch to deploy.
3. Confirm the Blueprint preview contains the `ankara-store` web service and
   `ankara-store-db` database, then apply it. Keep the generated value for
   `DJANGO_SECRET_KEY` private; Render creates and stores it as an environment
   variable.
4. Wait for the first deploy to finish. The build installs the requirements and
   runs `collectstatic`; the pre-deploy step applies migrations; Gunicorn then
   serves the app. Open the `onrender.com` URL shown on the service page.

The service reads the Render-provided `DATABASE_URL`. `RENDER_EXTERNAL_HOSTNAME`
is automatically added to Django's allowed hosts and CSRF trusted origins.
HTTPS redirects and secure session/CSRF cookies are enabled in production.
WhiteNoise serves versioned, compressed static files. Uploaded images are
stored under `/var/data/media` on the persistent disk.

## Finish the initial setup

1. Open the service's **Shell** from the Render dashboard and create an admin
   account:

   ```sh
   python manage.py createsuperuser
   ```

2. Visit `https://<your-service>.onrender.com/admin/` and sign in.
3. Add or edit **Site settings**, categories, fabrics, prices, testimonials,
   and facts. Upload the live images through the admin. The local seed command
   is optional sample content; it is not run automatically in production.
4. Check the home page and admin page, verify CSS and JavaScript load, and test
   that uploaded images remain available after a redeploy.

## Environment variables

The Blueprint sets the following values:

| Variable | Purpose |
| --- | --- |
| `DJANGO_DEBUG=0` | Disables Django debug mode. Keep this off in production. |
| `DJANGO_SECRET_KEY` | A generated private Django signing key. Do not share or commit it. |
| `DATABASE_URL` | Internal connection URL for the Blueprint's PostgreSQL database. |
| `MEDIA_ROOT=/var/data/media` | Upload location on the persistent Render disk. |

Render supplies `RENDER_EXTERNAL_HOSTNAME` to the web service. For a custom
domain, add it in the service's **Settings → Custom Domains**, then add these
environment variables in **Environment** and redeploy:

- `DJANGO_ALLOWED_HOSTS`: the service hostname and custom hostnames, separated
  by commas (for example, `ankara-store.onrender.com,shop.example.com,www.shop.example.com`).
- `DJANGO_CSRF_TRUSTED_ORIGINS`: full HTTPS origins separated by commas (for
  example, `https://shop.example.com,https://www.shop.example.com`).

Do not include paths or trailing slashes in CSRF origins. Render provisions TLS
for configured custom domains; wait until the domain is verified and its
certificate is active before forcing visitors to use it.

## Deploy updates

Push changes to the connected branch. Render builds the app, collects static
files, runs `python manage.py migrate` as the pre-deploy command, and deploys
the new web process. Review the deploy log if a build or migration fails; fix
the cause and deploy again rather than bypassing a failed migration.

For a manual deploy, use **Manual Deploy → Deploy latest commit** on the Render
service. Do not run the development server (`manage.py runserver`) in
production.

## Database and media considerations

- The production database is separate from `db.sqlite3`. The pre-deploy
  migration applies schema changes but does not import local shop records.
- Back up PostgreSQL before risky data migrations. Use Render's database
  backups/exports before changing database resources or plans.
- The persistent disk protects uploaded files across deploys, but it is
  attached to this service and is not a substitute for off-site backups. Keep
  a separate copy of important product images.
- The initial repository media files, if any, are not copied onto the disk.
  Upload the images you need from the admin after deployment or copy them to
  `/var/data/media` using the Render Shell.
- Static files are rebuilt on each deploy and served by WhiteNoise; do not put
  user uploads in `static/`.
- If you later use multiple web instances or need a CDN, move uploads to shared
  object storage. A local persistent disk is attached to one service instance.

## Troubleshooting

- **DisallowedHost**: ensure the public hostname is Render's
  `RENDER_EXTERNAL_HOSTNAME`, or add your custom domain to `DJANGO_ALLOWED_HOSTS`.
- **CSRF verification failed**: add the exact `https://` custom-domain origin to
  `DJANGO_CSRF_TRUSTED_ORIGINS`; redeploy and use HTTPS.
- **Static files return 404**: inspect the build log for `collectstatic`
  failures and confirm WhiteNoise middleware is enabled.
- **Database connection or migration failure**: check that `DATABASE_URL` is
  linked to the Blueprint database and inspect the database and pre-deploy
  logs. Never paste the connection URL into a public issue.
- **Uploaded images disappear**: confirm the disk is mounted at `/var/data`
  and `MEDIA_ROOT` is `/var/data/media`. Files written outside the disk can be
  lost on redeploy or restart.
- **App fails to start**: check the Render service logs for missing environment
  variables or Python import errors. `DJANGO_DEBUG=0` requires a non-default
  `DJANGO_SECRET_KEY`.

For local development, leave `DATABASE_URL` unset to use SQLite and run
`python manage.py runserver` as described in [README.md](README.md).
