import pandas as pd
from sqlmodel import Session, select
from app.models.stock import Product, StockMovement, Inventory


class AnalyticsService:
    @staticmethod
    def get_stock_turnover_report(db: Session):
        movements = db.exec(select(StockMovement)).all()
        products = db.exec(select(Product)).all()
        
        if not movements:
            return []

        df_movements = pd.DataFrame([m.model_dump() for m in movements])
        df_products = pd.DataFrame([p.model_dump() for p in products])
        
        exits = df_movements[df_movements["type"] == "exit"].groupby("product_id")["quantity"].sum()
        entries = df_movements[df_movements["type"] == "entry"].groupby("product_id")["quantity"].sum()
        
        report = pd.merge(df_products, exits.rename("total_exits"), left_on="id", right_index=True, how="left").fillna(0)
        report = pd.merge(report, entries.rename("total_entries"), left_on="id", right_index=True, how="left").fillna(0)
        
        return report.to_dict(orient="records")

    @staticmethod
    def get_low_stock_summary(db: Session):
        # Join Product and Inventory to find low stock per warehouse
        results = db.exec(
            select(Product, Inventory)
            .join(Inventory)
            .where(Inventory.quantity <= Product.min_stock_level)
        ).all()
        
        data = []
        for product, inventory in results:
            item = product.model_dump()
            item["current_stock"] = inventory.quantity
            item["warehouse_id"] = inventory.warehouse_id
            data.append(item)
            
        return data
    
    @staticmethod
    def get_warehouse_utilization(db: Session):
        inventory = db.exec(select(Inventory)).all()
        if not inventory:
            return []
            
        df = pd.DataFrame([i.model_dump() for i in inventory])
        
        utilization = df.groupby("warehouse_id").agg({
            "product_id": "count",
            "quantity": "sum"
        }).rename(columns={"product_id": "unique_products", "quantity": "total_items"})
        
        return utilization.reset_index().to_dict(orient="records")
