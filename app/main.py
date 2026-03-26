from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import admin, auth, clubs, events, initiatives, mobile_auth, panel, search

app = FastAPI(title="Kozmin Daily API", version="1.0.0")

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router)
app.include_router(clubs.router)
app.include_router(initiatives.router)
app.include_router(auth.router)
app.include_router(panel.router)
app.include_router(admin.router)
app.include_router(search.router)
app.include_router(mobile_auth.router)


@app.get("/")
async def root():
    return {"message": "Kozmin Daily API", "docs": "/docs"}
