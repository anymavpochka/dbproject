from flask import Flask, render_template, redirect, url_for, request
#from connection_to_db import engine
from flask import jsonify
from sqlalchemy.sql import select, update, join
from sqlalchemy import and_, or_, between, asc, desc, update
from sqlalchemy.orm import sessionmaker
import time
# from flask_wtf import FlaskForm
import datetime
import hashlib
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
#for local
os.environ['APP_SETTING'] = "config.DevelopmentConfig"
os.environ['DATABESE_URL'] = "postgresql://postgres:1111@localhost/cafe"

#for heroku
app.config.from_object(os.environ['APP_SETTING'])
app.config('SQLALCHEMY_TRACK_MODIFICATION') = False


db =SQLAlchemy(app)


from db import Users, Menu, Review, Reservation, Order, Base

global_email = None
global_name = None

@app.route('/')
def main_page():
    return redirect('/menu')


@app.route('/sign_up',methods=['POST','GET'])
def regestration(email=None, name = None):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        birthday = request.form['birthday']
        try:
            password = hashlib.sha256(password.encode('ascii')).hexdigest()
            row = Users(name=name, email=email, password=password, birthday=birthday,
                        total_order_amount=0, discount=0)
            db.session.add(row)

            global global_email
            global_email = email

            global global_name
            global_name = name

            db.session.commit()
            #return render_template("menu.html", email=global_email, name=global_name)
            return redirect('/menu')

        except:
            print('This email is already used')

    else:
        return render_template("sign_up.html", email=global_email, name=name)



@app.route('/sign_in', methods=['POST','GET'])
def sign_in(email=None, name=None):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password = hashlib.sha256(password.encode('ascii')).hexdigest()
        try:
            check = db.session.query(Users).filter_by(email=email, password=password).all()
            global global_name
            for i in check:
                email = i.email
                global_name = i.name
            global global_email
            global_email = email
            #return render_template("menu.html", email=global_email, name=name)
            return redirect('/menu')


        except:
            return render_template('sign_in.html', email=email, name=global_name)
    else:
        return render_template('sign_in.html', email=global_email, name=name)

@app.route('/comments',methods=['POST','GET'])
def comment():
    if request.method == 'POST':
        email = global_email
        if email != None:
            comment = request.form ['comment']

            current_date = datetime.datetime.now()
            date = current_date.strftime("%d"), current_date.strftime("%b"), current_date.strftime("%Y")
            date = ' '.join(date)

            all = db.session.query(Review).all()
            i = 0
            for a in all:
                i = i+1

            row = Review(comment_id=i, name=global_name, email=email, comment=comment, date=date)
            db.session.add(row)
            query = db.session.query(Review).all()
            db.session.commit()
            return render_template('coment.html', comments=query, email=global_email, name=global_name)

        else:
            query = db.session.query(Review).all()
            return render_template('coment.html', comments=query)

    else:
        query = db.session.query(Review).all()
        email =global_email
        if email != None:
            search = db.session.query(Users).filter_by(email=email).all()
        return render_template('coment.html', comments=query, email=email,name=global_name)


@app.route('/reserv',methods=['POST','GET'])
def reserv():
    if request.method == 'POST':
        email = global_email
        if email != None:
            date = request.form['date']
            time = request.form['time']
            table = request.form['table']

            all = db.session.query(Reservation).all()
            list = []
            for a in all:
                list.append(a.reserv_id)

            if list == []:
                i = 1
            else:
                i = max(list)+1

            row = Reservation(reserv_id=i, name=global_name, email=email, table=table, date=date,
                              time=time, reserv_status='1')
            db.session.add(row)
            db.session.commit()
            #return render_template('menu.html', email=email, name=global_name)
            return redirect('/menu')
        else:
            return render_template('reserv.html', email=email)
    else:
        email = global_email
        #search = session.query(Users).filter_by(email=email).all()
        #for i in search:
        #    name = i.name

        return render_template('reserv.html', email=email, name=global_name)



@app.route('/menu',methods=['POST','GET'])
def menu():
    email = global_email
    if request.method == 'POST':
        item_id = request.form['index']
        item = request.form['item']
        if email != None:

            all = db.session.query(Order).all()
            list = []
            for a in all:
                list.append(a.order_id)

            if list ==[]:
                i = 1
            else:
                i = max(list) + 1

            row = Order(order_id=i, email=global_email, item_id=item_id, item=item, order_status=0)
            db.session.add(row)
            db.session.commit()
            return render_template('menu.html', email=email,name=global_name )

        else:
            return render_template('menu.html', email=email)
    else:
        email = global_email

        return render_template('menu.html', email=email, name=global_name)


@app.route('/order', methods=['POST', 'GET'])
def order():
    email = global_email
    if request.method == 'POST':
        delete = request.form['delete']
        item = request.form['item']
        if delete == 'on':
            delete_query = db.session.query(Order).filter_by(email=global_email, item=item, order_status=0).first()
            db.session.delete(delete_query)
            db.session.commit()
            orders = db.session.query(Order).filter_by(email=global_email, order_status=0).all()
            return render_template('order.html', email=global_email, name=global_name, orders=orders)

        table = request.form['table']
        index = 1


        for i in db.session.query(Order).filter_by(email=email).all():
            i.table = table
            db.session.merge(i)
            i.order_status = index
            db.session.merge(i)
        orders = 'abs'
        db.session.commit()

        return render_template('order.html', email=email, name=global_name, orders=orders)
    else:
        orders = db.session.query(Order).filter_by(email=global_email, order_status=0).all()

        return render_template('order.html', email=email, name=global_name, orders=orders)

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    global global_email
    global global_name
    email = global_email
    if email == None:
        return redirect('/sign_up')
    if request.method == 'POST':
        new_name = request.form['name']
        new_email = request.form['email']
        new_password = request.form['password']
        new_birthday = request.form['birthday']
        if new_name != '':
            for i in db.session.query(Users).filter_by(email=global_email).all():
                i.name = new_name
                db.session.merge(i)
                global_name = new_name
                db.session.commit()
        if new_email != '':
            for i in session.query(Users).filter_by(email=global_email).all():
                i.email = new_email
                db.session.merge(i)
                global_email = email
                db.session.commit()
        if new_password != '':
            new_password = hashlib.sha256(new_password.encode('ascii')).hexdigest()
            for i in session.query(Users).filter_by(email=global_email).all():
                i.password = new_password
                db.session.merge(i)
                db.session.commit()
        if new_birthday != '':
            for i in session.query(Users).filter_by(email=global_email).all():
                i.birthday = new_birthday
                db.session.merge(i)
                db.session.commit()
        user = db.session.query(Users).filter_by(email=global_email).all()
        return render_template('profile.html', email=global_email, name=global_name, user=user)
    else:
        user = db.session.query(Users).filter_by(email=global_email).all()
        return render_template('profile.html', email=global_email, name=global_name, user=user)




@app.route('/<action>', methods = ['GET'])
def actinfo(action):
    if action == "order.html":
        return redirect('/order')
    elif action == "menu.html":
        return redirect('/menu')
    elif action == "coment.html":
        return redirect('/comments')
    elif action == "profile.html":
        return redirect('/profile')
    elif action == "reserv.html":
        return redirect('/reserv')
    elif action == "sign_in.html":
        return redirect('/sign_in')
    elif action == "sign_up.html":
        return redirect('/sign_up')

if __name__ == "__main__":
    app.run()