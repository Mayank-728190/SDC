from flask import request, jsonify
from bson.objectid import ObjectId
from auth import requires_auth

def setup_routes(app, db):
    @app.route('/blogs', methods=['POST'])
    @requires_auth
    def create_blog():
        data = request.get_json()
        blog_id = db.blogs.insert_one({
            'title': data['title'],
            'content': data['content']
        }).inserted_id
        return jsonify({"message": "Blog created", "id": str(blog_id)}), 201

    @app.route('/blogs', methods=['GET'])
    def get_blogs():
        blogs = db.blogs.find()
        return jsonify([{"id": str(blog["_id"]), "title": blog["title"]} for blog in blogs])

    @app.route('/blogs/<id>', methods=['GET'])
    def get_blog(id):
        blog = db.blogs.find_one({"_id": ObjectId(id)})
        if blog:
            return jsonify({"id": str(blog["_id"]), "title": blog["title"], "content": blog["content"]})
        return jsonify({"message": "Blog not found"}), 404

    @app.route('/blogs/<id>', methods=['PUT'])
    @requires_auth
    def update_blog(id):
        data = request.get_json()
        result = db.blogs.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.matched_count:
            return jsonify({"message": "Blog updated"})
        return jsonify({"message": "Blog not found"}), 404

    @app.route('/blogs/<id>', methods=['DELETE'])
    @requires_auth
    def delete_blog(id):
        result = db.blogs.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return jsonify({"message": "Blog deleted"})
        return jsonify({"message": "Blog not found"}), 404

    @app.route('/blogs/<id>/comments', methods=['POST'])
    @requires_auth
    def add_comment(id):
        data = request.get_json()
        db.blogs.update_one({"_id": ObjectId(id)}, {"$push": {"comments": data['comment']}})
        return jsonify({"message": "Comment added"})

    @app.route('/blogs/<id>/like', methods=['PUT'])
    def add_like(id):
        db.blogs.update_one({"_id": ObjectId(id)}, {"$inc": {"likes": 1}})
        return jsonify({"message": "Like added"})