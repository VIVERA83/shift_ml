from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.lifespan import store
from web.pages.utils import days_since

page_route = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@page_route.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@page_route.get("/registration", response_class=HTMLResponse)
async def registration(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@page_route.get("/dashboard", response_class=HTMLResponse)
async def registration(request: Request):
    user = await store.accessor.user.get_by_id(int(request.state.user_id))
    salary = await store.accessor.salary.get_current_salary(int(request.state.user_id))
    next_update = await store.accessor.salary.get_next_date_change(
        int(request.state.user_id)
    )
    salary = salary.salary if salary else "данные отсутствуют"
    next_update = next_update.date if next_update else "данные отсутствуют"

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "work_experience": days_since(user.created_at),
            "salary": salary,
            "next_update": next_update,
        },
    )
