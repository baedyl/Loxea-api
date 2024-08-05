from fastapi import APIRouter, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/bo")
templates = Jinja2Templates(directory="app/templates")


class MockService:
    def login(self, email: str, password: str) -> dict:
        return {"name": "Kinason", "email": email, "id": 1}

service = MockService()


@router.get("/dashboard", name="dashboard")
async def dashboard(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(request.url_for("login"))
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})


@router.get("/login", name="login")
async def login_page(request: Request):
    if request.session.get("user"):
        return RedirectResponse(request.url_for("dashboard"))
    return templates.TemplateResponse("login.html", {"request": request})


@router.post('/login')
async def login(request: Request, email: str = Form(), password: str = Form()):
    user = service.login(email, password)
    if user:
        request.session["user"] = user
        return RedirectResponse(request.url_for("dashboard"), status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(request.url_for("login"))