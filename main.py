import tornado.ioloop
import tornado.web
import requests
import json

class UserHandler(tornado.web.RequestHandler):
    API_URL = "http://172.18.0.3:3000/user"

    def get(self, user_id=None):
        if user_id:
            response = requests.get(f"{self.API_URL}/{user_id}")
            user_data = response.json()  # Asume que la respuesta es JSON
            self.render("user.html", user=user_data)
        else:
            response = requests.get(self.API_URL)
            users_data = response.json()  # Asume que la respuesta es JSON
            self.render("users.html", users=users_data)  # Asegúrate de que el archivo HTML se llama 'users.html'

    def post(self):
        user_data = {
            "username": self.get_argument("username"),
            "email": self.get_argument("email"),
            "password": self.get_argument("password"),
            "profile_picture": self.get_argument("profile_picture"),
            "bio": self.get_argument("bio")
        }
        response = requests.post(self.API_URL, json=user_data)
        # Redirecciona de vuelta a la página de usuarios después de crear uno
        self.redirect("/user")
    def put(self, user_id):
        user_data = json.loads(self.request.body)
        response = requests.put(f"{self.API_URL}/{user_id}", json=user_data)
        self.write(response.text)

    def delete(self, user_id):
        response = requests.delete(f"{self.API_URL}/{user_id}")
        self.write(response.text)

class StoriesHandler(tornado.web.RequestHandler):
    API_URL = "http://172.18.0.3:3000/stories"

    def get(self):
        response = requests.get(self.API_URL)
        stories_data = response.json()  # Asume que la respuesta es JSON
        self.render("stories.html", stories=stories_data)  # Asegúrate de que el archivo HTML se llama 'stories.html'

    def post(self):
        story_data = {
            "user_id": self.get_argument("user_id"),
            "image_url": self.get_argument("image_url"),
            "caption": self.get_argument("caption")
        }
        response = requests.post(self.API_URL, json=story_data)
        self.redirect("/stories")

    def put(self, story_id):
        update_data = json.loads(self.request.body)
        response = requests.put(f"{self.API_URL}/{story_id}", json=update_data)
        self.write(response.text)

    def delete(self, story_id):
        response = requests.delete(f"{self.API_URL}/{story_id}")
        self.write(response.text)

class PostsHandler(tornado.web.RequestHandler):
    API_URL = "http://172.18.0.3:3000/posts"

    def get(self):
        response = requests.get(self.API_URL)
        posts_data = response.json()  # Asume que la respuesta es JSON
        self.render("posts.html", posts=posts_data)  # Asegúrate de que el archivo HTML se llama 'posts.html'

    def post(self):
        post_data = {
            "user_id": self.get_argument("user_id"),
            "image_url": self.get_argument("image_url"),
            "caption": self.get_argument("caption")
        }
        response = requests.post(self.API_URL, json=post_data)
        self.redirect("/posts")

    def put(self, post_id):
        update_data = json.loads(self.request.body)
        response = requests.put(f"{self.API_URL}/{post_id}", json=update_data)
        self.write(response.text)

    def delete(self, post_id):
        response = requests.delete(f"{self.API_URL}/{post_id}")
        self.write(response.text)

class NotificationsHandler(tornado.web.RequestHandler):
    API_URL = "http://172.18.0.3:3000/notifications"

    def get(self, notification_id=None):
        if notification_id:
            response = requests.get(f"{self.API_URL}/{notification_id}")
        else:
            response = requests.get(self.API_URL)
        self.write(response.text)

    def post(self):
        notification_data = json.loads(self.request.body)
        response = requests.post(self.API_URL, json=notification_data)
        self.write(response.text)

    def put(self, notification_id):
        # Aquí, asumimos que el cuerpo de la solicitud no es necesario 
        # para marcar la notificación como leída.
        response = requests.put(f"{self.API_URL}/{notification_id}")
        self.write(response.text)

    def delete(self, notification_id):
        response = requests.delete(f"{self.API_URL}/{notification_id}")
        self.write(response.text)

class FollowersHandler(tornado.web.RequestHandler):
    API_URL = "http://172.18.0.3:3000/followers"

    def get(self):
        response = requests.get(self.API_URL)
        self.write(response.text)

    def post(self):
        follower_data = json.loads(self.request.body)
        response = requests.post(self.API_URL, json=follower_data)
        self.write(response.text)

    def delete(self, follower_id, followed_id):
        url = f"{self.API_URL}/{follower_id}/{followed_id}"
        response = requests.delete(url)
        self.write(response.text)

class CommentsHandler(tornado.web.RequestHandler):
    API_URL = "http://172.18.0.3:3000/comments"

    def get(self, comment_id=None):
        if comment_id:
            response = requests.get(f"{self.API_URL}/{comment_id}")
        else:
            response = requests.get(self.API_URL)
        self.write(response.text)

    def post(self):
        comment_data = json.loads(self.request.body)
        response = requests.post(self.API_URL, json=comment_data)
        self.write(response.text)

    def put(self, comment_id):
        comment_data = json.loads(self.request.body)
        response = requests.put(f"{self.API_URL}/{comment_id}", json=comment_data)
        self.write(response.text)

    def delete(self, comment_id):
        response = requests.delete(f"{self.API_URL}/{comment_id}")
        self.write(response.text)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("HTML/index.html")

def make_app():
    return tornado.web.Application([
        (r"/", IndexHandler), 
        (r"/user/?", UserHandler),
        (r"/user/([0-9]+)/?", UserHandler),
        (r"/stories/?", StoriesHandler),
        (r"/stories/([0-9]+)/?", StoriesHandler),
        (r"/posts/?", PostsHandler),
        (r"/posts/([0-9]+)/?", PostsHandler),
        (r"/notifications/?", NotificationsHandler),
        (r"/notifications/([0-9]+)/?", NotificationsHandler),
        (r"/followers/?", FollowersHandler),
        (r"/followers/([0-9]+)/([0-9]+)/?", FollowersHandler),
        (r"/comments/?", CommentsHandler),
        (r"/comments/([0-9]+)/?", CommentsHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
