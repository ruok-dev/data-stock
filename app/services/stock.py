from sqlmodel import Session, select
from app.models.stock import Product, StockMovement, Inventory
from app.models.alert import Alert


class StockService:
    @staticmethod
    def process_movement(
        db: Session, 
        product_id: int, 
        warehouse_id: int, 
        quantity: int, 
        movement_type: str,
        user_id: int = None
    ):
        # 1. Get or Create Inventory entry for this product and warehouse
        inventory = db.exec(
            select(Inventory).where(
                Inventory.product_id == product_id,
                Inventory.warehouse_id == warehouse_id
            )
        ).first()
        
        if not inventory:
            if movement_type == "exit":
                raise ValueError("No stock entry found for this warehouse")
            inventory = Inventory(product_id=product_id, warehouse_id=warehouse_id, quantity=0)
            db.add(inventory)
        
        # 2. Update Stock
        if movement_type == "entry":
            inventory.quantity += quantity
        elif movement_type == "exit":
            if inventory.quantity < quantity:
                raise ValueError("Insufficient stock in this warehouse")
            inventory.quantity -= quantity
        
        db.add(inventory)
        
        # 3. Record Movement
        movement = StockMovement(
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity=quantity,
            type=movement_type,
            user_id=user_id
        )
        db.add(movement)
        
        # 4. Check for Alerts
        product = db.get(Product, product_id)
        if inventory.quantity == 0:
            alert = Alert(
                product_id=product_id,
                type="rupture",
                message=f"Product {product.sku} is out of stock in warehouse {warehouse_id}."
            )
            db.add(alert)
        elif inventory.quantity <= product.min_stock_level:
            alert = Alert(
                product_id=product_id,
                type="low_stock",
                message=f"Product {product.sku} has reached low stock level ({inventory.quantity}) in warehouse {warehouse_id}."
            )
            db.add(alert)
        
        db.commit()
        db.refresh(inventory)
        return inventory

    @staticmethod
    def get_inventory_by_warehouse(db: Session, warehouse_id: int):
        statement = select(Inventory).where(Inventory.warehouse_id == warehouse_id)
        return db.exec(statement).all()
