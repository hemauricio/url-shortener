from flask import Flask, request, jsonify

import server

app = Flask(__name__)

@app.route("/")
def index():
    return server.index()

@app.route("/<slug>", methods=["GET"])
def reroute(slug):
    return server.reroute(slug)

@app.route("/url", methods=["POST"])
def add_url():
    return server.add_url(request.json)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True, threaded=True)
