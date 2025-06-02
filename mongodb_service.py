from ..mongodb_utils import get_database

class ProductAnalyticsService:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.product_analytics
    
    def record_product_view(self, product_id, user_id=None):
        """Record a product view event"""
        doc = {
            "product_id": str(product_id),
            "timestamp": datetime.datetime.now(),
            "event_type": "view"
        }
        if user_id:
            doc["user_id"] = str(user_id)
        
        return self.collection.insert_one(doc)
    
    def get_popular_products(self, limit=10):
        """Get most viewed products"""
        pipeline = [
            {"$match": {"event_type": "view"}},
            {"$group": {"_id": "$product_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]
        return list(self.collection.aggregate(pipeline))