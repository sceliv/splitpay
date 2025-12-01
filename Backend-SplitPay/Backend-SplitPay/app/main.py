from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app import models 
from app.routers import users, groups, expenses, settlements, compensation, auth

print("Creando tablas en MySQL si no existen...")
Base.metadata.create_all(bind=engine)
print("Tablas creadas.")


app = FastAPI(title="SplitPay API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(groups.router)
app.include_router(expenses.router)
app.include_router(settlements.router)
app.include_router(compensation.router)


@app.get("/")
def root():
    return {"msg": "SplitPay Backend OK"}
