from flask import Flask, request, jsonify, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
import os

# Инициализация
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db1.sqlite')
app.config['SQLALCHEMY_BINDS'] = {
    'db1': 'sqlite:///' + os.path.join(basedir, 'db1.sqlite'),
    'db2': 'sqlite:///' + os.path.join(basedir, 'db2.sqlite')
}
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    # __bind_key__ = 'db1'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    name = db.Column(db.String(50))
    language = db.Column(db.String(10))

    def __init__(self, email, name, language):
        self.email = email
        self.name = name
        self.language = language

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'name', 'language')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Создаем пользователя
@app.route('/api/user', methods = ['POST'])
def add_user():
    email = request.json['email']
    name = request.json['name']
    language = request.json['language']

    new_user = User(email, name, language)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

# Получить всех пользователей
@app.route('/api/user', methods = ['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result)

# Получить одного пользователя
@app.route('/api/user/<string:id>', methods = ['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# Обновить инфу о пользователе
@app.route('/api/user/<string:id>', methods = ['PUT'])
def update_user(id):
    user = User.query.get(id)

    email = request.json['email']
    name = request.json['name']
    language = request.json['language']

    user.email = email
    user.name = name
    user.language = language

    db.session.commit()

    return user_schema.jsonify(user)

# Удалить пользователя
@app.route('/api/user/<string:id>', methods = ['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

#------------------------------------------------------------------
# Данные для автомобилей
'''
class Car(db.Model):
    __bind_key__ = 'db2'
    id = db.Column(db.Integer, primary_key=True)
    model_ru = db.Column(db.String(50))
    model_eng = db.Column(db.String(50))
    year = db.Column(db.String(4))

    def __init__(self, model_ru, model_eng, year):
        self.model_ru = model_ru
        self.model_eng = model_eng
        self.year = year

class CarSchema(ma.Schema):
    class Meta:
        fields = ('id', 'model_ru', 'model_eng', 'year')

car_schema = CarSchema()
cars_schema = CarSchema(many=True)

# Создать автомобиль
@app.route('/api/car', methods=['POST'])
def add_car():
    model_ru = request.json['model_ru']
    model_eng = request.json['model_eng']
    year = request.json['year']

    new_car = Car(model_ru, model_eng, year)
    db.session.add(new_car)
    db.session.commit()

    return car_schema.jsonify(new_car)

# Получить все автомобили
@app.route('/api/car', methods = ['GET'])
def get_cars():
    all_cars = Car.query.all()
    result = cars_schema.dump(all_cars)

    return jsonify(result)

# Получить один автомобиль
@app.route('/api/car/<string:id>', methods = ['GET'])
def get_car(id):
    car = Car.query.get(id)
    return car_schema.jsonify(car)


# Обновить даннеы об автомобиле
@app.route('/api/car/<string:id>', methods=['PUT'])
def update_car(id):
    car = Car.query.get(id)

    model_ru = request.json['model_ru']
    model_eng = request.json['model_eng']
    year = request.json['year']

    car.model_ru = model_ru
    car.model_eng = model_eng
    car.year = year

    db.session.commit()

    return car_schema.jsonify(car)

# Удалить автомобиль
@app.route('/api/car/<string:id>', methods = ['DELETE'])
def delete_car(id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    return car_schema.jsonify(car)

#------------------------------------------------------------------------------------------------------------------
#HTML PART

# Редирект домой
@app.route('/web')
def index():
    return render_template('home.html')

# О нас
@app.route('/web/about')
def about():
    return render_template('about.html')

# Автомобили
@app.route('/web/cars')
def cars():

    all_products = Car.query.all()
    cars = cars_schema.dump(all_products)

    if len(cars) > 0:
        return render_template('cars.html', cars=cars)
    else:
        msg = 'Автомобилей нет'
        return render_template('cars.html', msg=msg)

class RegisterForm(Form):
    name = StringField('Имя', [validators.DataRequired(), validators.Length(min=3, max=50)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=6, max=30)])
    language = StringField('Язык', [validators.DataRequired(), validators.Length(min=2, max=20)])
    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли не совпадают')
    ])
    confirm = PasswordField('Подтвердите пароль')

@app.route('/web/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        language = form.language.data
        password = sha256_crypt.encrypt(str(form.password.data))

        new_user = User(email, name, language, password)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация прошла успешно!', 'success')

    return render_template('register.html', form=form)


@app.route('/web/cars/<string:id>')
def car(id):
    car = Car.query.get(id)
    return render_template('car.html', car=car)
'''

if __name__ == "__main__":
    app.run(debug=True)