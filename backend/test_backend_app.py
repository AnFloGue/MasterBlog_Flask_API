
import unittest
from flask import json
from backend_app import app


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Ensure there is a post with id=1
        response = self.app.post('/api/posts', data=json.dumps({"title": "First post", "content": "This is the first post."}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        post_id = response.json.get('id')
        self.assertIsNotNone(post_id)
        # Verify the post exists
        response = self.app.get(f'/api/posts/{post_id}')
        self.assertEqual(response.status_code, 200)
    def test_get_posts(self):
        response = self.app.get('/api/posts')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_add_post(self):
        new_post = {"title": "New post", "content": "This is a new post."}
        response = self.app.post('/api/posts', data=json.dumps(new_post), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_update_post(self):
        update_data = {"title": "Updated title"}
        response = self.app.put('/api/posts/1', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], "Updated title")

    def test_delete_post(self):
        response = self.app.delete('/api/posts/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)

    def test_search_posts(self):
        response = self.app.get('/api/posts/search?title=First')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

if __name__ == '__main__':
    unittest.main()