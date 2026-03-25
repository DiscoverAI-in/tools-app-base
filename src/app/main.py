"""
FastAPI multi-app starter.

Each "app" is a folder under static/apps/<app-slug>/index.html.
Visit /<app-slug> to load it. The API lives under /api/v1/*.
"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1 import health
from app.config import get_settings

settings = get_settings()

# ── App ──────────────────────────────────────────────────────────────────────

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)

# ── Middleware ────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static files ─────────────────────────────────────────────────────────────

STATIC_DIR = Path(__file__).parent / "static"
APPS_DIR = STATIC_DIR / "apps"

# Serve /static/* for shared CSS, JS, images
app.mount("/static", StaticFiles(directory=STATIC_DIR / "shared"), name="static")

# ── API routes ───────────────────────────────────────────────────────────────

app.include_router(health.router, prefix="/api/v1")

# ── App page routes ──────────────────────────────────────────────────────────


def _resolve_app(app_slug: str) -> Path | None:
    """Safely resolve an app's index.html, preventing path traversal."""
    candidate = (APPS_DIR / app_slug / "index.html").resolve()
    if candidate.is_file() and str(candidate).startswith(str(APPS_DIR.resolve())):
        return candidate
    return None


@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the home page."""
    index = APPS_DIR / "home" / "index.html"
    return FileResponse(index)


@app.get("/{app_slug}", response_class=HTMLResponse)
async def serve_app(request: Request, app_slug: str):
    """
    Serve any registered app by its slug.
    e.g. /source-to-final  →  static/apps/source-to-final/index.html
    """
    page = _resolve_app(app_slug)
    if page is None:
        return HTMLResponse(
            content="<h1>404 — App not found</h1>",
            status_code=404,
        )
    return FileResponse(page)


# ── Sub-paths within apps (e.g. /my-app/settings) ───────────────────────────


@app.get("/{app_slug}/{rest:path}", response_class=HTMLResponse)
async def serve_app_subpath(request: Request, app_slug: str, rest: str):
    """
    SPA-style catch-all: any sub-path under an app slug
    still serves the app's index.html (Vue Router handles the rest).
    """
    page = _resolve_app(app_slug)
    if page is None:
        return HTMLResponse(
            content="<h1>404 — App not found</h1>",
            status_code=404,
        )
    return FileResponse(page)
