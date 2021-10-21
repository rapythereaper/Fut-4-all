from peewee import *
from peewee import Expression # the building block for expressions
import bcrypt
import os
import datetime as dt

user_db = SqliteDatabase('User.db')
futsal_db=SqliteDatabase('futsal.db')



class User(Model):
    name = CharField()
    uid= CharField()
    password=CharField()

    def set_password(self,s):
        if(s!=None ):
            self.password=bcrypt.hashpw(s.encode(),bcrypt.gensalt(5))
            return True
        return False

    def check_password(self,s):
        if(s!=None):
            if bcrypt.checkpw(s.encode(),self.password.encode()):
                return True
        return False
    def todict(self):
        return {"id":self.id,"name":self.name,"uid":self.uid};
    


    class Meta:
        database = user_db # This model uses the "people.db" database.

class Futsal(Model):
    name=CharField()
    open_time= TimeField()
    close_time=TimeField()
    lat=DecimalField()
    lan=DecimalField()
    img=CharField(null=True)
    owener=CharField()

    def time_and_money(self,s,e):
        data={"status":False}
        if s!=e :
            s1=dt.time(s[0],s[1])
            e1=dt.time(e[0],e[1])
            print(s1,e1)
            print(self.open_time,self.close_time)
            print(e1.hour-s1.hour)
            if s1>=self.open_time and e1<=self.close_time and e1.hour-s1.hour>0 :
                data["status"]=True
                data["amount"]=(e1.hour-s1.hour)*100
                data["start_time"]=s
                data["end_time"]=e
                data["futsal"]=self.id


        return data


    def todict(self):
        return {"name":self.name,"_id":self.id,"open_time":str(self.open_time),
                "close_time":str(self.close_time),
                "lat":float(self.lat),
                "lan":float(self.lan),
                "owener":self.owener
        }

    class Meta:
        database = futsal_db



class Booked(Model):
    _id=CharField()
    futsal=ForeignKeyField(Futsal)
    date=DateField()
    start_time=TimeField()
    end_time=TimeField()

    def set_data(self,data):
        self.futsal=Futsal(id=data["futsal"])
        self.date=dt.date(data["date"][0],data["date"][1],data["date"][2])
        self.start_time=dt.time(data["start_time"][0],data["start_time"][1])
        self.end_time=dt.time(data["end_time"][0],data["end_time"][1])



    class Meta:
        database=futsal_db


def start():
    if(not os.path.isfile("./User.db")):
        user_db.create_tables([User])
    if(not os.path.isfile("./futsal.db")):
        futsal_db.create_tables([Futsal,Booked])

start()