from app.models.customer import Customer
from app.schemas.customer_schemas import CustomerListResponse, CustomerViewSchema
from app import db
from uuid import uuid4
from app.logger import logger
from sqlalchemy.exc import IntegrityError


def add_customer_service(data):
    '''Adiciona um cliente a base
    '''   
    existing_customer = Customer.query.filter_by(
        name=data.name
    ).first()

    if not existing_customer:
        customer = Customer(
            name=data.name,
            phone=data.phone,
            address=data.address
        )
        logger.info(f"Adicionando a base cliente de nome: {customer.name}")
        try:
            # adicionando cliente a base
            db.session.add(customer)
            # efetivando a adição a base
            db.session.commit()
            logger.info(f"Adicionado a base cliente: {customer.name}")
            return customer
        except Exception:
            db.session.rollback()
            error_msg = "Não foi possível salvar cliente"
            logger.warning("Erro ao adicionar cliente")
            return error_msg

    error_msg = "Cliente já possui cadastro"
    logger.warning("Erro ao adicionar cliente")
    return error_msg


def list_all_customers():
    '''Retorna todos os clientes cadastrados
    '''

    customers = Customer.query.all()

    result = [
        CustomerViewSchema.model_validate(customer)
        for customer in customers
    ]

    return CustomerListResponse(items=result)