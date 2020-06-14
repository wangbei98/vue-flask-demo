from flask import Flask, render_template
from flask_restful import Api
from apis.testapi import TestAPI
from flask_cors import CORS


app = Flask(__name__,
            static_folder = "../dist/static",
            template_folder = "../dist")


api = Api(app)
# 请求跨域
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


api.add_resource(TestAPI, '/api/test', endpoint='test')