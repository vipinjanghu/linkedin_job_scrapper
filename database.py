import pymongo
from constant import cluster_pass

def to_database(search_job,document):
    client = pymongo.MongoClient(f"mongodb+srv://vipinjanghu:{cluster_pass}@cluster0.2rskres.mongodb.net/?retryWrites=true&w=majority")
    db = client["scrapper"]
    try:
        db.validate_collection(search_job)  # Try to validate a collection
        coll=db[search_job]
    except pymongo.errors.OperationFailure:  # If the collection doesn't exist
        coll=db[search_job]
    coll.insert_many(document)
