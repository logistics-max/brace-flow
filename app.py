from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///brace_qty_flow.db'
db = SQLAlchemy(app)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(100))
    size = db.Column(db.Integer)
    quantity = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50)) 

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clinic_name = db.Column(db.String(100))
    size = db.Column(db.Integer)
    quantity = db.Column(db.Integer, default=1) # Track how many were requested
    status = db.Column(db.String(50), default='Requested') 

@app.route('/')
def index():
    def get_inv(name, size):
        return Inventory.query.filter_by(location_name=name, size=size).first()
    
    clinics = Inventory.query.filter_by(category='Clinic').group_by(Inventory.location_name).all()
    requested = Request.query.filter_by(status='Requested').all()
    approved = Request.query.filter_by(status='Approved').all()
    accepted = Request.query.filter_by(status='Accepted').all()
    
    return render_template('index.html', clinics=clinics, get_inv=get_inv, 
                           requested=requested, approved=approved, accepted=accepted)

@app.route('/create_request', methods=['POST'])
def create_request():
    new_req = Request(
        clinic_name=request.form.get('clinic'), 
        size=int(request.form.get('size')),
        quantity=int(request.form.get('qty', 1)) # User enters qty here
    )
    db.session.add(new_req)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/approve/<int:id>')
def approve(id):
    req = Request.query.get(id)
    req.status = 'Approved'
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/accept/<int:id>')
def accept(id):
    req = Request.query.get(id)
    req.status = 'Accepted'
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete(id):
    req = Request.query.get(id)
    ws = Inventory.query.filter_by(location_name='Workshop', size=req.size).first()
    ws.quantity += req.quantity # Adds the full requested qty to workshop balance
    db.session.delete(req)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/transfer', methods=['POST'])
def transfer():
    sz = int(request.form.get('size'))
    mode = request.form.get('mode')
    qty = int(request.form.get('qty', 1))
    
    if mode == 'ws_to_store':
        src, dest = 'Workshop', 'Medical Store'
    else:
        src, dest = 'Medical Store', request.form.get('clinic')

    source_item = Inventory.query.filter_by(location_name=src, size=sz).first()
    dest_item = Inventory.query.filter_by(location_name=dest, size=sz).first()
    
    if source_item.quantity >= qty:
        source_item.quantity -= qty
        dest_item.quantity += qty
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with if __name__ == '__main__':
    app.run(debug=True)
        db.create_all()
        if Inventory.query.count() == 0:
            for loc in ["Workshop", "Medical Store"]:
                for s in range(4, 17):
                    db.session.add(Inventory(location_name=loc, size=s, category='Internal'))
            clinics_list = ["Abetech Gobena MCH", "Alert Comprehensive", "Black Lion Hospital", "CURE Addis Ababa", "St. Paul Abet", "St. Peters Specialized", "Tirunesh Beijing", "Yeka Kotebe", "Dubti Referral", "Abala/Mohammed Akle", "Debark General", "Debre Birhane Referral", "Debre Markos", "Debre Tabor", "Dessie Physical Rehab", "Dessie Referral", "Felege Hiwot", "Finote Selam", "Gondar University", "Injibara Hospital", "Kemise General", "Woldiya Specialized", "Asossa Hospital", "Grarbet Butajira", "Halaba Hospital", "Worabe Comprehensive", "Nigist Heleni Hossana", "Wolkite University", "Sabian General", "Gambela Referral", "Hiwot Fana Harar", "Dembi Dollo", "Shambu", "Gimbi and Ayra", "Adama Referral", "Adola Hospital", "Ambo Hospital", "Assela Referral", "Bale Goba", "Chiro Zonal", "Deder Hospital", "Gelemso General", "Jimma University", "Metu Karl Referral", "Moyale/Ginir", "Nekemt Referral", "Selale Comprehensive", "Shashemene General", "Wolisso St. Luke", "Bule Hora", "Konso", "Arbaminch PRC", "Dilla University", "Jinka Hospital", "Sawola General", "Wolaita Sodo", "Adare General", "Bona Hospital", "Hawassa Referral", "Yirgalem Hospital", "Gode Hospital", "Karamara/Jigjiga", "Filtu General", "Bonga Hospital", "Mizan Tepi University", "Addigrat Hospital", "Lemlem Karl Maichew", "Mekelle Referral", "St. Mary Axum", "Suhul Hospital"]
            for loc in clinics_list:
                for s in range(4, 17):
                    db.session.add(Inventory(location_name=loc, size=s, category='Clinic'))
            db.session.commit()
    app.run(debug=True)
