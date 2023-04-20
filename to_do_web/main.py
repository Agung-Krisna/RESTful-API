from flask import Flask, render_template, request
import requests
from asgiref.wsgi import WsgiToAsgi


app = Flask(__name__)

API_ENDPOINT = "http://127.0.0.1:8000/"

@app.get("/")
def home():
    try:
        json_list = requests.get(API_ENDPOINT+"list_todos").json()
    except:
        return "can't find the API endpoint"
    return render_template("home.html", todos=json_list, api_endpoint=API_ENDPOINT)

@app.get("/description")
def description():
    return render_template('description.html')

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

asgi = WsgiToAsgi(app)