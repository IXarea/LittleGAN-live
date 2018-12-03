from flask import make_response, jsonify, request, render_template, url_for
from . import app
from .form import UploadForm
from .helper import norm_input, model_generate


@app.route("/")
def index():
    return render_template("index.html", message="Hello World!")


@app.route("/discriminate")
def discriminate():
    upload_form = UploadForm()
    return render_template("discriminate.html", form=upload_form)


@app.route("/generate_adjust")
def generate_adjust():
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
    data['image'] = url_for("static", filename=filename)
    return jsonify(data)


@app.route("/api/discriminate", methods=['POST'])
def api_discriminate():
    f = request.files['image']
    response = make_response(f.read())
    response.headers['Content-Type'] = 'image/jpeg'
    return response
