from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://your_username:your_password@localhost/your_database_name'
db = SQLAlchemy(app)

# Define the model for Dojo
class Dojo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ninjas = db.relationship('Ninja', backref='dojo', lazy=True)

# Define the model for Ninja
class Ninja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    dojo_id = db.Column(db.Integer, db.ForeignKey('dojo.id'), nullable=False)

# Create the database tables
db.create_all()

# Routes
@app.route('/')
def index():
    return redirect(url_for('dojos'))

@app.route('/dojos')
def dojos():
    all_dojos = Dojo.query.all()
    return render_template('dojos.html', dojos=all_dojos)

@app.route('/dojos/add', methods=['GET', 'POST'])
def add_dojo():
    if request.method == 'POST':
        dojo_name = request.form.get('name')
        new_dojo = Dojo(name=dojo_name)
        db.session.add(new_dojo)
        db.session.commit()
        return redirect(url_for('dojos'))
    return render_template('add_dojo.html')

@app.route('/dojos/<int:dojo_id>')
def dojo_show(dojo_id):
    dojo = Dojo.query.get(dojo_id)
    if dojo:
        ninjas = dojo.ninjas
        return render_template('dojo_show.html', dojo=dojo, ninjas=ninjas)
    return redirect(url_for('dojos'))

@app.route('/ninjas/add', methods=['GET', 'POST'])
def add_ninja():
    if request.method == 'POST':
        ninja_name = request.form.get('name')
        dojo_id = int(request.form.get('dojo_id'))
        new_ninja = Ninja(name=ninja_name, dojo_id=dojo_id)
        db.session.add(new_ninja)
        db.session.commit()
        return redirect(url_for('dojo_show', dojo_id=dojo_id))
    dojos = Dojo.query.all()
    return render_template('add_ninja.html', dojos=dojos)

if __name__ == '__main__':
    app.run(debug=True)
