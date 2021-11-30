from flask import Flask, render_template, request, redirect
from models import db, EmployeeModel

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/')
def index():
    return render_template("index.html", title="Flask CRUD")


@app.route("/data/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("createpage.html", titel="Create data")

    if request.method == "POST":
        employee_id = request.form["employee_id"]
        name = request.form["name"]
        age = request.form["age"]
        position = request.form["position"]
        employee = EmployeeModel(
            employee_id=employee_id, name=name, age=age, position=position)
        db.session.add(employee)
        db.session.commit()
        return redirect("/data")


@app.route("/data")
def RetrieveList():
    employees = EmployeeModel.query.all()
    return render_template("datalist.html", employees=employees, title="Datalist")


@app.route("/data/<int:id>", methods=["GET", "POST"])
def RetrieveEmployee(id):
    if request.method == "POST":
        employee = EmployeeModel.query.filter_by(employee_id=id).first()
        if employee:
            return render_template("data.html", employee=employee, title="Data")
        return f"Employee with id ={id} Doenst exist"


@app.route("/data/<int:id>/update", methods=["GET", "POST"])
def update(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == "POST":
        if employee:
            db.session.delete(employee)
            db.session.commit()
            name = request.form["name"]
            age = request.form["age"]
            position = request.form["position"]
            employee = EmployeeModel(
                employee_id=id, name=name, age=age, position=position)
            db.session.add(employee)
            db.session.commit()
            return redirect(f"/data")

    return render_template("update.html", employee=employee, title="Update")


@app.route("/data/<int:id>/delete", methods=["GET", "POST"])
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == "POST":
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return redirect("/data")
        abort(404)

    return render_template("delete.html", title="Delete")
