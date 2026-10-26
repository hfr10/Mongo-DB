from bson import ObjectId
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
jeux = MongoClient("mongodb://localhost:27017")["ludotheque"]["jeux"]


def to_json(jeu):
    jeu["_id"] = str(jeu["_id"])
    return jeu


@app.post("/items")
def create():
    jeu = request.get_json()
    jeu["_id"] = jeux.insert_one(jeu).inserted_id
    return jsonify(to_json(jeu)), 201


@app.get("/items/<id>")
def read(id):
    if not ObjectId.is_valid(id):
        return jsonify({"erreur": "id invalide"}), 400
    jeu = jeux.find_one({"_id": ObjectId(id)})
    if not jeu:
        return jsonify({"erreur": "jeu introuvable"}), 404
    return jsonify(to_json(jeu))


@app.get("/items")
def list_items():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    resultats = jeux.find().skip((page - 1) * limit).limit(limit)
    return jsonify([to_json(j) for j in resultats])


@app.get("/search")
def search():
    keyword = request.args.get("keyword", "")
    filtre = {"$or": [
        {"nom": {"$regex": keyword, "$options": "i"}},
        {"description": {"$regex": keyword, "$options": "i"}},
    ]}
    if "genre" in request.args:
        filtre["genre"] = request.args["genre"]
    if "note_min" in request.args:
        filtre["note"] = {"$gte": float(request.args["note_min"])}
    return jsonify([to_json(j) for j in jeux.find(filtre)])


if __name__ == "__main__":
    app.run(debug=True)
