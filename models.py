from app import db
class Users(db.Model):

    __tablename__ = 'Users'

    email = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(80))
    name = db.Column(db.String(30))
    birthday = db.Column(db.Date)
    total_order_amount = db.Column(db.Integer)
    discount = db.Column(db.Integer)
    UniqueConstraint(email)

    def __init__(self, password, name, birthday, total_order_amount, discount):
        self.password = password
        self.name = name
        self.birthday = birthday
        self.total_order_amount = total_order_amount
        self.discount = discount

    def __repr__(self):
        return 'email{}'.format(self.email)

    def serialise(self):



class Menu(db.Model):

    __tablename__ = 'Menu'

    item_id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(30))
    price = db.Column(db.Integer)
    promotion = db.Column(db.Integer)


class Reservation(db.Model):

    __tablename__ = 'Reservation'

    reserv_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    name = db.Column(db.String(30))
    table = db.Column(db.Integer)
    date = db.Column(db.Date)
    time = db.Column(db.String(30))
    reserv_status = db.Column(db.Integer)
    db.UniqueConstraint(email)


class Review(db.Model):

    __tablename__ = 'Review'

    comment_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    name = db.Column(db.String(30))
    comment = db.Column(db.String(70))
    date = db.Column(db.Date)


class Order(db.Model):
    __tablename__ = 'Order'

    order_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    item_id = db.Column(db.Integer)
    item = db.Column(db.String(30))
    table = db.Column(db.Integer)
    order_status = db.Column(db.Integer)