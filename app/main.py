from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from .rest import hespress

app = FastAPI()
app.include_router(hespress.router, prefix="/hespress", tags=["Hespress"])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Hespress scraper",
        version="1.0.0",
        description="This is a api doc for endpoint of hespress scraper",
        routes=app.routes,
        openapi_version="3.0.0"
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://i1.hespress.com/wp-content/uploads/2021/09/schema_publisher_logo.jpg"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
