import pytest
from sqlmodel import Session, create_engine, SQLModel, select
from app.models.stock import Product, Inventory
from app.models.base_entities import Warehouse
from app.services.stock import StockService

# Setup in-memory sqlite for testing
engine = create_engine("sqlite://")
SQLModel.metadata.create_all(engine)

@pytest.fixture
def session():
    with Session(engine) as session:
        yield session

def test_process_movement_entry(session):
    # Setup
    warehouse = Warehouse(name="Main")
    session.add(warehouse)
    session.commit()
    
    product = Product(sku="ITEM1", name="Product 1")
    session.add(product)
    session.commit()
    
    # Action
    StockService.process_movement(session, product.id, warehouse.id, 15, "entry")
    
    # Assert
    inventory = session.exec(
        select(Inventory).where(Inventory.product_id == product.id, Inventory.warehouse_id == warehouse.id)
    ).first()
    assert inventory.quantity == 15

def test_process_movement_exit(session):
    # Setup
    warehouse = Warehouse(name="Main")
    session.add(warehouse)
    session.commit()
    
    product = Product(sku="ITEM2", name="Product 2")
    session.add(product)
    session.commit()
    
    # Initial stock
    StockService.process_movement(session, product.id, warehouse.id, 10, "entry")
    
    # Action
    StockService.process_movement(session, product.id, warehouse.id, 3, "exit")
    
    # Assert
    inventory = session.exec(
        select(Inventory).where(Inventory.product_id == product.id, Inventory.warehouse_id == warehouse.id)
    ).first()
    assert inventory.quantity == 7

def test_insufficient_stock(session):
    # Setup
    warehouse = Warehouse(name="Main")
    session.add(warehouse)
    session.commit()
    
    product = Product(sku="ITEM3", name="Product 3")
    session.add(product)
    session.commit()
    
    # Action & Assert
    with pytest.raises(ValueError, match="No stock entry found for this warehouse"):
        StockService.process_movement(session, product.id, warehouse.id, 10, "exit")
