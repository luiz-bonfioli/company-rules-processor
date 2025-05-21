from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware

from src.controllers import company_controller

app = FastAPI()
app.add_middleware(GZipMiddleware)

# Controllers setup
app.include_router(company_controller.router)