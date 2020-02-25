from flask import Flask,flash,render_template,request,redirect, url_for, session,logging
from werkzeug import secure_filename
 # from flask_sqlalchemy import SQLAlchemy
import os
import insure2 as sh
from keras import backend as K

app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.sqlite3'
# db = SQLAlchemy(app)

# class user(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   name=db.Column(db.String(50))
#   email = db.Column(db.String(120))
#   password = db.Column(db.String(80))
#   mobileno=db.Column(db.Integer)
#   address=db.Column(db.String(160))
#   carno=db.Column(db.Integer)
#   carrcno=db.Column(db.String(25))

#   def __init__(self, name, email, password, mobileno, address,carno,carrcno):
#       self.name= name
#       self.email = email
#       self.password=password
#       self.mobileno=mobileno
#       self.address=address
#       self.carno=carno
#       self.carrcno=carrcno

# @app.route('/')
# def index():
#   if not session.get('logged_in'):
#       return render_template('index.html')
#   else:
#       if request.method == 'POST':
#           username = getname(request.form['username'])
#           return render_template('index.html', data=getfollowedby(username))
#       return render_template('index.html')
#   return render_template('index.html')

# @app.route('/login')
# def login():
#   if request.method == 'GET':
#       return render_template('login.html')
#   else:
#       fname = request.form['name']
#       mail = request.form['email']
#       passw = request.form['password']
#       mobile = request.form['mobileno']
#       faddress = request.form['address']
#       fcarno = request.form['carno']
#       fcarrcno= request.form['carrcno']

#       try:
#           data = User.query.filter_by(name=fname,email=mail, password=passw,mobileno=mobile,address=faddress,carno=fcarrcno,carrcno=fcarrcno).first()
#           if data is not None:
#               session['logged_in'] = True
#               return redirect(url_for('index'))
#           else:
#               return 'Dont Login'
#       except:
#           return "Dont Login"    

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#   if request.method == 'POST':
#       new_user = User(name = request.form['name'],email = request.form['email'],password = request.form['password'],mobileno = request.form['mobileno'],address = request.form['address'],carno = request.form['carno'],carrcno = request.form['carrcno'])
#       db.session.add(new_user)
#       db.session.commit()
#       return render_template('login.html')
#     return render_template('register.html') 

@app.route('/')      
def index():
   return render_template("index.html")

@app.route('/login')      
def login():
   return render_template("login.html")

@app.route('/register')
def register():
	return render_template('register.html')     


@app.route('/upload')
def upload():
	return render_template('upload.html')     

@app.route('/main')
def main():
   return render_template('main.html')


@app.route('/insure')
def insure():
   K.clear_session()
   return render_template('insure.html')

@app.route('/uploader',methods=['GET', 'POST']) ##called when new file is uploaded in UI
def uploader():
   K.clear_session()

   if request.method == 'POST':
      f = request.files['file']
      print(str(f.filename))
      f.save("C:/Users/Dell/Desktop/InsurePlus - Copy/static/"+secure_filename(f.filename))
      f.close()
      #path_to_file = "C:/Users/Sumit Manocha/Desktop/IIT-Hyd/static/"+str(f.filename)
      print(str(f.filename))
      sh.loadImg(str(f.filename))
      sh.imgup(str(f.filename))
      a = sh.imgup(str(f.filename))
      return render_template("claim.html", user_image = str(f.filename), user_input = a)


@app.route('/support')
def support():
	return render_template('support.html')   

# @app.route('/claim')
# def claim():
# 	return render_template('claim.html')  	         

if __name__ == '__main__':
	app.debug = True
	# db.create_all()
	app.run()    