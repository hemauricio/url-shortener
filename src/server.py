from flask import redirect, jsonify
from utils import new_slug, validate_slug
from pymongo import MongoClient

client = MongoClient()

# url_shortener is the name of my db
db = client.url_shortener

# urls is the collection name
urls = db.urls

def index():
    return jsonify({
        "message": "Url shortener!"
    })

def reroute(slug):

    query = urls.find_one({"slug": slug.lower()})

    if not query:
        return jsonify({
            "status": "Failure",
            "message":"Slug not found"
        })

    url = query.get("url")

    return redirect(url, code=302)

def add_url(payload):

    url = payload.get("url")
    slug = payload.get("slug", new_slug())

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
        "status": "Success",
        "url": url,
        "slug": slug
    })
