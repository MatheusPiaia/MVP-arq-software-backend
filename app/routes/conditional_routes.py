from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify, request
from app.schemas.conditional_schemas import ConditionalViewSchema, ConditionalSchema, ConditionalListResponse, ConditionalItemListResponse, ConditionalPath, ConditionalStatusResponse
from app.schemas.conditional_items_schemas import ConditionalItemSchema, ConditionalItemViewSchema, ConditionalItemDeleteResponse, ConditionalItemPath, ConditionalItemReturn, ConditionalReturnForm
from app.schemas.error import ErrorSchema
from app.services.conditional_service import (
    get_conditional_service,
    add_item_service,
    create_conditional_service,
    list_conditional_service,
    close_conditional_service,
    delete_item_service,
    return_conditional_service
)

conditional_bp = APIBlueprint(
    name="conditional",
    import_name=__name__,
    url_prefix="/conditional"
)

conditional_tag = Tag(
    name="Condicionais",
    description="Operações de consulta e manipulação de condicionais"
)

@conditional_bp.get("/<uuid:conditional_id>", tags=[conditional_tag],
                    responses={"200": ConditionalViewSchema, "404": ErrorSchema})
def get_conditional(path: ConditionalPath):
    conditional_id = path.conditional_id
    conditional_or_error = get_conditional_service(conditional_id)

    if isinstance(conditional_or_error, str):
        return jsonify({"message": conditional_or_error}), 404
    
    response = ConditionalViewSchema.model_validate(conditional_or_error).model_dump()

    return jsonify(response), 200

'''
@conditional_bp.get("/", tags=[conditional_tag],
                    responses={"200": ConditionalListResponse})
def list_conditionals():
    response = list_conditional_service()  
    return jsonify(response.model_dump()), 200
'''


@conditional_bp.get("/", tags=[conditional_tag],
                    responses={"200": ConditionalListResponse})
def list_conditionals():
    # lê o query param 'status' da URL, ex: /conditional/?status=open
    status_filter = request.args.get("status")

    response = list_conditional_service(status_filter)
    return jsonify(response.model_dump()), 200


@conditional_bp.post("/", tags=[conditional_tag],
                     responses={"200": ConditionalViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def create_conditional(form: ConditionalSchema):
    conditional_or_error = create_conditional_service(form)

    if isinstance(conditional_or_error, str):
        # é erro
        error_msg = conditional_or_error
        status = 409 if "aberto para esse cliente" in error_msg else 400
        return jsonify({"message": error_msg}), status
    
    response = ConditionalViewSchema.model_validate(conditional_or_error).model_dump()
    return jsonify(response), 200


@conditional_bp.post("/item", tags=[conditional_tag],
                     responses={"200": ConditionalItemViewSchema, "400": ErrorSchema})
def add_item(form: ConditionalItemSchema):
    item_or_error = add_item_service(form)

    if isinstance(item_or_error, str):
        return jsonify({"message": item_or_error}), 400

    response = ConditionalItemViewSchema.model_validate(item_or_error).model_dump()
    return jsonify(response), 200


@conditional_bp.delete("/item/<uuid:item_id>", tags=[conditional_tag],
                       responses={"200": ConditionalItemDeleteResponse, "404": ErrorSchema})
def delete_item(path: ConditionalItemPath):
    result = delete_item_service(path.item_id)

    if isinstance(result, str):
        return jsonify({"message": result}), 404

    return jsonify({"message": "Item removido com sucesso"}), 200


@conditional_bp.post(
    "/<uuid:conditional_id>/close",
    tags=[conditional_tag],
    responses={"200": ConditionalStatusResponse, "400": ErrorSchema}
)
def close_conditional(path: ConditionalPath):
    conditional_id = path.conditional_id
    result = close_conditional_service(conditional_id)

    if isinstance(result, str):
        return jsonify({"message": result}), 400

    return jsonify({"status": "closed"}), 200


@conditional_bp.post(
    "/<uuid:conditional_id>/returned",
    tags=[conditional_tag],
    responses={"200": ConditionalStatusResponse, "400": ErrorSchema}
)
def return_conditional(path: ConditionalPath, body: ConditionalReturnForm):
    conditional_id = path.conditional_id
    result = return_conditional_service(conditional_id, body.items)

    if isinstance(result, str):
        return jsonify({"message": result}), 400
    
    return jsonify({"status": "returned"}), 200
