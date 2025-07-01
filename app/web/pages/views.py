from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


page_route = APIRouter()

templates = Jinja2Templates(directory="templates")


@page_route.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@page_route.get("/registration", response_class=HTMLResponse)
async def registration(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@page_route.get("/dashboard", response_class=HTMLResponse)
async def registration(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})