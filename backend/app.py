from flask import Flask
from routes import register_routes
from database import init_db
import os



app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)
init_db()

register_routes(app)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
