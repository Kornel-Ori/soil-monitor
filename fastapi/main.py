# uv run uvicorn main:app --reload
# ads1115 library: uv add adafruit-circuitpython-ads1x15

from fastapi import FastAPI, Request, Form, Depends
from fastapi import FastAPI, Depends, HTTPException, status, Request


from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from auth import verify_password, create_access_token, JWT_EXPIRE_MINUTES

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


@app.get("/", include_in_schema=False)
def login_page(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {"hide_navigation": True}
    )


@app.get("/home", include_in_schema=False, name="home")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"title": "Plant Soil Level"}
    )


@app.post("/login", include_in_schema=False)
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(models.User).where(models.User.email == email)
    )
    user = result.scalar_one_or_none()

    if user is None or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "hide_navigation": True,
                "error": "Incorrect email or password."
            },
            status_code=401
        )

    token = create_access_token(user.id)

    response = RedirectResponse("/home", status_code=303)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=JWT_EXPIRE_MINUTES * 60
    )

    return response


@app.get("/about", include_in_schema=False)
def about(request: Request):
    return templates.TemplateResponse(
        request,
        "about.html"
    )