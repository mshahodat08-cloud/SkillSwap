from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models  # noqa: F401  (jadvallar yaratilishi uchun kerak)
from .database import Base, engine
from .routers import skills, stats, swaps, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="SkillSwap API", version="1.0.0", lifespan=lifespan)

# Faqat rivojlanish uchun. Saytni joylagach "*" o'rniga o'z domeningizni yozing.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(skills.router)
app.include_router(swaps.router)
app.include_router(stats.router)


@app.get("/", tags=["Umumiy"])
def root():
    return {"app": "SkillSwap API", "docs": "/docs"}
