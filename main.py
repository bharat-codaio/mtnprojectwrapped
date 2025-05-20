import base64
import os
import time

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    send_from_directory,
)
import pandas as pd


ASSETS_DIR = "attached_assets"

app = Flask(__name__)


@app.route("/")
def index():
    data = {}
    return render_template("index.html", data=data)


@app.route("/upload", methods=["POST"])
def upload():
    data = None
    uploaded_file = request.files.get("csvFile")
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
    else:
        url = request.form["profileURL"]
        if request.form["profileURL"][-1] != "/":
            url = url + "/"
        url = url + "tick-export"
        data = pd.read_csv(url)

    this_year = data[(data["Date"] >= "2024-01-01")]
    routes = this_year.Route.nunique()
    locations = this_year.Location.nunique()
    max_crag = "Not enough data :("
    if locations > 0:
        full_path = (
            this_year.groupby(["Location"])["Location"].count().idxmax()
        )
        path_parts = full_path.split(">")
        max_crag = path_parts[-1].strip()

    max_type = "Not enough data :("
    max_route = "Not enough data :("
    if routes > 0:
        max_type = (
            this_year.groupby(["Route Type"])["Route Type"].count().idxmax()
        )
        max_route = this_year["Route"][this_year["Your Stars"].idxmax()]

    number_days = this_year["Date"].nunique()
    climbing_style = (
        max_type.lower() if max_type != "Not enough data :(" else "sport"
    )
    return render_template(
        "data.html",
        routes=routes,
        locations=locations,
        max_crag=max_crag,
        max_type=max_type,
        max_route=max_route,
        number_days=number_days,
        climbing_style=climbing_style,
    )


@app.route("/save-image", methods=["POST"])
def save_image():
    data = request.get_json(silent=True) or {}
    image_data = data.get("imageData")
    if not image_data:
        return jsonify({"error": "Missing image data"}), 400

    if image_data.startswith("data:image"):
        image_data = image_data.split(",", 1)[1]

    try:
        image_bytes = base64.b64decode(image_data)
    except (base64.binascii.Error, TypeError):
        return jsonify({"error": "Invalid image data"}), 400

    os.makedirs(ASSETS_DIR, exist_ok=True)
    filename = f"image_{int(time.time()*1000)}.png"
    filepath = os.path.join(ASSETS_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(image_bytes)

    url = f"/{ASSETS_DIR}/{filename}"
    return jsonify({"url": url})


@app.route(f"/{ASSETS_DIR}/<path:filename>")
def serve_image(filename):
    return send_from_directory(ASSETS_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

