from pymongo import MongoClient
from bson import ObjectId

MC = MongoClient("127.0.0.1",27017)

MongoDB = MC["Day93"] # 创建一个新的数据库，且没有生成数据库，因为没有数据

 #插入
res = MongoDB.Users.insert_one({"name":"ywb","age":99}) # 单个插入
print(res.inserted_id,type(res.inserted_id)) #5d515df968da7313e10fed46 <class 'bson.objectid.ObjectId'>

res = MongoDB.Users.insert_many([{"name":"wang","age":22},{"name":"wu","age":20}]) #多个插入
print(res.inserted_ids,type(res.inserted_ids))  #注意：这里要加s，因为是list，不会触发每个对象的str，单个就会打印具体指
    #[ObjectId('5d5160749d1fec33df7b6400'), ObjectId('5d5160749d1fec33df7b6401')] <class 'list'>


 #查询
res = MongoDB.Users.find_one({"name":"ywb"})
print(res) #{'_id': ObjectId('5d515df968da7313e10fed46'), 'name': 'ywb', 'age': 99}

res = MongoDB.Users.find_one({"_id":ObjectId("5d515df968da7313e10fed46")})
print(res) #{'_id': ObjectId('5d515df968da7313e10fed46'), 'name': 'ywb', 'age': 99}

res = MongoDB.Users.find({"name":"ywb"}) # 得到一个生成器
for raw in res:
    print(raw)


 #改
MongoDB.Users.update_one({},{"$inc":{"age":1}})  # 第一个对象age+1
MongoDB.Users.update_many({},{"$inc":{"age":1}})  # 第一个对象age+1

 #删除

MongoDB.Users.delete_one({})  # 删除第一条数据，可写入条件
MongoDB.Users.delete_many({})  # 删除第一条数据，可写入条件

 #高级函数
from pymongo import DESCENDING,ASCENDING  # 正序，倒叙
res = MongoDB.Users.find({}).skip(2).sort("age",DESCENDING)  # 还可以填-1正序
for row in res:
    print(row)

