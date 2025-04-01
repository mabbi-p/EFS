from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app and MySQL Database connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mabbi515@localhost/furniture_db'  # Replace with your MySQL username, password, and database name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a Product model (this will create a 'products' table in your MySQL database)
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)

# Route to add a new product (this will save product details to your MySQL database)
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        stock_quantity=data['stock_quantity']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully"}), 201

# Route to get all products (this will fetch product details from the database)
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock_quantity": product.stock_quantity
    } for product in products])

if __name__ == '__main__':
    app.run(debug=True)
