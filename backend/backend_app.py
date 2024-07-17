from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)

SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={'app_name': 'Masterblog API'}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort, direction = request.args.get('sort'), request.args.get('direction', 'asc')
    if sort and sort not in ['title', 'content']:
        return jsonify({"error": "Invalid sort field"}), 400
    if direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid sort direction"}), 400
    sorted_posts = sorted(POSTS, key=lambda post: post[sort], reverse=(direction == 'desc')) if sort else POSTS
    return jsonify(sorted_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    title, content = data.get('title'), data.get('content')
    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400
    new_post = {"id": max(post['id'] for post in POSTS) + 1 if POSTS else 1, "title": title, "content": content}
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    global POSTS
    post_to_delete = next((post for post in POSTS if post['id'] == id), None)
    if not post_to_delete:
        return jsonify({"error": "Post not found"}), 404
    POSTS = [post for post in POSTS if post['id'] != id]
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    post_to_update = next((post for post in POSTS if post['id'] == id), None)
    if not post_to_update:
        return jsonify({"error": "Post not found"}), 404
    post_to_update.update({k: v for k, v in data.items() if k in ['title', 'content']})
    return jsonify(post_to_update), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query, content_query = request.args.get('title', ''), request.args.get('content', '')
    filtered_posts = [post for post in POSTS if
                      title_query.lower() in post['title'].lower() or content_query.lower() in post['content'].lower()]
    return jsonify(filtered_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)