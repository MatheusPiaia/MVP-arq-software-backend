from flask import redirect
from flask_openapi3 import Tag, APIBlueprint

main_bp = APIBlueprint(
    name="main",
    import_name=__name__,
    )


home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")

@main_bp.get("/", tags=[home_tag])
def index():
    # Redireciona para a página do Swagger (OpenAPI)
    return redirect("/openapi")
