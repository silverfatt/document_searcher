from fastapi import FastAPI

from app.routes import router
from app.database import prepare_db, DB_URL

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    prepare_db()


app.include_router(router)


@app.on_event("shutdown")
def shutdown_event():
    pass
