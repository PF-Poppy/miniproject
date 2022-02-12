from pymongo import MongoClient

#เลือกใช้มาอันนึง
#client = MongoClient("host",port_number)
#client = MongoClient("mongodb://localhost:27017/")
client = MongoClient("mongodb://localhost",27017)

#ใช้ของกลุ่มตัวเอง
#db = client["database"]
db = client["teach"]
#col = db["collection_name"]
menu_collection = db["menu"]

mylist = client.list_database_names()
#print(mylist)

orange = {
    "name": "Orange",
    "price": 40
}
banana = {
    "name": "Banana",
    "price": 20
}

#menu_collection.insert_one(orange)
#menu_collection.insert_one(banana)

fruit_list = []
fruit_list.append(orange)
fruit_list.append(banana)
x = menu_collection.insert_many(fruit_list)
print(x.inserted_ids)

result = menu_collection.find_one() #เอาบนสุด
print(result)

r = menu_collection.find({},{"_id": 0 ,"name": 1,"price": 1})
for fruit in r:
    print(fruit)

query = {"name": "Orange","price": 40}
result = menu_collection.find(query,{"_id": 0 ,"name": 1,"price": 1})
for r in result:
    print(r)
result = menu_collection.find_one(query)
print(result)

query = {"price": {"$lt": 50}}

result = menu_collection.find(query, {"_id": 0, "name": 1})
for r in result:
    print(r)
result = menu_collection.find_one(query)
print(result)

# # Equality     {“key” : “value”}
c = menu_collection.find({"price": 259})
for menu in c:
    print(menu)
    
# # Less Than     {“key” :{$lt:”value”}}
cc = menu_collection.find({"price": {"$lt": 21}})
[print(menu) for menu in cc]
# # Greater Than    {“key” :{$gt:”value”}}
# # Less Than Equal to    {“key” :{$lte:”value”}}
# # Greater Than Equal to    {“key” :{$gte:”value”}}

# # Not Equal to    {“key”:{$ne: “value”}}
cc = menu_collection.find({"price": {"$ne": 259}})
[print(menu) for menu in cc]
# # Logical AND    { “$and”:[{exp1}, {exp2}, …, {expN}] }
# # Logical OR    { “$or”:[{exp1}, {<exp2}, …, {expN}] }
# Logical NOT    { “$not”:[{exp1}, {exp2}, …, {expN}] }
cc = menu_collection.find({"$or": [
                            {"price":{"$lt":21}},
                            {"price":{"$gt":200}}
                        ]})
[print(menu) for menu in cc]

query = {"name": "Chicken"}
menu_collection.delete_many(query)

query = {"name": "Grape"}
newvalues = { "$set": {"price": 90} }

menu_collection.update_one(query, newvalues)
#menu_collection.update_many(query, newvalues)