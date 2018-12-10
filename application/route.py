from flask import jsonify, request, render_template, url_for
from . import app
from .helper import norm_input, model_generate, model_discriminate
from os import path
import hashlib


@app.route("/")
def index():
    return render_template("index.html", message="Hello World!")


@app.route("/discriminate")
def discriminate():
    return render_template("discriminate.html")


@app.route("/generate")
def generate():
    return render_template("generate.html")


@app.route("/api/list")
def api_list():
    return jsonify({
        "/api/list": "List of api",
        "/api/generate": "Generate Image",
        "/api/discriminate": "Discriminate Image"
    })


"""
@app.route("/api/info")
def api_info():
    return jsonify({
        "root_path": app.root_path,
        "instance_path": app.instance_path,
        "static_path": app.static_folder,
        "template_path": app.template_folder
    })
"""


@app.route("/api/generate", methods=['POST'])
def api_generate():
    data = request.get_json()
    data = norm_input(data)
    filename = model_generate(data)
    data['status'] = True
    data['image'] = url_for("static", filename=filename,_external=True)
    return jsonify(data)


@app.route("/api/discriminate", methods=['POST'])
def api_discriminate():
    image = request.files['image'].read()
    filename = "upload/%s.jpg" % hashlib.sha3_224(image).hexdigest()
    local_path = path.join(app.static_folder, filename)
    with open(local_path, "wb") as f:
        f.write(image)
    result = model_discriminate(image)
    result["image"] = url_for("static", filename=filename, _external=True)
    return jsonify(result)
