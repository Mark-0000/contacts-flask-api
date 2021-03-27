from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f'{self.name} - {self.description}'


@app.route('/')
def contacts():
    return 'Flask API'


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    output = [{'id': drink.id, 'name': drink.name, 'description': drink.description} for drink in drinks]
    return {"drinks": output}


@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {'name': drink.name, 'description': drink.description}


@app.route('/drinks', methods=["POST"])
def add_drink():
    drink = Drink(name=request.json['name'], description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'message': 'drink created', 'id': drink.id}


@app.route('/drinks', methods=["PUT"])
def update_drink():
    drink = Drink.query.get(request.json['id'])
    if drink is None:
        return {"error": "drink not found"}
    drink.name = request.json['name']
    drink.description = request.json['description']
    db.session.commit()
    return {'message': "drink updated"}


@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error": "drink not found"}
    db.session.delete(drink)
    db.session.commit()
    return {'message': "drink deleted"}


if __name__ == '__main__':
    app.run(debug=True)
