from fastapi.templating import Jinja2Templates
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse

page_route = APIRouter()

templates = Jinja2Templates(directory="templates")


@page_route.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
