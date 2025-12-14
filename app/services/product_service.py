from app.models.api_products_cache import ApiProductsCache
from app.models.product import Product
from app.models.product_stock import ProductStock
from sqlalchemy.exc import IntegrityError
from app import db
from uuid import uuid4
from app.logger import logger


def import_products_from_api(products):

    list_products = []

    for item in products:
        api_id = item["id"]

        cache = ApiProductsCache.query.filter_by(api_id=api_id).first()
        if not cache:
            cache = ApiProductsCache(
                api_id=api_id,
                raw_json=item
            )
            db.session.add(cache)
        else:
            cache.raw_json = item

        product = Product.query.filter_by(api_id=api_id).first()

        if not product:
            product = Product(
                id=uuid4(),
                api_id=api_id,
                name=item["title"],
                description=item["description"],
                category=item["category"],
                image_url=item["image"],
                price=item["price"]
            )
            db.session.add(product)
            db.session.flush()            

            add_default_stock(product.id)
        else:
            product.name = item["title"]
            product.description = item["description"]
            product.category = item["category"]
            product.image_url = item["image"]
            product.price = item["price"]

            ensure_default_stock(product.id)
        
        list_products.append(product)

    db.session.commit()
    return list_products

def add_default_stock(product_id):
    '''Add registro de estoque ao importa da fakestore
    '''
    existing_stock = ProductStock.query.filter_by(
        product_id=product_id,
        size="UN",
        color="UN"
    ).first()

    if not existing_stock:

        default_stock = ProductStock(
            product_id=product_id,
            size="UN",
            color="UN",
            quantity_available=0,
            quantity_reserved=0
        )
    db.session.add(default_stock) 
    logger.info("Adicionado registros de estoque")


def ensure_default_stock(product_id):
    """Garante que exista estoque UN/UN para produtos já existentes."""
    existing_stock = ProductStock.query.filter_by(
        product_id=product_id,
        size="UN",
        color="UN"
    ).first()

    if not existing_stock:
        add_default_stock(product_id)

def add_product_service(data):
    '''Add um novo produto a base
    '''
    product = Product(
        name=data.name,
        description=data.description,
        category=data.category,
        image_url=data.image_url,
        price=data.price
    )
    
    logger.info(f"Adicionando produto de nome: '{product.name}'")
    try:        
        # adicionando produto
        db.session.add(product)
        # efetivando o camando de adição de novo item na tabela
        db.session.commit()
        logger.info("Adicionado produto, criando registros de estoque...")

        sizes = ["PP", "P", "M", "G", "GG"]

        for size in sizes:
            stock = ProductStock(
                product_id=product.id,
                size=size,
                color="UN",
                quantity_available=0,
                quantity_reserved=0
            )
            db.session.add(stock)
        
        db.session.commit()
        logger.info("Adicionado registros de estoque")

        return product

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        db.session.rollback()
        error_msg = "Produto de mesmo nome e marca já salvo na base :/"
        logger.warning(f"Erro ao adicionar produto '{product.name}', {error_msg}")
        return error_msg

    except Exception as e:
        # caso um erro fora do previsto
        db.session.rollback()
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar produto '{product.name}', {error_msg}")
        return error_msg

def del_product_service(data):
    '''Deleta um produto a partir do id
    '''
    product_id = data.id
    logger.info(f"Deletando dados sobre o produto #{product_id}")

    product = Product.query.get(product_id)
    
    if not product:
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao deletar produto #'{product_id}', {error_msg}")
        return None, error_msg

    try:
        #Confirma que tem o produto na base e remove
        db.session.delete(product)
        db.session.commit()

        logger.info(f"Produto removido: {product.name}")
        return product, None
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao deletar: {e}")
        return None, "Não foi possível remover o produto"