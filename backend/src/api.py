import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=['GET'])
def fetch_drinks():
    try:
        drinks = Drink.query.all()
        drinks= [drink.short() for drink in drinks]
        
        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except:
        abort(404)

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route("/drinks-detail", methods=['GET'])
def fetch_drinks_detail():
    try:
        drinks = Drink.query.all()
        drinks=[drink.long() for drink in drinks]
        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except:
        abort(404)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def add_drink(payload):
    body = request.json
    title = body["title"]
    recipe = body["recipe"]

    if not title or not recipe:
        abort(400)

    for item in recipe:
        color = item["color"]
        parts = item["parts"]
        name = item["name"]
        if not color or not parts or not name:
            abort(400)

    recipe=json.dumps(recipe)
    drink = Drink(title=title, recipe=recipe)
    drink.insert()

    return jsonify({"success": True, "drinks": [drink.long()]})
        

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>',methods=["PATCH"])
@requires_auth("patch:drinks")
def patch_drink(payload,id):
    drink=Drink.query.get(id)
    if not drink:
        abort(404)
    try:
        request_body=request.json
        title=request_body["title"]
        recipe=request_body["recipe"]
        
        drink.title=title
        drink.recipe = json.dumps(recipe)
        drink.update()
        return jsonify(
        {
            'success': True,
            'drinks': [drink.long()]
            
        }), 200
 
    except:
        abort(400)
        
        
    

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(payload, id):
    drink = Drink.query.get(id)

    if not drink:
        abort(404)

    try:
        drink.delete()
        return jsonify({"success": True, "delete": id})
    except:
        db.session.rollback()
        abort(500)

  
        

# Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''



'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
# @app.errorhandler(404)
# def resource_not_found_handler(error):

#         error_response['error'] = 404
#         error_response['success'] = False
#         error_response['The requested resource was not found']

#         return jsonify({
#             error_response
#         }), 404





'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
