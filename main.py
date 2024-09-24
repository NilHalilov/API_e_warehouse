from contextlib import asynccontextmanager

# import uvicorn
from fastapi import FastAPI

from models import Base, e_store_db
from api_v1__warehouse.products.views import router as products_router
from api_v1__warehouse.orders.views import router as orders_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with e_store_db.engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(products_router)
app.include_router(orders_router)


# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)
