# FastAPI Apps

Multi-app platform — FastAPI serves APIs and static HTML pages powered by Vue 3 (CDN).

Each "app" is a self-contained folder with its own `index.html`. No build step required.

## Quick Start

```bash
# Install dependencies
uv sync

# Run dev server (auto-reload)
uv run uvicorn app.main:app --reload --app-dir src

# Or with Docker
docker compose up --build
```

Visit [http://localhost:8000](http://localhost:8000)

## Project Structure

```
fastapi-apps/
├── src/app/
│   ├── main.py                  # FastAPI app — routing & static serving
│   ├── config.py                # pydantic-settings (.env config)
│   ├── api/v1/                  # API route modules
│   │   └── health.py
│   └── static/
│       ├── shared/              # Shared assets across all apps
│       │   ├── css/base.css     # Theme variables & utility classes
│       │   └── js/api.js        # Fetch wrapper for API calls
│       └── apps/                # ← Each subfolder = one app
│           ├── home/index.html
│           └── source-to-final/index.html
├── tests/
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── .env
└── .env.example
```

## Adding a New App

**1. Create the folder and page:**

```bash
mkdir -p src/app/static/apps/my-new-app
```

Create `src/app/static/apps/my-new-app/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>My New App</title>
  <link rel="stylesheet" href="/static/css/base.css" />
</head>
<body>
<div id="app" class="container">
  <nav>
    <a href="/">← Home</a>
    <span style="color: var(--color-text-muted)">|</span>
    <strong>My New App</strong>
  </nav>

  <div class="card">
    <h2>{{ message }}</h2>
  </div>
</div>

<script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>
<script src="/static/js/api.js"></script>
<script>
const { createApp, ref } = Vue;

createApp({
  setup() {
    const message = ref('Hello from My New App!');
    return { message };
  },
}).mount('#app');
</script>
</body>
</html>
```

**2. Register it on the home page** (optional but recommended):

Edit `src/app/static/apps/home/index.html` and add to the `apps` array:

```js
{ slug: 'my-new-app', name: 'My New App', icon: '✨', description: 'Does something cool.' },
```

**3. Add API routes** (if the app needs a backend):

Create `src/app/api/v1/my_new_app.py`:

```python
from fastapi import APIRouter

router = APIRouter(prefix="/my-new-app", tags=["my-new-app"])

@router.post("/process")
async def process(payload: dict):
    return {"result": "done", "input": payload}
```

Register in `main.py`:

```python
from app.api.v1 import my_new_app
app.include_router(my_new_app.router, prefix="/api/v1")
```

That's it — visit `/my-new-app` and it works.

## URL Routing

| URL                     | What it serves                          |
|-------------------------|-----------------------------------------|
| `/`                     | Home page (app listing)                 |
| `/source-to-final`     | source-to-final app                     |
| `/my-app/sub/path`     | SPA catch-all → my-app's `index.html`  |
| `/static/css/base.css` | Shared static assets                    |
| `/api/v1/health`       | API health check                        |
| `/api/docs`            | Swagger UI (DEBUG=true only)            |

## Shared Resources

All apps share:

- **`/static/css/base.css`** — Dark theme, CSS variables, `.card`, `.btn`, `.container`
- **`/static/js/api.js`** — `api.get()`, `api.post()`, `api.put()`, `api.del()` helpers

## Commands

```bash
# Dev server
uv run uvicorn app.main:app --reload --app-dir src

# Run tests
uv run pytest

# Lint
uv run ruff check src/

# Docker
docker compose up --build
docker compose down
```

## Environment Variables

| Variable       | Default         | Description                   |
|---------------|-----------------|-------------------------------|
| `APP_NAME`    | FastAPI Apps    | App title                     |
| `APP_VERSION` | 0.1.0           | Shown in health check         |
| `DEBUG`       | false           | Enables /api/docs & /api/redoc|
| `HOST`        | 0.0.0.0         | Bind address                  |
| `PORT`        | 8000            | Bind port                     |
| `CORS_ORIGINS`| *               | Comma-separated allowed origins|
