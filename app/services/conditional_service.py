from app.models.conditional import Conditional
from app import db
from app.models.conditional_item import ConditionalItem
from app.models.product_stock import ProductStock
from app.schemas.conditional_schemas import ConditionalViewSchema, ConditionalListResponse
from app.schemas.conditional_items_schemas import ConditionalItemReturn
from app.services.stock_service import reserve_stock_service
from uuid import uuid4
from app.logger import logger
from datetime import datetime, timezone


def get_conditional_service(conditional_id):
    '''Retorna as informações de um condicional a partir do id
    '''
    conditional = (
        db.session.query(Conditional)
        .filter(Conditional.id == conditional_id)
        .first()
    )

    if not conditional:
        return "Condicional não encontrado"
    
    return conditional


def create_conditional_service(data):
    '''Cria um condicional
    '''

    cond = Conditional.query.filter_by(customer_id=data.customer_id, user_id=data.user_id, status="open").first()
    
    if cond:
        error_msg = "Já possui condicional aberto para esse cliente verificar"
        logger.warning(f"Erro ao cadastrar condicional")
        return error_msg
    
    try:
        conditional = Conditional(
            id=uuid4(),
            customer_id=data.customer_id,
            user_id=data.user_id,
            status=data.status
        )
        db.session.add(conditional)
        db.session.commit()
        return conditional
    
    except Exception:
        db.session.rollback()
        error_msg = "Não foi possível salvar condicional"
        logger.warning(f"Erro ao adicionar condicional")
        return error_msg


def add_item_service(data):
    '''
    Adiciona um item a um condicional e reserva estoque
    (operação transacional)
    '''

    try:
        #Para evitar concorrência
        stock = (
            db.session.query(ProductStock)
            .filter(ProductStock.id == data.product_stock_id)
            .with_for_update()
            .first()
        )

        if not stock:
            return "Estoque não encontrado"

        if data.quantity > stock.quantity_real:
            return (
                f"Estoque insuficiente. "
                f"Disponível: {stock.quantity_real}"
            )

        item = ConditionalItem(
            id=uuid4(),
            conditional_id=data.conditional_id,
            product_stock_id=data.product_stock_id,
            quantity=data.quantity,
            final_action=data.final_action
        )

        db.session.add(item)

        #reserva incremental
        stock.quantity_reserved += data.quantity

        db.session.commit()

        logger.info(
            f"Item {item.id} adicionado ao condicional "
            f"{data.conditional_id} | "
            f"Reservado {data.quantity} do estoque {stock.id}"
        )

        return item

    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao adicionar item ao condicional: {e}")
        return "Erro ao adicionar item ao condicional"


def list_conditional_service(status: str | None = None):
    '''Lista todos os condicionais ou filtra por status
    '''
    #conditionals = Conditional.query.all()
    query = db.session.query(Conditional)

    if status:
        query = query.filter(Conditional.status == status)

    conditionals = query.order_by(Conditional.created_at.desc()).all()  

    result = [
        ConditionalViewSchema.model_validate(conditional)
        for conditional in conditionals
    ]
    return ConditionalListResponse(items=result)


def close_conditional_service(conditional_id):
    '''Fecha um condicional
    '''
    cond = Conditional.query.filter_by(id=conditional_id).first()

    if not cond:
        return "Condicional não encontrado"

    if cond.status == "closed":
        return "Condicional já está fechado"

    cond.status = "closed"
    cond.closed_at = datetime.utcnow()

    db.session.commit()
    return cond


def delete_item_service(item_id):
    '''Deleta um item de um condicional e devolve estoque reservado
    '''
    item = (
        db.session.query(ConditionalItem)
        .filter(ConditionalItem.id == item_id)
        .first()
    )

    if not item:
        return "Item não encontrado"

    conditional = (
        db.session.query(Conditional)
        .filter(Conditional.id == item.conditional_id)
        .first()
    )

    if not conditional:
        return "Condicional não encontrado"

    if conditional.status == "closed":
        return "Não é possível remover itens de um condicional fechado"

    stock = (
        db.session.query(ProductStock)
        .filter(ProductStock.id == item.product_stock_id)
        .first()
    )

    if not stock:
        return "Estoque não encontrado"

    try:
        # devolve quantidade reservada
        stock.quantity_reserved -= item.quantity

        if stock.quantity_reserved < 0:
            stock.quantity_reserved = 0 

        db.session.delete(item)
        db.session.commit()

        logger.info(
            f"Item {item_id} removido e estoque atualizado (reserved devolvido)"
        )

        return True

    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao remover item {item_id}: {e}")
        return "Erro ao remover item do condicional"

    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao remover item do condicional: {e}")
        return "Erro ao remover item"
    
def close_conditional_service(conditional_id):
    conditional = (
        db.session.query(Conditional)
        .filter(Conditional.id == conditional_id)
        .first()
    )

    if not conditional:
        return "Condicional não encontrado"

    if conditional.status != "open":
        return "Apenas condicionais abertas podem ser fechadas"

    if not conditional.items:
        return "Não é possível fechar um condicional sem itens"

    try:
        conditional.status = "closed"
        conditional.closed_at = datetime.now(timezone.utc)
        db.session.commit()

        return True

    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao fechar condicional: {e}")
        return "Erro ao fechar condicional"


def return_conditional_service(conditional_id, items_data: list[ConditionalItemReturn]):
    conditional = (
        db.session.query(Conditional)
        .filter(Conditional.id == conditional_id)
        .first()
    )

    if not conditional:
        return "Condicional não encontrado"

    if conditional.status != "closed":
        return "Apenas condicionais fechadas podem ser devolvidas"

    try:
        for data in items_data:
            item = (
                db.session.query(ConditionalItem)
                .filter(ConditionalItem.id == data.item_id)
                .first()
            )

            if not item:
                return "Item inválido"

            stock = (
                db.session.query(ProductStock)
                .filter(ProductStock.id == item.product_stock_id)
                .first()
            )

            returned = data.returned_quantity
            total = item.quantity
            purchased = total - returned

            if returned < 0 or returned > total:
                return "Quantidade devolvida inválida"

            # devolvidos
            stock.quantity_reserved -= returned            

            # comprados
            stock.quantity_reserved -= purchased
            stock.quantity_available -= purchased

            # atualiza informação para o item
            item.returned_quantity = returned
            item.purchased_quantity = purchased

            if purchased > 0 and returned > 0:
                item.final_action = "partial"
            elif purchased > 0:
                item.final_action = "bought"
            else:
                item.final_action = "returned"           
        conditional.status = "returned"
        db.session.commit()

        return True

    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao devolver condicional: {e}")
        return "Erro ao processar devolução"