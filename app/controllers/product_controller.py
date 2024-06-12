from app.views.product_view import render_product_detail,render_product_list
from app.utils.decorators import jwt_required,role_required
from app.models.product_model import Product
from flask import Blueprint,request,jsonify

producto_bp=Blueprint("producto",__name__)

@producto_bp.route("/products",methods=["GET"])
@jwt_required
@role_required(roles=["admin","user"])
def get_products():
    productos=Product.get_all()
    return jsonify(render_product_list(productos))

@producto_bp.route("/products/<int:id>",methods=["GET"])
@jwt_required
@role_required(roles=["admin","user"])
def get_product(id):
    producto=Product.get_by_id(id)

    if producto:
        return jsonify(render_product_detail(producto))
    return jsonify({"error":"Producto no encontrado"}),404

@producto_bp.route("/products",methods=["POST"])
@jwt_required
@role_required(roles=["admin"])
def create_product():
    data=request.json
    name=data.get("name")
    description=data.get("description")
    price=data.get("price")
    stock=data.get("stock")

    if name is None or description is None or price is None or stock is None:
        return jsonify({"error":"Faltan datos requeridos"}),400
    
    producto=Product(name,description,price,stock)
    producto.save()

    return jsonify(render_product_detail(producto)),201

@producto_bp.route("/products/<int:id>",methods=["PUT"])
@jwt_required
@role_required(roles=["admin"])
def update_producto(id):
    producto=Product.get_by_id(id)

    if not producto:
        return jsonify({"error":"Producto no encontrado"}),404
    
    data=request.json
    name=data.get("name")
    description=data.get("description")
    price=data.get("price")
    stock=data.get("stock")

    producto.update(name,description,float(price),int(stock))

    return jsonify(render_product_detail(producto))

@producto_bp.route("/products/<int:id>",methods=["DELETE"])
@jwt_required
@role_required(roles=["admin"])
def delete_product(id):
    producto=Product.get_by_id(id)

    if not producto:
        return jsonify({"error":"Producto no encontrado"}),404
    
    producto.delete()

    return "",204