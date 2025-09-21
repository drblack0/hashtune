from flask import Flask, jsonify, request
from app.api import scrape_hastag, scrape_profiles, get_gemini_response, scrape
from asgiref.wsgi import WsgiToAsgi
import asyncio

app = Flask(import_name=__name__)
asgi_app = WsgiToAsgi(app)

# CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

def run_async(coro):
    """Helper function to run async functions in sync context"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

@app.route("/", methods=["GET"])
def index():
    print("Root endpoint accessed")
    return jsonify({"message": "Hello, World!"})

@app.route("/scrape-hashtags", methods=["POST", "OPTIONS"])
def scrape_hashtags_route():
    if request.method == "OPTIONS":
        return "", 200
    data = request.json
    print(data.get("hashtags"))
    result = run_async(scrape_hastag(data["hashtags"]))
    return result

@app.route("/scrape-posts", methods=["POST", "OPTIONS"])
def scrape_posts_route():
    if request.method == "OPTIONS":
        return "", 200
    data = request.json
    print(data.get("usernames"))
    result = run_async(scrape_profiles(data["usernames"]))
    return result

@app.route("/get-post-ideas", methods=["POST", "OPTIONS"])
def get_post_ideas_route():
    if request.method == "OPTIONS":
        return "", 200
    data = request.json
    print(data.get("hashtags_used"), data.get("posts_used"))
    result = run_async(get_gemini_response(
        data.get("hashtags_used"), data.get("posts_used", False)
    ))
    return result

@app.route("/scrape-hashtags-and-posts", methods=["POST", "OPTIONS"])
def scrape_hashtags_and_posts_route():
    if request.method == "OPTIONS":
        print("OPTIONS request received")
        return "", 200
    
    print("=== SCRAPE REQUEST RECEIVED ===")
    data = request.json
    print(f"Hashtags: {data.get('hashtags')}")
    print(f"Profiles: {data.get('profiles')}")
    
    try:
        result = run_async(scrape(data.get("hashtags"), data.get("profiles")))
        print(f"Scrape result: {result}")
        return result
    except Exception as e:
        print(f"Error in scrape: {str(e)}")
        return jsonify({"error": str(e)}), 500
