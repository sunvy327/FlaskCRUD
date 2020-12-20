from flask import Flask

from flask_pymongo import PyMongo

from bson.json_util import dumps

from bson.objectid import ObjectId #generates random strings that is used as ID

from flask import jsonify,request #converts the bson into json, # request is used to request from the server

from werkzeug.security import generate_password_hash, check_password_hash
#wekzeug is a hashing library for passwords

app = Flask(__name__) #standard syntax for flask application

app.secret_key = "secretkey"

app.config["MONGO_URI"] = "mongodb://localhost:27017/testdb1"

mongo = PyMongo(app) #Connecting the flask app with pymongo library

#POST request for inserting records on DB

@app.route("/add", methods = ["POST"])
def add_user():
    _json = request.json
    _name = _json["name"]
    _email = _json["email"]
    _password = _json["pwd"]

    if _name and _email and _password and request.method == "POST":
        _hashed_password = generate_password_hash(_password)

        id = mongo.db.user.insert({"name":_name, "email":_email, "pwd":_hashed_password})
        #"user" here after mongo.db is the collection name of the db in the Mongo

        #creating a response variable after Sucessful Opertation
        resp_add_user = jsonify("User Added Successfully")

        resp_add_user.status_code = 200 # Status code 200, meaning operation Success

        return resp_add_user

    else:
        return not_found()

@app.route("/user")
def users():
    users = mongo.db.user.find()
    resp_read_user = dumps(users)
    return resp_read_user 


@app.route("/user/<id>")
def user(id):
    user = mongo.db.user.find_one({"_id": ObjectId(id)})
    resp_read_user_one = dumps(user)
    return resp_read_user_one


@app.route("/delete/<id>", methods = ["DELETE"])
def delete_user(id):
    user = mongo.db.user.delete_one({"_id":ObjectId(id)})
    resp_delete_user_one = jsonify("User Deleted Successfully")
    resp_delete_user_one.status_code = 200

    return resp_delete_user_one

@app.route("/update/<id>", methods = ["PUT"])
def update_user(id):
    
    _id = id
    _json = request.json
    _name = _json["name"]
    _email = _json["email"]
    _password = _json["pwd"] 

    if _name and _email and _password and _id and request.method == "PUT":
        _hashed_password = generate_password_hash(_password)
        
        # I need to work on and see how the update really works!
        
        mongo.db.user.update_many(
         {"_id": ObjectId(_id)}, 
         {"$set":{"name":_name}}, 
         {"email":_email}, 
         {"pwd": _hashed_password},
         "multi"==True)
        
        resp_update_user = jsonify("User Updated Successfully")
        resp_update_user.status_code = 200

        return resp_update_user
    
    else:
         return not_found()



@app.errorhandler(404)
def not_found(error=None):
    message = {
        "status":404,
        "message":"Not Found" + request.url}
    

    resp_not_found = jsonify(message)
    resp_not_found.status_code = 404

    return resp_not_found


if __name__=="__main__":
    app.run(debug=True)



