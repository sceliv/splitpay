import os
from typing import List


class Settings:
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "sugar123")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "splitpay")

    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    # Orígenes permitidos para CORS, separados por comas.
    # Ejemplo: "http://localhost:8000,http://127.0.0.1:5500"
    _origins = os.getenv("FRONTEND_ORIGINS", "").strip()

    @property
    def CORS_ORIGINS(self) -> List[str]:
        if not self._origins:
            # Para desarrollo, permitimos cualquier origen.
            # En producción, configura FRONTEND_ORIGINS con las URLs permitidas.
            return ["*"]
        return [origin.strip() for origin in self._origins.split(",") if origin.strip()]

    # --- Seguridad / JWT ---
    SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_IN_PRODUCTION")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


settings = Settings()
