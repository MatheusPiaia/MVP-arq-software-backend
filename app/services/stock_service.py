from app.models.product_stock import ProductStock
from app.models.product import Product
from app.schemas.stock_schemas import StockListResponse, StockViewSchema, StockSchema, StockResponse
from sqlalchemy.exc import IntegrityError
from app import db
from uuid import uuid4
from app.logger import logger


def add_stock_service(data):
    '''Adiciona um item ao estoque
    '''
    product_stock = ProductStock(
        product_id=data.product_id,
        size=data.size,
        color=data.color,
        quantity_available=data.quantity
    )
    logger.info(f"Adicionando ao estoque produto ID: '{product_stock.product_id}'")
    try:
        # adicionando produto ao estoque
        db.session.add(product_stock)
        # efetivando o comando de adição do item ao estoque
        db.session.commit()
        logger.info(f"Adicionado ao estoque produto: {product_stock} ")
        return product_stock
    
    except IntegrityError:
        db.session.rollback()
        error_msg = "Produto já possui posição no estoque"
        logger.warning(f"Erro ao adicionar ao estoque")
        return error_msg
    
    except Exception:
        db.session.rollback()
        error_msg = "Não foi possível salvar produto no estoque"
        logger.warning(f"Erro ao adicionar ao estoque")
        return error_msg


def list_all_stock(filters=None):
    '''Retorna todos os produtos do estoque e também com filtros
    '''
    query = (
        db.session.query(ProductStock)
        .join(Product)
    )

    if filters:
        if filters.size:
            query = query.filter(ProductStock.size == filters.size)

        if filters.category:
            query = query.filter(Product.category == filters.category)

        if filters.brand:
            query = query.filter(Product.brand == filters.brand)

        if filters.reference:
            query = query.filter(
                Product.reference.ilike(f"%{filters.reference}%")
            )

    stocks = query.all()

    result = [
        StockViewSchema.model_validate(stock)
        for stock in stocks
    ]

    return StockListResponse(items=result)


def update_stock_service(stock_id, data):
    '''Atualiza um produto do estoque'''

    stock = ProductStock.query.get(stock_id)

    if not stock:
        return "Item de estoque não encontrado"
    
    try:
        if data.quantity_available is not None:
            stock.quantity_available = data.quantity_available
        
        if data.quantity_reserved is not None:
            stock.quantity_reserved = data.quantity_reserved

        db.session.commit()

        logger.info(f"Estoque atualizado: {stock_id}")
        return stock
    
    except Exception as e:
        logger.error(f"Erro ao atualizar estoque {stock_id}: {e}")
        db.session.rollback()
        return "Erro ao atualizar estoque"


def reserve_stock_service(stock_id, quantity):
    '''Atualiza a quantidade de itens reservados do estoque
    '''

    stock = ProductStock.query.get(stock_id)

    if not stock:
        return "Item de estoque não encontrado"
    
    if quantity <= 0:
        return "Quantidade inválida"

    if quantity > stock.quantity_real:
        return "Quantidade insuficiente no estoque"

    try:  
        stock.quantity_reserved += quantity
        db.session.commit()

        logger.info(
            f"Reservado {quantity} do estoque {stock_id} | "
            f"Disponível real: {stock.quantity_real}"
        )
        return stock
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao reservar estoque {stock_id}: {e}")
        return "Erro ao reservar estoque"