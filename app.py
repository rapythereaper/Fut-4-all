from flask import Flask,request,session
from flask import render_template
from flask import abort, redirect, url_for
from werkzeug.utils import secure_filename


import json
import requests

import setting
from db import *

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}

def __dis__(lhs,rhs):
    a=Expression(lhs.lat, '-', rhs["lat"])
    b=Expression(lhs.lan,'-',rhs["lan"])
    c=Expression(a,'*',a)
    d=Expression(b,'*',b)

    return Expression(c,"+",d)


app = Flask(__name__)
app.secret_key = setting.APP_SECRETE_KEY

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/")
def home():
    return render_template("index1.html")
    d={"lan":2331,"lat":90}
    data=Futsal.select().order_by((__dis__(Futsal,d)))
    res=[]
    if data.exists():
        for i in data:
            res.append(i.todict())
    return json.dumps(res)
    return "index.html"
    
@app.route("/get/<float:lat>/<float:lan>/<int:offset>")
def idk(lat,lan,offset):
    data=Futsal.select().order_by(__dis__(Futsal,{"lan":lan,"lat":lat})).offset(offset).limit(50)

    res=[]
    if data.exists():
        for i in data:
            res.append(i.todict())
    return json.dumps(res)




@app.route("/login",methods=['GET', 'POST'])
def login():
    if not session.get("user") :
        if request.method=='POST':
            info= request.json
            print("[*]Login:"+ info.get("uid"))
            user=User.select().where(User.uid==info.get("uid"))
            if  user.exists():
                user=user.get()
                if user.check_password(info.get("pass")):
                    
                    session["user"]=user.todict();
                    #return redirect(url_for("dashboard"))
                    return "ok"

            return "error",404
        else :
            return render_template("login.html",name="Login")
    else:
        return redirect(url_for("dashboard"))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user', None)
    return redirect(url_for('home'))
   

@app.route("/dashboard")
def dashboard():
    if session.get("user"):
        return render_template("Dashboard.html")
    return redirect(url_for("login"))

@app.route("/dashboard/<string:action>",methods=["GET","POST"])
def dashboard_(action):
    print("action jakson "+action)
    if session.get("user"):
        if request.method=="POST":
            data=request.json
            if action=="del":
                f=Futsal.select().where(Futsal.id==data.get("id"))
                if f.exists():
                    f=f.get()
                    if f.owener==session["user"]["uid"]:
                        f.delete_instance()
                        return json.dumps("ok")
                return json.dumps("error"),404

            if action=="insert":

                f=Futsal(name=data["name"],
                    open_time=dt.time(data["open_time"][0],data["open_time"][1]),
                    close_time=dt.time(data["close_time"][0],data["close_time"][0]),
                    lat=data["lat"],
                    lan=data["lan"],
                    owener=session["user"]["uid"]
                    )
                file=request.files.get("file")
                filename=None
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                f.img=filename
                f.save()

                return json.dumps({"_id":f.id})

        if action=="get":
         
            res=Futsal.select().where(Futsal.owener==session["user"]["uid"])
        
            if res.exists():
                data=[]
                for t in res:
                    data.append(t.todict())

                return json.dumps(data)
            
            return "Null"
        


        return "Dashboard"
       # return render_template("dashboard.html",name="Dashboard")
    return redirect(url_for("login"))




@app.route("/rent",methods=["GET","POST"])
def rent():
    if request.method=="POST":
        data=request.json
        res=Futsal.select().where(Futsal.id==data.get("_id"))
        if res.exists():
            res=res.get()
            booked=Booked.select().where(
                (Booked.futsal==res)&
               ( Booked.date==dt.date(data["date"][0],data["date"][1],data["date"][2]))&
                (Booked.start_time<=dt.time(data["start_time"][0],data["start_time"][1]))|
                (Booked.start_time>=dt.time(data["end_time"][0],data["end_time"][1]))
                )
            if booked.exists():
                return "Time not fisible",404

            status=res.time_and_money(data["start_time"],data["end_time"])
            status["date"]=data["date"];
            if status["status"] :
                session["status"]=status;
                return json.dumps({"amount":status["amount"]})

    return "error",404
    #GET req
    

@app.route("/payment",methods=["POST"])
def payment():
    if request.method=="POST":
        data=request.json
        playload=data
        playload["amount"]=session.get("status").get("amount")*100
        print(playload);

              #  playload={"amount":session.get("status").get("amount")*100,
        #"token": data.get("token")
        #}
        url = "https://khalti.com/api/v2/payment/verify/"
        headers = {"Authorization":setting.KHALTI_SECRETE_KEY}
        rs = requests.post(url,playload, headers = headers)
        if rs.status_code==200  :
            b=Booked(_id=playload["token"])
            b.set_data(session["status"])
            b.save()
            session.pop('status', None)
            return json.dumps({"token":playload["token"]})
        #refund baki xa


    return "payment verify failed",404







app.run(host="127.0.0.1", port=8080)