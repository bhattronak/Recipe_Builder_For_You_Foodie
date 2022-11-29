from flask import Flask, request, jsonify
import json
import datetime as dt
from helper.pymongo_get_database import get_database


dbname = get_database()
collection_name = dbname["recipes"]


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/recipe", methods=["POST", "GET"])
def recipe():
    if request.method == 'POST':
        data = request.get_json()
        # added new recipe url to the list
        # Insert the recipe_url in mongodb and check if it is inserted or not
        try:
            collection_name.insert_one({
                "recipe": data["recipe"],
                "user": data["user"],
                "added_date": dt.date.today().strftime("%d/%m/%Y"),
                "status": "new"
            })
            return jsonify({"message": "Recipe added successfully"})
        except Exception as e:
            return jsonify({"message": "Recipe not added", "error": e}), 400
    elif request.method == 'GET':
        # Get the list of available recipies in the database and return a json with recipe link, added date and status
        recipe_list = []
        for recipe in collection_name.find():
            recipe_list.append({
                "recipe": recipe["recipe"],
                "user": recipe["user"],
                "added_date": recipe["added_date"],
                "status": recipe["status"]
            })
        return recipe_list


if __name__ == '__main__':
    app.run(debug=True)
