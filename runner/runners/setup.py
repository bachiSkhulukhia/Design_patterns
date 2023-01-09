from fastapi import FastAPI

from Core.Persistance.Database.database import add_starting_tables_in_database
from infra.controller.manager_api import manager_api
from infra.controller.shop_api import shop_api


def setup() -> FastAPI:
    add_starting_tables_in_database()
    app = FastAPI()
    app.include_router(shop_api)
    app.include_router(manager_api)
    return app
