from flask import Flask
from routes import register_routes
from database import init_db



app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)
init_db()

register_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)