from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

from app import create_app
from app.config.config import config
from app.db.database import create_db_and_tables
from app.data.models import User 

create_db_and_tables()

app = create_app()

templates = Jinja2Templates(directory="static")


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == '__main__':
    import uvicorn

    if config.ENVIRONMENT == "dev":
        uvicorn.run("main:app", reload=True, port=int(config.SERVER_PORT), host=config.SERVER_HOST)

    else:
        uvicorn.run("main:app", port=int(config.SERVER_PORT), host=config.SERVER_HOST)
