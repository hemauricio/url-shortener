from flask import Flask, request, jsonify, redirect
from utils import new_slug, validate_slug

from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()

# url_shortener is the name of my db
db = client.url_shortener

# urls is the collection name
urls = db.urls

@app.route('/')
def index():
    # print urls.find_one({"slug":"mau"})
    return 'URL Shortener... In Python! ... But Python 2.7 :('

@app.route('/<slug>', methods=['GET'])
def reroute(slug):

    query = urls.find_one({"slug": slug.lower()})

    if not query:
        return "Slug not found"

    url = query.get("url")

    return redirect(url, code=302)

@app.route('/url', methods=['POST'])
def add_url():

    payload = request.json
    url = payload.get('url')
    slug = payload.get('slug', new_slug())

    # NOTE: What would happen if someone tries to save a slug to redirect to
    # the shortener URL ?

    # if 'short.ener' in url:
    #     # TODO: Fix ugly exception (maybe?)
    #     raise Exception('Don\'t')

    # Validate slug has only ascii characters
    valid = validate_slug(slug)

    if not valid:
        return jsonify({"status": "Failure",
                        "message": "Slug contains not only ascii characters"})

    # Check whether the slug is already in use
    query = urls.find_one({"slug": slug.lower()})

    if query:
        return jsonify({"status": "Failure",
                        "message": "Slug already in use"})

    # Add slug and URL to DB
    doc = {
        "url": url,
        "slug": slug.lower()
    }

    urls.insert_one(doc)

    return jsonify({
        'status': 'Success',
        'url': url,
        'slug': slug
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True, threaded=True)
