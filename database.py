import pymongo

def to_database(db,job_name,document):
    if job_name in db.list_collection_names():
        coll=db[job_name]
        coll.insert_many(document)
    else:
        coll=db.create_collection(job_name)
        coll.insert_many(document)

def from_database(db,job_name):
    if job_name in db.list_collection_names():
        coll=db[job_name].find()
        job_container=[]
        for i in coll:
            job_container.append((i))
        return job_container
    else:
        return str("Try again scrape via linkedin.")