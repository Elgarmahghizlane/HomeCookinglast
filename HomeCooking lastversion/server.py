from flask import Flask,render_template, request ,redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField
from flask_wtf.file import FileField , FileAllowed
import datetime


app=Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'images'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'



db = SQLAlchemy(app)


#  ************les tables ************

# class Meals(db.Model): 
#     id = db.Column(db.Integer, primary_key=True)
#     # categorie=db.Column(db.String(100))
#     title = db.Column(db.String(30), unique=True)
#     price = db.Column(db.Integer) 
#     # store = db.Column(db.Integer)
#     description = db.Column(db.String(500))
#     image = db.Column(db.String(30))

# class AddMeals(FlaskForm):
#     title= StringField('Title')
#     # categorie = IntegerField('Categorie')   
#     price = IntegerField('Price')
#     # store = IntegerField('Store')
#     description = TextAreaField('Description')
#     image = FileField('Image', validators=[FileAllowed(IMAGES, ' Seules les images sont acceptées. ')])

class Repas(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    categorie=db.Column(db.String(100))
    title = db.Column(db.String(30), unique=True)
    price = db.Column(db.Integer) 
    store = db.Column(db.Integer)
    description = db.Column(db.String(500))
    image = db.Column(db.String(30))

class AddRepas(FlaskForm):
    title= StringField('Title')
    categorie = IntegerField('Categorie')   
    price = IntegerField('Price')
    store = IntegerField('Store')
    description = TextAreaField('Description')
    image = FileField('Image', validators=[FileAllowed(IMAGES, ' Seules les images sont acceptées. ')])

class Message(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(100),nullable=False) 
    phone = db.Column(db.Integer,nullable=False)
    address = db.Column(db.String(200),nullable=False)
    message= db.Column(db.String(30),nullable=False)

class AddMessage(FlaskForm):
    name = StringField('name')
    email = StringField('email')
    phone = IntegerField('phone')
    address = TextAreaField('address')
    message = TextAreaField('message')


# ************Clients************
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return  render_template("about.html")

@app.route("/contact", methods=['GET','POST'])
def contact(): 
    form = AddMessage()
    if form.validate_on_submit():        
        new_message=Message(name=form.name.data,email=form.email.data,phone=form.phone.data,address=form.address.data,message=form.message.data)
        db.session.add(new_message)
        db.session.commit()
        print(new_message)
        return redirect(url_for('home'))

    return render_template("contact.html",form=form)

@app.route("/basket")
def basket():
    return render_template("basket.html")

@app.route("/meals")
def meals():
    repas=Repas.query.all()
    return render_template("meals.html", repas=repas)
@app.route("/login_client")
def login_client():
    return render_template("login_client.html")

# ************Admin************
@app.route("/admin")
def admin():
    return render_template("admin/admin.html")

@app.route("/admin/inbox")
def inbox():
    messages=Message.query.all()
    m=messages.reverse()
    # print("**",m)
    return render_template('admin/inbox.html', admin=True,messages=messages)

    # return render_template("admin/inbox.html")
@app.route("/admin/add_meals",methods=['GET','POST'])
def addmeals():
    form = AddRepas()
    if form.validate_on_submit():        
        image_url=photos.url(photos.save(form.image.data))
        new_meal=Repas(title=form.title.data,categorie=form.categorie.data,store=form.store.data,price=form.price.data,description=form.description.data,image=image_url)
        db.session.add(new_meal)
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('admin/add_meals.html', admin=True,form=form)

    # return render_template("/admin/add_meals.html")
@app.route("/login_admin")
def login_admin():
    return render_template("login_admin.html")


if __name__=="__main__":
    app.run(debug=True)