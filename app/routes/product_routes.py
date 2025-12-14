from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify

from app.services.fakestore_service import fetch_products_from_fakestore
from app.services.product_service import import_products_from_api, add_product_service, del_product_service
from app.schemas.product_schemas import ProductSchema, ProductResponse, ProductDelSchema, ProductDeleteRequest, ProductListResponse, ProductViewSchema
from app.schemas.error import ErrorSchema

product_bp = APIBlueprint(
    name="products",
    import_name=__name__,
    url_prefix="/products"
)

product_tag = Tag(
    name="Produtos",
    description="Importação e listagem de produtos vindos da Fake Store API"
)

@product_bp.get("/sync", tags=[product_tag],
                responses={"200": ProductListResponse})
def sync_produtos():
    products = fetch_products_from_fakestore()
    imported_products = import_products_from_api(products)
    
    response = ProductListResponse(
        items=[
            ProductViewSchema(
                name=p.name,
                description=p.description,
                category=p.category,
                image_url=p.image_url,
                price=p.price   
            )
            for p in imported_products
        ]
    )
    return jsonify(response.model_dump()), 200


@product_bp.post("", tags=[product_tag],
                 responses={"200": ProductResponse, "409": ErrorSchema, "400": ErrorSchema})
def add_product(form: ProductSchema):
    '''Add um novo produto a base
    '''
    product_or_error = add_product_service(form)

    # service retorna produto OU string de erro
    if isinstance(product_or_error, str):
        # é erro
        error_msg = product_or_error
        status = 409 if "mesmo nome" in error_msg else 400
        return jsonify({"message": error_msg}), status

    # retorna produto
    response = ProductResponse.model_validate(product_or_error).model_dump()
    return jsonify(response), 200


@product_bp.delete("", tags=[product_tag],
                   responses={"200": ProductDelSchema, "400": ErrorSchema, "404": ErrorSchema})
def del_product(form: ProductDeleteRequest):

    product, error = del_product_service(form)

    if error:
        status = 404 if "não encontrado" in error.lower() else 400
        return {"message": error}, status
    
    # sucesso ao deletar, converter para o formato ProductDelSchema
    response = ProductDelSchema.model_validate(product).model_dump()
    return jsonify(response), 200