use ecommerce

db.users.insertMany([
  { nom: "Alice", age: 25, ville: "Paris" },
  { nom: "Bob", age: 32, ville: "Lyon" },
  { nom: "Chloé", age: 41, ville: "Paris" }
])

db.products.insertMany([
  { nom: "Clavier", prix: 45, categorie: "Informatique" },
  { nom: "Écran", prix: 180, categorie: "Informatique" },
  { nom: "Casque", prix: 75, categorie: "Audio" },
  { nom: "Tapis de souris", prix: 12, categorie: "Accessoires" }
])

db.orders.insertOne({
  utilisateur: "Alice",
  produits: [
    { nom: "Écran", prix: 180 },
    { nom: "Casque", prix: 75 }
  ],
  total: 255
})

db.users.find()
db.products.find({ prix: { $gt: 50 } })
db.users.find({ ville: "Paris" })
db.orders.find()

db.users.updateOne({ nom: "Bob" }, { $set: { age: 33 } })

db.products.deleteOne({ nom: "Tapis de souris" })
