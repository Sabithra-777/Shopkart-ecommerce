from pymongo import MongoClient

def get_mongodb_client():
    """Returns a MongoDB client instance connected to Atlas"""
    connection_string = "mongodb+srv://sabithram:07072007@sabithracluster.qasbpv4.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(
        connection_string,
        ssl=True,
        ssl_cert_reqs='CERT_NONE'
    )
    return client

def get_database(db_name='django_sabi'):
    """Returns a MongoDB database instance"""
    client = get_mongodb_client()
    return client[db_name]




