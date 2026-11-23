# uv run uvicorn main:app --reload

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import models
from database import Base, engine
from routers import plants, users, nodes, readings

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(plants.router)
app.include_router(users.router)
app.include_router(nodes.router)
app.include_router(readings.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", include_in_schema=False, name="home")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"title": "Plant Soil Level"}
    )
