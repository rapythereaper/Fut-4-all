import sys

import db

db.start






class CLI:
	def __init__(self):
		self.option=[
			f"add_user\t(--add user in database)",
			f"del_user	<uid>\t(--deletes user <uid> & its futsal record form database)",
			f"change_password	<uid>\t(--change passwor of user <uid>)"
			f"get <DB name>\t(--print all the record of <DB name>)"
		]
		

	def print(self):
		print("****[Fut-4-all CLi tool]****")
		print("-help menue")
		for i in self.option:
			print(f"\t[-]{i}")

	def add_user(self):
		uname=input("User Name: ")
		passw=input("Password: ")
		name=input("Name: ")
		ul=db.User.select().where(User.uid==uname)
		if(ul.exists()):
			print("User name already exists")
			exit()
		u=db.User(name=name,uid=uname)
		u.setPassword(passw)
		u.save()

	def del_user(self):
		if(len(sys.argv)==3):
			uname=sys.argv[2]
			u=db.User.select().where(User.uid==uname)
			f=db.Futsal.select().where(Futsal.owener==uname)
			if(u.exists()):
				u.get().delete_instance
			if f.exists():
				for i in f:
					i.delete_instance()
		else:
			print("[!]Error: plz provide user name as argument")

	def change_password(self):
		if(len(sys.argv)==3):
			uname=sys.argv[2]
			u=db.User.select().where(User.uid==uname)
			if u.exists() :
				user=u.get()
				pas=input("Enter new password: ")
				user.set_password(pas)
				user.save()
		else:
			print("[!]Error: plz provide a valid username")

	def get(sef):
		if len(sys.argv)==3:
			try:
				clss=getattr(db,sys.argv[2])
				clss=clss.select()
				if clss.exists():
					for i in clss:
						print(f"Record No.{i.id}")
						dick=i.todict()
						for j in dick:
							print(f"\t[*]{j} :{dick[j]}")
						print("...................")
			except:
				print(f"[!]Error:: no DB record name {sys.argv[2]}")

		else:
			print("[!]Error:: plz provide a DB name")






"""
if(opt=="add-user"):
	uname=input("User Name: ")
	passw=input("Password: ")
	name=input("Name: ")
	ul=User.select().where(User.uid==uname)
	if(ul.exists()):
		print("User name already exists")
		exit()
	u=User(name=name,uid=uname)
	u.setPassword(passw)
	u.save()

elif opt=="del-user":
	if(len(sys.argv)==3):
		uname=sys.argv[2]
		u=User.select().where(User.uid==uname)
		f=Futsal.select().where(Futsal.owener==uname)
		if(u.exists()):
			u.get().delete_instance
		if f.exists():
			for i in f:
				i.delete_instance()
	else:
		print("[!]Error: plz provide user name as argument")

elif opt=="change-password":
	if(len(sys.argv)==3):
		uname=sys.argv[2]
		u=User.select().where(User.uid==uname)
		if u.exists() :
			user=u.get()
			pas=input("Enter new password: ")
			user.set_password(pas)
			user.save()


	else:
		print("[!]Error: plz provide user name as argument")
elif opt=="get-user":
	u=User.select()
	if u.exists():
		for i in User.select():
			print(f"Record No.{i.id}")
			dick=i.todict()
			for j in dick:
				print(f"\t[*]{j} :{dick[j]}")
			print("...................")

"""

cli=CLI()
if len(sys.argv)== 1 or sys.argv[1]=="help":
	cli.print()

else:
	try:
		getattr(cli,sys.argv[1])()
	except :
		print(f"[!]No Module name {sys.argv[1]}")

