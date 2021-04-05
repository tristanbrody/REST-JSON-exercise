from flask import Flask, request, redirect, render_template, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc
from models import db, Cupcake, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
connect_db(app)

#FE code

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/search')
def search():
    search = request.args['search']
    search_formatted = '%{}%'.format(search)
    search_results = Cupcake.query.filter(Cupcake.flavor.like(search_formatted)).all()
    return render_template('index.html', search_results=search_results)

#BE code for API

@app.route('/api/cupcakes')
def get_root_resource():
    """Respond with data about all cupcakes"""
    cupcakes = Cupcake.query.all()
    serialized_cupcakes = [serialize_cupcake(cupcake) for cupcake in cupcakes]
    return jsonify(cupcakes=serialized_cupcakes)

@app.route('/api/cupcakes/<cupcake_id>')
def get_single_cupcake(cupcake_id):
    """Respond with data about a single cupcake"""
    cupcake = serialize_cupcake(Cupcake.query.get_or_404(cupcake_id))
    return jsonify(cupcake=cupcake)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a cupcake"""
    flavor = request.json["flavor"]
    image = request.json.get("image")
    size = request.json["size"]
    rating = request.json["rating"]
    cupcake = Cupcake(flavor=flavor,size=size,rating=rating,image=image)

    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=serialize_cupcake(cupcake)), 201

@app.route('/api/cupcakes/<cupcake_id>', methods=["PATCH"])
def update_all_cupcake_fields(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json["flavor"]
    cupcake.image = request.json.get("image")
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=serialize_cupcake(cupcake))

@app.route('/api/cupcakes/<cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return {"message": "Deleted"}

def serialize_cupcake(cupcake):
    """Turn a SQLAlchemy cupcake object into dictionary to allow for conversion to JSON"""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }