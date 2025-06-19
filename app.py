from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return 'Superheroes API'

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [hero.to_dict() for hero in heroes]
    return jsonify(heroes_data)

# GET /heroes/:id
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404

    hero_data = hero.to_dict()
    hero_data['hero_powers'] = []

    for hp in hero.hero_powers:
        hp_data = {
            'id': hp.id,
            'hero_id': hp.hero_id,
            'power_id': hp.power_id,
            'strength': hp.strength,
            'power': hp.power.to_dict()
        }
        hero_data['hero_powers'].append(hp_data)

    return jsonify(hero_data)

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [power.to_dict() for power in powers]
    return jsonify(powers_data)

# GET /powers/:id
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    return jsonify(power.to_dict())

# PATCH /powers/:id
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    data = request.get_json()
    try:
        if 'description' in data:
            power.description = data['description']
            db.session.commit()
            return jsonify(power.to_dict())
    except ValueError as e:
        return jsonify({'errors': [str(e)]}), 400

# POST /heroes
@app.route('/heroes', methods=['POST'])
def create_hero():
    data = request.get_json()
    if not data.get('name') or not data.get('super_name'):
        return jsonify({'errors': ['Name and super_name are required']}), 400
    hero = Hero(name=data['name'], super_name=data['super_name'])
    db.session.add(hero)
    db.session.commit()
    return jsonify(hero.to_dict()), 201

# DELETE /heroes/:id
@app.route('/heroes/<int:id>', methods=['DELETE'])
def delete_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    db.session.delete(hero)
    db.session.commit()
    return jsonify({}), 204

# POST /powers
@app.route('/powers', methods=['POST'])
def create_power():
    data = request.get_json()
    if not data.get('name') or not data.get('description'):
        return jsonify({'errors': ['Name and description are required']}), 400
    try:
        power = Power(name=data['name'], description=data['description'])
        db.session.add(power)
        db.session.commit()
        return jsonify(power.to_dict()), 201
    except ValueError as e:
        return jsonify({'errors': [str(e)]}), 400

# DELETE /powers/:id
@app.route('/powers/<int:id>', methods=['DELETE'])
def delete_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    db.session.delete(power)
    db.session.commit()
    return jsonify({}), 204

# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    required_fields = ['strength', 'power_id', 'hero_id']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'errors': [f'Missing fields: {", ".join(missing_fields)}']}), 400

    try:
        hero_power = HeroPower(
            strength=data['strength'],
            power_id=data['power_id'],
            hero_id=data['hero_id']
        )

        db.session.add(hero_power)
        db.session.commit()

        return jsonify(hero_power.to_dict()), 201

    except ValueError as e:
        return jsonify({'errors': [str(e)]}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
