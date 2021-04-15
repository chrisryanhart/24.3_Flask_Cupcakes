"""Flask app for Cupcakes"""
from flask import Flask, render_template, redirect, request, jsonify
from models import Cupcake, db, connect_db
from flask_debugtoolbar import DebugToolbarExtension
# from forms import AddPetForm, EditPetForm
import requests


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

def serialize_cupcake(cake):
    return {
        'id': cake.id,
        'flavor': cake.flavor,
        'size': cake.size,
        'rating': cake.rating,
        'image': cake.image
    }

@app.route('/')
def display_homeage():

    return render_template('base.html')


@app.route('/api/cupcakes')
def get_cupcakes():
    cake_list = Cupcake.query.all()

    serialized_list = [serialize_cupcake(cake) for cake in cake_list]

    return jsonify(cupcakes=serialized_list)



@app.route('/api/cupcakes/<int:id>')
def get_cupcake_detail(id):
    try: 
        cupcake = Cupcake.query.get_or_404(id)
    except:
        error = '404 error - cupcake does not exist'
        return render_template('errors.html',error=error)

    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

# @app.route('/api/cupcakes/post')
# def show_post_form():
#     return render_template('post.html')

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    # new_cupcake = Cupcake(flavor='strawberry', size=4, rating=6, image='https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Chocolate_Cupcakes.jpg/360px-Chocolate_Cupcakes.jpg')

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)
    # add serialize feature, then return json
    return (jsonify(cupcake=serialized), 201)




@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json['flavor']
    cupcake.size = request.json['size']
    cupcake.rating = request.json['rating']
    cupcake.image = request.json['image']

    db.session.add(cupcake)
    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return (jsonify(cupcake=serialized), 201)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return ({"message": "Deleted"}, 201)


# Cupcake(flavor='strawberry', size=4, rating=6 image='https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Chocolate_Cupcakes.jpg/360px-Chocolate_Cupcakes.jpg')