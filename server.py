from flask import Flask,Response,request
import pymongo
import json
import os

app = Flask(__name__)

try:

    #Enter DB credentials
    USERNAME = os.environ.get("USERNAME")
    PASSWORD = os.environ.get("PASSWORD")
    HOST = os.environ.get("HOST")
    PORT = os.environ.get("PORT")
    
    client = pymongo.MongoClient("mongodb://"+USERNAME+":"+PASSWORD+"@"+HOST+":"+PORT)
    db=client["aashish"]
    
    
except Exception as ex:
    print(ex)
    print("cannot connect to DB")

@app.route("/loadmachine",methods=["POST"])
def load_machine():
    try:
        data=request.get_json()
        for item in data:
            db.foodmart.update({"item":item["item"]},item,upsert=True)
        return Response(
            response=json.dumps({"success":True,"message":"Databse loaded/updated"}),
            status=200, 
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"success":False,"message":"Cannot post data into DB"}),
            status=500, 
            mimetype="application/json"
        )

@app.route("/fetchitems",methods=["GET"])
def fetch_items():
    try:
        item=request.args.get("item")
        amount=request.args.get("amount")
        quantity=request.args.get("quantity")

        dbdata = db.foodmart.find_one({"item":item})
        print(dbdata)
        if dbdata:
            
            if dbdata["quantity"]<int(quantity):
                return Response(
                response=json.dumps({'success':False,"message":"Given quantity is unavailable"}),
                mimetype="application/json"
                )
            else:
                
                req_amount=dbdata["cost"]*int(quantity)
                
                if req_amount>int(amount):
                    return Response(
                    response=json.dumps({'success':False,"message":"Amount paid is insuffiecient!"}),
                    mimetype="application/json"
                    )
                else:
                    db.foodmart.update_one({"item":item},{"$set":{"quantity":dbdata["quantity"]-int(quantity)}})
                    return Response(
                    response=json.dumps({'success':True,"message":quantity+" "+item+" purchased ! Database updated"}),
                    mimetype="application/json"
                    )
        else:
            return Response(
                    response=json.dumps({'success':False,"message":"Given item is unavailable!"}),
                    mimetype="application/json"
                    )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"success":False,"message":"Cannot post data into DB"}),
            status=500, 
            mimetype="application/json"
        )
if __name__ == "__main__":
    app.run(port=8000,debug=True)