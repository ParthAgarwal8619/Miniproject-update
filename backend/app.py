from flask import Flask
from routes import register_routes
from database import init_db
import os

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

# 🔐 SECRET KEY (required for login/session)
app.secret_key = "super_secret_key_123"

# 🔹 DATABASE INIT (users + existing tables)
init_db()

# 🔹 REGISTER ALL ROUTES (including login/signup/profile/admin)
register_routes(app)


# 🔹 RUN SERVER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
