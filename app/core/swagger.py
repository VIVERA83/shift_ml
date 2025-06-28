from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def setup_openapi(app: FastAPI):
    openapi_schema = get_openapi(
        title="My Custom API",
        version="1.0.0",
        description="This is a highly customized API documentation",
        routes=app.routes,
    )

    openapi_schema["info"]["contact"] = {
        "name": "Support Team",
        "email": "support@company.com",
        "url": "http://0.0.0.0:8006"
    }

    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter JWT token in format: **Bearer <token>**"
        }
    }

    for path, methods in openapi_schema["paths"].items():
        for method, operation in methods.items():
            if path not in ["/auth/login", "auth/registration"]:
                operation.setdefault("security", [])
                operation["security"].append({"OAuth2PasswordBearer": []})

    hidden_paths = ["/"]
    for path in hidden_paths:
        if path in openapi_schema["paths"]:
            del openapi_schema["paths"][path]

    app.openapi_schema = openapi_schema
