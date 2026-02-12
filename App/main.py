from .routers import auth
from fastapi import FastAPI
from .database import engine, Base

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

app.include_router(auth.router)

@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    templates = Jinja2Templates(directory="templates")
    app.mount("/static", StaticFiles(directory="static"), name="static")