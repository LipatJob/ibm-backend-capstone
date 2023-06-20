from flask import Flask, make_response, request

app = Flask(__name__)
data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "d64efd92-ca8e-40da-b234-47e6403eb167",
        "first_name": "Ferdy",
        "last_name": "Garrow",
        "graduation_year": 1970,
        "address": "10 Wayridge Terrace",
        "city": "North Little Rock",
        "zip": "72199",
        "country": "United States",
        "avatar": "http://dummyimage.com/148x100.png/dddddd/000000",
    },
    {
        "id": "66c09925-589a-43b6-9a5d-d1601cf53287",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "graduation_year": 1985,
        "address": "637 Carey Pass",
        "city": "Gainesville",
        "zip": "32627",
        "country": "United States",
        "avatar": "http://dummyimage.com/174x100.png/ff4444/ffffff",
    },
    {
        "id": "0dd63e57-0b5f-44bc-94ae-5c1b4947cb49",
        "first_name": "Abdel",
        "last_name": "Duke",
        "graduation_year": 1995,
        "address": "2 Lake View Point",
        "city": "Shreveport",
        "zip": "71105",
        "country": "United States",
        "avatar": "http://dummyimage.com/145x100.png/dddddd/000000",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    }
]


@app.route("/")
def index():
    return {
        "message": "Hello world"
    }


@app.route("/no_content")
def no_content():
    return {
        "message": "No content found"
    }, 204


@app.route("/exp")
def index_explicit():
    res = make_response({
        "message": "Hello world"
    })
    res.status_code = 200
    return res


@app.route("/data")
def get_data():
    try:
        if data and len(data) > 0:
            return {"message": f"Data of length {len(data)} found"}
        else:
            return {"message": "Data is empty"}, 500
    except NameError:
        return {"message": "Data not found"}, 404


@app.route("/name_search")
def name_search():
    # validate request query parameters
    if "q" not in request.args:
        return {"message": "Invalid input parameter"}, 422
    first_name = request.args["q"]

    matches = [info for info in data if info.get(
        "first_name").lower() == first_name.lower()]
    if any(matches):
        return matches[0], 400
    else:
        return {"message": "Person not found"}, 400


@app.route("/count")
def count():
    return {"count": len(data)}

@app.route("/person/<uuid:uuid>", methods=["GET"])
def get_person(uuid):
    matches = [info for info in data if info.get("id") == str(uuid)]
    if any(matches):
        return matches[0], 200
    else:
        return {"message":"Person cannot be found"}, 404

@app.route("/person/<uuid:uuid>", methods=["DELETE"])
def delete_person(uuid):
    matches = [info for info in data if info.get("id") == str(uuid)]
    if any(matches):
        data.remove(matches[0])
        return {"deleted_id": str(uuid)}, 200
    else:
        return {"message":"Person cannot be found"}, 404

@app.route("/person", methods = ["POST"])
def add_by_uid():
    new_person = request.json
    if not new_person:
        return {"message": "Invalid body"}, 400
    data.append(new_person)
    return {"message": f"User with UUID {new_person['id']} was added"}, 200

@app.errorhandler(404)
def handle_404(e):
    return {
        "message": "404 Endpoint Not Found"
    }


@app.errorhandler(500)
def handle_500(e):
    return {
        "message": "500 Internal Server Error"
    }


def __main__():
    app.run()
