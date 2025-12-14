from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify
from app.services.costumer_service import add_customer_service, list_all_customers
from app.schemas.customer_schemas import CustomerSchema, CustomerResponse, CustomerListResponse
from app.schemas.error import ErrorSchema

customer_bp = APIBlueprint(
    name="customer",
    import_name=__name__,
    url_prefix="/customer"
)

customer_tag = Tag(
    name="Clientes",
    description="Listagem e manipulação dos clientes cadastrados"
)


@customer_bp.post("/", tags=[customer_tag],
                  responses={"200": CustomerResponse, "404": ErrorSchema, "400": ErrorSchema})
def add_customer(form: CustomerSchema):
    '''Adiciona cliente a base
    '''

    customer_or_error = add_customer_service(form)

    # service retorna dados do cliente ou string de erro
    if isinstance(customer_or_error, str):
        # é erro
        error_msg = customer_or_error
        status = 409 if "Cliente já possui" in error_msg else 400
        return jsonify({"message": error_msg}), status
   
    response = CustomerResponse.model_validate(customer_or_error).model_dump()
    return jsonify(response), 200


@customer_bp.get("/", tags=[customer_tag],
                 responses={"200": CustomerListResponse})
def get_all_customers():
    response = list_all_customers()
    return jsonify(response.model_dump()), 200