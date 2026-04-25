from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.firebase import init_firebase
from app.routers import academic_calendar, admin, auth, clubs, config, discounts, events, mobile_auth, news, panel, search

app = FastAPI(
    title="Kozmin Daily API",
    version="1.0.0",
    docs_url=None if settings.DISABLE_DOCS else "/docs",
    redoc_url=None if settings.DISABLE_DOCS else "/redoc",
    openapi_url=None if settings.DISABLE_DOCS else "/openapi.json",
)

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
allow_all = origins == ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=not allow_all,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_firebase()

app.include_router(events.router)
app.include_router(clubs.router)
app.include_router(auth.router)
app.include_router(panel.router)
app.include_router(admin.router)
app.include_router(search.router)
app.include_router(mobile_auth.router)
app.include_router(news.router)
app.include_router(config.router)
app.include_router(academic_calendar.router)
app.include_router(discounts.router)


@app.get("/")
async def root():
    return {"message": "Kozmin Daily API"}
