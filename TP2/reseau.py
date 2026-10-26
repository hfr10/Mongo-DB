from pymongo import MongoClient

db = MongoClient("mongodb://localhost:27017")["reseau"]
db.users.drop()
db.publications.drop()

db.users.insert_many([
    {"nom": "Alice", "email": "alice@mail.com"},
    {"nom": "Bob", "email": "bob@mail.com"},
    {"nom": "Chloé", "email": "chloe@mail.com"},
])

db.publications.insert_many([
    {"auteur": "Alice", "contenu": "Premier post !", "commentaires": [], "likes": []},
    {"auteur": "Alice", "contenu": "Vacances à la mer", "commentaires": [], "likes": []},
    {"auteur": "Bob", "contenu": "Nouveau projet Python", "commentaires": [], "likes": []},
    {"auteur": "Chloé", "contenu": "Recette de crêpes", "commentaires": [], "likes": []},
    {"auteur": "Bob", "contenu": "Match ce soir", "commentaires": [], "likes": []},
])

db.publications.update_one(
    {"contenu": "Premier post !"},
    {"$push": {"commentaires": {"$each": [
        {"auteur": "Bob", "texte": "Bienvenue !"},
        {"auteur": "Chloé", "texte": "Salut Alice"},
    ]}}},
)
db.publications.update_one(
    {"contenu": "Recette de crêpes"},
    {"$push": {"commentaires": {"auteur": "Alice", "texte": "Miam"}}},
)

db.publications.update_one({"contenu": "Premier post !"}, {"$addToSet": {"likes": {"$each": ["Bob", "Chloé"]}}})
db.publications.update_one({"contenu": "Recette de crêpes"}, {"$addToSet": {"likes": {"$each": ["Alice", "Bob", "Chloé"]}}})
db.publications.update_one({"contenu": "Match ce soir"}, {"$addToSet": {"likes": "Alice"}})

print("1. Toutes les publications")
for p in db.publications.find():
    print(p["auteur"], ":", p["contenu"])

print("\n2. Publications de Bob")
for p in db.publications.find({"auteur": "Bob"}):
    print(p["contenu"])

print("\n3. Commentaires de 'Premier post !'")
pub = db.publications.find_one({"contenu": "Premier post !"})
for c in pub["commentaires"]:
    print(c["auteur"], ":", c["texte"])

print("\n4. Publication la plus likée")
top = next(db.publications.aggregate([
    {"$addFields": {"nbLikes": {"$size": "$likes"}}},
    {"$sort": {"nbLikes": -1}},
    {"$limit": 1},
]))
print(top["contenu"], "-", top["nbLikes"], "likes")

print("\n5. Nombre de publications par utilisateur")
for r in db.publications.aggregate([{"$group": {"_id": "$auteur", "total": {"$sum": 1}}}]):
    print(r["_id"], ":", r["total"])
