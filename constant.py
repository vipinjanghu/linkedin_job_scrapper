url = "https://www.linkedin.com/home"
#cluster_user="vipinjanghu"
cluster_pass="linkdin12345"


import pymongo
client = pymongo.MongoClient(f"mongodb+srv://vipinjanghu:{cluster_pass}@cluster0.2rskres.mongodb.net/?retryWrites=true&w=majority")
db = client["scrapper"]