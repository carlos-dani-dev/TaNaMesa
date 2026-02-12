from .routers import auth
from fastapi import FastAPI

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

app.include_router(auth.router)

@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}