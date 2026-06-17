from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import joblib
import re
from datetime import datetime


app = Flask(__name__)


# Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'

db = SQLAlchemy(app)


# Load ML model

model = joblib.load("health_model.pkl")


# Patient Table

class Patient(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    dob = db.Column(db.String(20))

    email = db.Column(db.String(100))

    glucose = db.Column(db.Float)

    haemoglobin = db.Column(db.Float)

    cholesterol = db.Column(db.Float)

    remarks = db.Column(db.String(200))



# Validation

def validate_data(email, dob, glucose, haemoglobin, cholesterol):


    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'


    if not re.match(email_pattern,email):

        return "Invalid Email"


    dob_date = datetime.strptime(dob,"%Y-%m-%d")


    if dob_date > datetime.today():

        return "Future DOB not allowed"



    if glucose < 0 or haemoglobin < 0 or cholesterol < 0:

        return "Values cannot be negative"


    return None





# Home Page (READ)

@app.route("/")
def home():


    patients = Patient.query.all()


    return render_template(
        "index.html",
        patients=patients
    )





# ADD Patient (CREATE)

@app.route("/add", methods=["POST"])

def add():


    name=request.form["name"]

    dob=request.form["dob"]

    email=request.form["email"]


    try:

        glucose=float(request.form["glucose"])

        haemoglobin=float(request.form["haemoglobin"])

        cholesterol=float(request.form["cholesterol"])


    except:

        return "Only numbers allowed"



    error=validate_data(
        email,
        dob,
        glucose,
        haemoglobin,
        cholesterol
    )


    if error:

        return error



    prediction=model.predict(
        [[glucose,
        haemoglobin,
        cholesterol]]
    )[0]



    patient=Patient(

        name=name,
        dob=dob,
        email=email,
        glucose=glucose,
        haemoglobin=haemoglobin,
        cholesterol=cholesterol,
        remarks=prediction

    )


    db.session.add(patient)

    db.session.commit()


    return redirect("/")





# Edit Page

@app.route("/edit/<int:id>")

def edit(id):


    patient=Patient.query.get(id)


    return render_template(
        "update.html",
        patient=patient
    )





# UPDATE

@app.route("/update/<int:id>",
methods=["POST"])

def update(id):


    patient=Patient.query.get(id)



    patient.name=request.form["name"]

    patient.dob=request.form["dob"]

    patient.email=request.form["email"]


    patient.glucose=float(request.form["glucose"])

    patient.haemoglobin=float(
        request.form["haemoglobin"]
    )

    patient.cholesterol=float(
        request.form["cholesterol"]
    )



    patient.remarks=model.predict(

        [[
        patient.glucose,
        patient.haemoglobin,
        patient.cholesterol
        ]]

    )[0]


    db.session.commit()


    return redirect("/")






# DELETE

@app.route("/delete/<int:id>")

def delete(id):


    patient=Patient.query.get(id)


    db.session.delete(patient)

    db.session.commit()


    return redirect("/")





if __name__=="__main__":


    with app.app_context():

        db.create_all()


    app.run(debug=True)