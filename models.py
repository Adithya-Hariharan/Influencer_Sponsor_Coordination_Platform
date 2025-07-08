from app import app

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(256), nullable = False) 


class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32))
    category = db.Column(db.String(20))
    reach = db.Column(db.Numeric(15,0))
    username = db.Column(db.String(32))
    password = db.Column(db.String(256), nullable = False)
    
    ad_requests = db.relationship(('Ad_request'), backref = 'influencer') 
    # ad_negotiate = db.relationship(('Ad_request'), backref = 'sponsor') 

class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40))
    industry = db.Column(db.String(32))
    username = db.Column(db.String(32))
    password = db.Column(db.String(256), nullable = False)
    
    sponsors = db.relationship('Campaign', backref = 'sponsor')

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'))
    title = db.Column(db.String(32))
    desc = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Integer)

    campaign = db.relationship('Ad_request', backref = 'campaign')
    
class Ad_request(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    payment_amount = db.Column(db.Integer)
    proposed_amount = db.Column(db.Integer)
    status = db.Column(db.Enum('Pending', 'Accepted', 'Rejected','Negotiation'), default = 'Pending')


with app.app_context():
    db.create_all()
    admin = Admin.query.first()
    if not admin:
        admin = Admin(username = 'admin', password = 'Admin!12')
        db.session.add(admin)
        db.session.commit()


