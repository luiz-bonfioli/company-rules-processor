from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware

from src.controllers import company_controller, health_controller
from src.core.context import get_database

app = FastAPI()
app.add_middleware(GZipMiddleware)

# Controllers setup
app.include_router(health_controller.router)
app.include_router(company_controller.router)


async def create_db():
    db = get_database()
    db.create_db()


@app.on_event("startup")
async def startup():
    await create_db()
