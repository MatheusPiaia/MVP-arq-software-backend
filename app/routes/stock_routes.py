from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify
from app.services.stock_service import list_all_stock, add_stock_service, update_stock_service
from app.schemas.stock_schemas import StockListResponse, StockResponse, StockSchema, StockUpdateSchema, StockViewSchema, StockPath, StockFilterQuery
from app.schemas.error import ErrorSchema


stock_bp = APIBlueprint(
    name="stock",
    import_name=__name__,
    url_prefix="/stock"
)

stock_tag = Tag(
    name="Estoque",
    description="Listagem e manipulação do estoque"
)

@stock_bp.get("/", tags=[stock_tag],
              responses={"200": StockListResponse})
def get_all_stock(query: StockFilterQuery = StockFilterQuery()):
    response = list_all_stock(query)
    return jsonify(response.model_dump()), 200


@stock_bp.post("/", tags=[stock_tag],
               responses={"200": StockResponse, "404": ErrorSchema, "400": ErrorSchema})
def add_stock(form: StockSchema):
    '''Adiciona registro de um produto ao estoque manualmente
    '''

    stock_or_error = add_stock_service(form)

    # service retorna produto OU string de erro
    if isinstance(stock_or_error, str):
        # é erro
        error_msg = stock_or_error
        status = 409 if "mesmo nome" in error_msg else 400
        return jsonify({"message": error_msg}), status
    
    response = StockResponse.model_validate(stock_or_error).model_dump()
    return jsonify(response), 200


@stock_bp.patch("/<uuid:stock_id>", tags=[stock_tag],                
                responses={"200": StockViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_stock(path: StockPath, form: StockUpdateSchema):
    '''Atualiza um produto do estoque
    '''
    stock_id = path.stock_id
    stock_or_error = update_stock_service(stock_id, form)

    if isinstance(stock_or_error, str):
        return {"message": stock_or_error}, 404
    
    response = StockViewSchema.model_validate(stock_or_error).model_dump()
    return jsonify(response), 200