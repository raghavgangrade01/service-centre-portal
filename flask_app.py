import requests
import pyqrcode
import png
from flask import Flask,render_template,redirect,request
import flask
import flask_login
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import LoginManager
from flask_login import current_user
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import datetime
def verify_pincode(pincode):
    try:
        url="https://api.postalpincode.in/pincode/"+str(pincode)
        result=requests.get(url=url)
        result=result.json()
        if result[0]["Status"]=="404" or result[0]["Status"]=="Error":
            return 0
        else:
            return 1
    except:
        return 0
def qrcode():
    s = "Name:Abhinav Gangrade\nPhone Number:6265056990"
    url = pyqrcode.create(s)
    url.svg("myqr.svg", scale = 8)
    url.png('myqr.png', scale = 6)
db=SQLAlchemy()
app=Flask(__name__)
app.config["SECRET_KEY"]="SPORTAL"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///db.sqlite3"
db.init_app(app)
login_manager=LoginManager()
login_manager.login_view="login"
login_manager.init_app(app)
class Datacenter_Credential(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    pname=db.Column(db.String(1000))
    pincode=db.Column(db.String(1000))
    Address=db.Column(db.String(1000))
    Landmark=db.Column(db.String(1000))
    phone=db.Column(db.String(1000))
    email=db.Column(db.String(1000))
    city=db.Column(db.String(1000))
    category=db.Column(db.String(1000))
    payment=db.Column(db.String(1000))
@login_manager.user_loader
def load_user(user_id):
     return Datacenter_Credential.query.get(int(user_id))
@app.route("/")
def main_page():
    return render_template("main_page.html")
@app.route("/search")
def search_centers():
    return render_template("search.html")
@app.route("/registration")
def register():
    return render_template("sc_reg_portal.html",message="")
@app.route("/registration",methods=["POST"])
def register_post():
    # Using Get method extracting the value from form
    username=request.form.get("username")
    password=request.form.get("psw")
    name=request.form.get("name")
    pincode=request.form.get("pincode")
    category=request.form.get("category")
    payment=request.form.get("payment")
    city=request.form.get("city")
    landmark=request.form.get("landmark")
    add1=request.form.get("al1")
    add2=request.form.get("al2")
    address=add1+"\\n"+add2
    phone=request.form.get("phone")
    email=request.form.get("email")
    priter=request.form.get("propriter") 
    user=(Datacenter_Credential.query.filter_by(username=username).count())
    print(user)
    if not verify_pincode(pincode):
        return render_template("sc_reg_portal.html",message="Pincode is not Valid")
    if user>0:
        return render_template("sc_reg_portal.html",message="Username Already Exists")
    new_user=Datacenter_Credential(username=username,name=name,pincode=pincode,pname=priter,Address=address,Landmark=landmark,phone=phone,email=email,city=city,category=category,payment=payment,password=generate_password_hash(password,method="sha256"))
    db.session.add(new_user)
    db.session.commit()
    return redirect("/login")
@app.route("/login")
def login():
    return render_template("sc_login_page.html",message="")
@app.route("/login",methods=["POST"])
def login_post():
    pincode=request.form.get("pincode-lgn")
    username=request.form.get("username-lgn")
    password=request.form.get("psw-lgn")
    user=Datacenter_Credential.query.filter_by(username=username).first()
    if not verify_pincode(pincode):
        return render_template("sc_login_page.html",message="Invalid Pincode")
    if user==None:
        return render_template("sc_login_page.html",message="User doesnt Exist")
    if user.pincode!=pincode:
        return render_template("sc_login_page.html",message="Pincode Doesnt matched with the Username")
    if not check_password_hash(user.password,password):
        return render_template("sc_login_page.html",message="Wrong Password")
    login_user(user)
    return user.name
@app.route("/booking")
def booking():
    return render_template("booking_portal.html")
@app.route("/details")
def details():
    pincode=request.args["pincode-search"]
    if verify_pincode(pincode):
        return request.args["pincode-search"]
    else:
        return "Pincode doesnt Exist"
@app.before_first_request
def create_tables():
    db.create_all()
@app.before_request
def before_request():
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=10)
    flask.session.modified = True
    flask.g.user = flask_login.current_user
app.run(debug=True)