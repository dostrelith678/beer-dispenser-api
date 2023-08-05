from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = "/api/docs"
API_URL = "/docs/api.spec.yaml"

bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Beer dispenser API",
    },
)
