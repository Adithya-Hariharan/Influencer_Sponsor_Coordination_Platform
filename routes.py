from flask import render_template, request, flash, redirect, url_for, session
from app import app
from models import *
from functions import *
from datetime import datetime

#index
@app.route('/')
def index():
    return render_template('index.html')

#admin

@app.route('/admin_login')
def admin_login():
    return render_template('admin/admin_login.html')

@app.route('/admin_login', methods = ['POST'])
def admin_login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    admin = Admin.query.filter_by(username = username).first()
    if not admin:
        flash('Username does not exist')
        return redirect(url_for('admin_login'))
    
    if admin.password != password:
        flash('Incorrect password, try again')
        return redirect(url_for('admin_login'))
    
    session['user_id'] = admin.id
    session['user_role'] = 'admin'
    flash("login successful")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_profile')
@auth_required('admin')
def admin_profile():
    admin = Admin.query.get(session['user_id'])
    if not admin:
        flash('User not found')
        return redirect(url_for('admin_login'))
    return render_template('admin/admin_profile.html', admin = admin)
    
@app.route('/admin_logout')
@logout_required('admin')
def admin_logout():
    return redirect(url_for('admin_login'))

@app.route('/admin_dashboard')
@auth_required('admin')
def admin_dashboard():
    influencers=[]
    sponsors=[]
    campaigns = Campaign.query.all()
    campaign_details = []
    for campaign in campaigns:
        ad_requests = Ad_request.query.filter_by(campaign_id=campaign.id).all()
        ad_request_details = [{
            'id': ad_request.id,
            'influencer_id': ad_request.influencer_id,
            'payment_amount': ad_request.payment_amount,
            'proposed_amount': ad_request.proposed_amount,
            'status': ad_request.status
        } for ad_request in ad_requests]
        
        campaign_details.append({
            'id': campaign.id,
            'title': campaign.title,
            'desc': campaign.desc,
            'start_date': campaign.start_date,
            'end_date': campaign.end_date,
            'budget': campaign.budget,
            'ad_requests': ad_request_details
        })
        influencers = Influencer.query.all()
        sponsors = Sponsor.query.all()
    
    return render_template('admin/admin_dashboard.html', campaigns=campaign_details, influencers=influencers, sponsors=sponsors)


#influencer

@app.route('/influencer_login')
def influencer_login():
    return render_template('influencer/influencer_login.html')

@app.route('/influencer_login', methods = ['POST'])
def influencer_login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    influencer = Influencer.query.filter_by(username = username).first()

    if not influencer:
        flash('Username does not exist')
        return redirect(url_for('influencer_login'))
    
    if influencer.password != password:
        flash('Incorrect password, try again')
        return redirect(url_for('influencer_login'))
    session['user_id'] = influencer.id
    session['user_role'] = 'influencer'
    flash("login successful")
    return redirect(url_for('influencer_dashboard'))


@app.route('/i_reg')
def influencer_registeration():
    return render_template('influencer/i_reg.html')

@app.route('/i_reg', methods = ['POST'])
def influencer_reg_post():
    name = request.form.get('name')
    username  = request.form.get('username')
    password = request.form.get('password')
    category = request.form.get('category')
    

    influencer = Influencer.query.filter_by(username = username).first()

    if influencer:
        flash('Username already exists')
        return redirect(url_for('influencer_registeration'))
    new_user = Influencer(name=name, username = username, password = password, category = category )
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('influencer_login'))

@app.route('/influencer_profile')
@auth_required('influencer')
def influencer_profile():
    influencer = Influencer.query.get(session['user_id'])
    if not influencer:
        flash('User not found')
        return redirect(url_for('influencer_login'))
    return render_template('influencer/influencer_profile.html', influencer=influencer)

@app.route('/influencer_logout')
@logout_required('influencer')
def influencer_logout():
    return redirect(url_for('influencer_login'))

@app.route('/influencer_dashboard')
@auth_required('influencer')
def influencer_dashboard():
    influencer = Influencer.query.get(session['user_id'])
    ad_requests = Ad_request.query.filter_by(influencer_id=influencer.id).all()
    requested_campaigns = []
    for ad_request in ad_requests:
        campaign = Campaign.query.get(ad_request.campaign_id)
        if campaign:
            requested_campaigns.append({'campaign':campaign,'ad_request':[ad_request]})
            
    return render_template('influencer/influencer_dashboard.html', campaigns=requested_campaigns)

#sponsor

@app.route('/sponsor_login')
def sponsor_login():
    return render_template('sponsor/sponsor_login.html')

@app.route('/sponsor_login', methods = ['POST'])
def sponsor_login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    sponsor = Sponsor.query.filter_by(username = username).first()

    if not sponsor:
        flash('Username does not exist')
        return redirect(url_for('sponsor_login'))
    if sponsor.password != password:
        flash('Incorrect password, try again')
        return redirect(url_for('sponsor_login'))
    session['user_id'] = sponsor.id
    session['user_role'] = 'sponsor'
    flash("login successful")
    return redirect(url_for('sponsor_dashboard'))

@app.route('/s_reg')
def sponsor_registeration():
    return render_template('sponsor/s_reg.html')

@app.route('/s_reg', methods = ['POST'])
def sponsor_reg_post():
    name = request.form.get('name')
    username  = request.form.get('username')
    password = request.form.get('password')
    industry = request.form.get('industry')

    sponsor = Sponsor.query.filter_by(username = username).first()

    if sponsor:
        flash('Username already exists')
        return redirect(url_for('sponsor_registeration'))
    new_user = Sponsor(name=name, username = username, password = password, industry = industry)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('sponsor_login'))

@app.route('/sponsor_profile')
@auth_required('sponsor')
def sponsor_profile():
    sponsor = Sponsor.query.get(session['user_id'])
    if not sponsor:
        flash('User not found')
        return redirect(url_for('sponsor_login'))
    return render_template('sponsor/sponsor_profile.html', sponsor=sponsor)

@app.route('/sponsor_logout')
@logout_required('sponsor')
def sponsor_logout():
    return redirect(url_for('sponsor_login'))

@app.route('/sponsor_dashboard')
@auth_required('sponsor')
def sponsor_dashboard():      
    return render_template('sponsor/sponsor_dashboard.html')

#campaign

@app.route('/campaign')
@auth_required('sponsor')
def campaign():
    campaigns = Campaign.query.all()
    influencers = Influencer.query.all()    
    campaign_details = []
    for campaign in campaigns:
        ad_requests = Ad_request.query.filter_by(campaign_id=campaign.id).all()
        ad_request_details = [{
            'influencer_name': Influencer.query.get(ad_request.influencer_id).name,
            'proposed_amount': ad_request.proposed_amount,
            'status': ad_request.status
        } for ad_request in ad_requests]
        
        campaign_details.append({'id': campaign.id,'title': campaign.title,'desc': campaign.desc,'start_date': campaign.start_date,'end_date': campaign.end_date,'budget': campaign.budget,'ad_requests': ad_request_details})
    return render_template('campaign/campaign.html', campaigns=campaign_details, influencers=influencers)

@app.route('/campaign/add')
@auth_required('sponsor')
def add_campaign():
    return render_template('campaign/add.html')


@app.route('/campaign/add', methods = ['POST'])
@auth_required('sponsor')
def add_campaign_post():
    title = request.form.get('title')
    budget = request.form.get('budget')
    desc = request.form.get('desc')
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    campaign = Campaign(title=title, budget = budget, desc=desc, start_date = start_date, end_date=end_date)

    db.session.add(campaign)
    db.session.commit()
    flash('Campaign added successfully')
    return redirect(url_for('campaign'))


@app.route('/campaign/<int:id>/edit')
@auth_required('sponsor')
def edit_campaign(id):
    campaign = Campaign.query.get(id)
    return render_template('campaign/edit.html', campaign=campaign)

@app.route('/campaign/<int:id>/edit', methods = ['POST'])
@auth_required('sponsor')
def edit_campaign_post(id):

    campaign = Campaign.query.get(id)
    title = request.form.get('title')
    budget = request.form.get('budget')
    desc = request.form.get('desc')
    visibility = request.form.get('visibility')
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    
    campaign.title = title
    campaign.budget = budget
    campaign.desc = desc
    campaign.visibility = visibility
    campaign.start_date = start_date
    campaign.end_date = end_date

    db.session.commit()
    flash('Campaign updated successfully')
    return redirect(url_for('campaign'))

@app.route('/campaign/<int:id>/delete')
@auth_required('sponsor')
def delete_campaign(id):
    campaign = Campaign.query.get(id)
    return render_template('campaign/delete.html', campaign  = campaign)

@app.route('/campaign/<int:id>/delete', methods = ['POST'])
@auth_required('sponsor')
def delete_campaign_post(id):
    campaign = Campaign.query.get(id)
    db.session.delete(campaign)
    db.session.commit()
    flash('campaign deleted successfully')
    return redirect(url_for('campaign'))


@app.route('/campaign/<int:id>/request_ad', methods = ['POST'])
def request_ad(id):
    search_influencers = request.form.getlist('influencers')
    campaign = Campaign.query.get(id)
    
    for influencer_id in search_influencers:
        ad_request = Ad_request.query.filter_by(influencer_id=influencer_id, campaign_id=id).first()
        if not ad_request:
            ad_request = Ad_request(influencer_id=influencer_id, campaign_id=id, payment_amount=campaign.budget)
            db.session.add(ad_request)
        db.session.commit()
    flash('Ad request sent successfully')
    return redirect(url_for('campaign'))
    

@app.route('/influencer_dashboard/accept_ad/<int:ad_request_id>', methods=['POST'])
@auth_required('influencer')
def accept_ad(ad_request_id):
    ad_request = Ad_request.query.get(ad_request_id)
    if ad_request:
        ad_request.status = 'Accepted'
        db.session.commit()
        flash('Ad request accepted successfully')
    else:
        flash('Ad request not found')
    return redirect(url_for('influencer_dashboard'))


@app.route('/influencer_dashboard/reject_ad/<int:ad_request_id>', methods=['POST'])
@auth_required('influencer')
def reject_ad(ad_request_id):
    ad_request = Ad_request.query.get(ad_request_id)
    if ad_request:
        ad_request.status = 'Rejected'
        db.session.commit()
        flash('Ad request rejected successfully')
    else:
        flash('Ad request not found')
    return redirect(url_for('influencer_dashboard'))


@app.route('/influencer_dashboard/negotiate_ad/<int:ad_request_id>', methods=['GET', 'POST'])
def negotiate_ad(ad_request_id):
    ad_request = Ad_request.query.get(ad_request_id)
    if not ad_request:
        flash('Ad request not found')
        return redirect(url_for('influencer_dashboard'))

    if request.method == 'POST':
        proposed_amount = request.form.get('proposed_amount', type=int)
        ad_request.proposed_amount = proposed_amount
        ad_request.status = 'Negotiation'
        db.session.commit()
        flash('Negotiation proposal sent successfully.')
        return redirect(url_for('influencer_dashboard')) 
    return render_template('ad_neg.html', ad_request=ad_request)

# @app.route('/influencer_dashboard/negotiate_ad/<int:ad_request_id>', methods=['GET','POST'])
# @auth_required('influencer')
# def negotiate_ad(ad_request_id):
#     ad_request = Ad_request.query.get(ad_request_id)
#     if request.method == 'POST':
#         proposed_amount = request.form.get('proposed_amount', type=int)
#         ad_request.proposed_amount = proposed_amount
#         ad_request.status = 'Negotiation'
#         db.session.commit()
#         flash('Negotiation proposal sent successfully.')
#         return redirect(url_for('influencer_dashboard'))
#     return render_template('influencer/negotiate_ad.html', ad_request=ad_request)