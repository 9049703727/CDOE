# CDOE WEB — Django migration

This repo contains the original static "Learner" site converted to a Django project.

## Quick start (development)

1. Create and activate a virtualenv (Windows):

   python -m venv venv
   .\venv\Scripts\activate

2. Install dependencies:

   pip install -r requirements.txt

3. Run migrations:

   python cdoe_site\manage.py migrate

4. Create a superuser to access the admin (optional):

   python cdoe_site\manage.py createsuperuser

5. Run the development server:

   python cdoe_site\manage.py runserver

6. Open http://127.0.0.1:8000/ in your browser.

## Notes

- The `main` app includes a `ContactForm` and a `Newsletter` subscription handler. Contact submissions use the console email backend by default (see `cdoe_site/settings.py`).
- Static assets are served from the top-level `assets/` folder via `STATICFILES_DIRS` in settings.
- The templates live in `templates/` and most pages were converted to extend `templates/base.html`.

## Next steps (suggested)

- All templates now use `{% static %}` and the runtime asset-fixer in `base.html` has been removed.
- Implement storage/back-end for newsletter subscribers or integrate with an external service.
- Harden email configuration for production.
