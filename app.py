from flask import Flask, request, render_template, redirect, url_for, jsonify, abort, make_response
from forms import SpendingsForm
from models import spendings


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/api/v1/spendings/", methods=["GET"])
def spendings_list_api_v1():
    return jsonify(spendings.all())

@app.route("/api/v1/spendings/<int:spending_id>", methods=["GET"])
def get_spending(spending_id):
    spending = spendings.get(spending_id)
    if not spending:
        abort(404)
    return jsonify({"spending": spending})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.route("/api/v1/spendings/", methods=["POST"])
def create_spending():
    if not request.json or not 'title' in request.json:
        abort(400)
    spending = {
        'id': spendings.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'amount': request.json.get('amount', "")
    }
    spendings.create(spending)
    return jsonify({'spending': spending}), 201

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.route("/api/v1/spendings/<int:spending_id>", methods=['DELETE'])
def delete_spending(spending_id):
    result = spendings.delete(spending_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/spendings/<int:spending_id>", methods=["PUT"])
def update_spending(spending_id):
    spending = spendings.get(spending_id)
    if not spending:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'amount' in data and not isinstance(data.get('amount'), float)
    ]):
        abort(400)
    spending = {
        'title': data.get('title', spending['title']),
        'description': data.get('description', spending['description']),
        'amount': data.get('amount', spending['amount'])
    }
    spendings.update(spending_id, spending)
    return jsonify({'spending': spending})



# ------------------------
@app.route("/spendings/", methods = ["GET", "POST"])
def spendings_list():
    form = SpendingsForm()
    # id = spendings.all()[-1]['id'] + 1
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
