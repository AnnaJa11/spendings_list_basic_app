from flask import Flask, request, render_template, redirect, url_for
from forms import SpendingsForm
from models import spendings

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/spendings/", methods = ["GET", "POST"])
def spendings_list():
    form = SpendingsForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            spendings.create(form.data)
            spendings.save_all()
        return redirect(url_for("spendings_list"))
    return render_template("spendings.html", form=form, spendings=spendings.all(), error=error)

@app.route("/spendings/<int:spending_id>/", methods=["GET", "POST"])
def spending_details(spending_id):
    spending = spendings.get(spending_id -1)
    form = SpendingsForm(data=spending)

    if request.method == "POST":
        if form.validate_on_submit():
            spendings.update(spending_id-1, form.data)
        return redirect(url_for("spendings_list"))
    return render_template("spending.html", form=form, spending_id=spending_id)

if __name__ == "__main__":
    app.run(debug=True)
