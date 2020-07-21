from flask import Flask, request, jsonify, redirect
from utils import new_slug

app = Flask(__name__)

@app.route('/')
def index():
    return 'URL Shortener... In Python! ... But Python 2.7 :('

@app.route('/<id>', methods=['GET'])
def reroute(id):
    # TODO: Get the actual URL from the DB given the id
    url = 'https://google.com' if id != 'mau' else 'https://mau-frbs.dev'

    # TODO: Redirect to saved URL
    return redirect(url, code=302)

@app.route('/url', methods=['POST'])
def add_url():

    payload = request.json
    url = payload.get('url')
    slug = payload.get('slug', new_slug())

    # NOTE: What would happen if someone tries to save a slug to redirect to
    # the shortener URL ?
    # We'll use localhost in this example

    if 'short.ener' in url:
        # TODO: Fix ugly exception (maybe?)
        raise Exception('Don\'t')

    # TODO: validate slug or create one in case no slug was provided

    # TODO: check whether the slug is already in use

    # TODO: Add slug and URL to DB

    return jsonify({
        'status': 'Success',
        'url': url,
        'slug': slug
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True, threaded=True)
