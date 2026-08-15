# HR Dashboard App

A Django-based HR management application.

## Prerequisites
- Python 3.8+
- Virtual Environment (included as `venv/`)

## Getting Started
1. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
2. Change directory to the project root:
   - `cd root`
3. Run migrations:
   - `python manage.py migrate`
4. Start the development server:
   - `python manage.py runserver`

## Docker development

```bash
docker compose up -d
```

The project directory is mounted into the `web` container. Saved Python files
trigger Django's development-server reload; saved templates and static files are
available immediately after refreshing the browser.

## Project Structure
- `root/`: Main Django project folder
  - `core_module/`: Core HR logic and components
  - `main/`: Main application dashboards and features
  - `operation/`: Operational tasks and workflows
  - `talent_growth/`: Employee development and growth tracking
  - `root/`: Project-wide settings and URLs
- `venv/`: Project virtual environment
