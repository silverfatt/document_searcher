from fastapi import FastAPI

from app.routes import router
from app.database import prepare_db, DB_URL

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    try:
        prepare_db()
    except Exception:
        print("Wrong database info. Check DB_USER, DB_PASSWORD, DB_NAME and DB_HOST variables.")
        print(f"Current URL:{DB_URL}")
        exit(1)


app.include_router(router)


@app.on_event("shutdown")
def shutdown_event():
    pass
