from flask import render_template, request, redirect, session
from model import classify_email
from sentiment import analyze_sentiment
from ticket_system import generate_response
from database import get_connection
import random
from werkzeug.security import generate_password_hash, check_password_hash


def register_routes(app):

    # 🔹 HOME
    @app.route("/")
    def home():
        return render_template("index.html")


    # 🔹 SIGNUP
    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            name = request.form["name"]
            email = request.form["email"]
            password = generate_password_hash(request.form["password"])

            conn = get_connection()
            c = conn.cursor()

            try:
                c.execute(
                    "INSERT INTO users (name,email,password) VALUES (?,?,?)",
                    (name, email, password)
                )
                conn.commit()
                conn.close()
                return redirect("/login")
            except:
                conn.close()
                return render_template("signup.html", error="User already exists")

        return render_template("signup.html")


    # 🔹 LOGIN
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            conn = get_connection()
            c = conn.cursor()

            c.execute("SELECT * FROM users WHERE email=?", (email,))
            user = c.fetchone()
            conn.close()

            if user and check_password_hash(user[3], password):
                session["user_id"] = user[0]
                session["role"] = user[4]

                if user[4] == "admin":
                    return redirect("/admin")
                return redirect("/dashboard")

            return render_template("login.html", error="Invalid Login")

        return render_template("login.html")


    # 🔹 LOGOUT
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/")


    # 🔹 DASHBOARD
    @app.route("/dashboard")
    def dashboard():

        if "user_id" not in session:
            return redirect("/login")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM history")
        total_emails = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM history WHERE category='Complaint'")
        complaints = cursor.fetchone()[0]

        cursor.execute("""
        SELECT COUNT(*) FROM history 
        WHERE category='Query' OR category='Order Status'
        """)
        queries = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM history WHERE category='Feedback'")
        feedbacks = cursor.fetchone()[0]

        conn.close()

        return render_template(
            "dashboard.html",
            total_emails=total_emails,
            complaints=complaints,
            queries=queries,
            feedbacks=feedbacks
        )


    # 🔹 ADMIN PANEL
    @app.route("/admin")
    def admin():

        if session.get("role") != "admin":
            return "Access Denied"

        conn = get_connection()
        c = conn.cursor()

        c.execute("SELECT id, name, email, role FROM users")
        users = c.fetchall()

        conn.close()

        return render_template("admin.html", users=users)


    # 🔹 MAKE ADMIN
    @app.route("/make-admin/<int:id>")
    def make_admin(id):

        if session.get("role") != "admin":
            return "Access Denied"

        conn = get_connection()
        c = conn.cursor()

        c.execute("UPDATE users SET role='admin' WHERE id=?", (id,))
        conn.commit()
        conn.close()

        return redirect("/admin")


    # 🔹 REMOVE ADMIN
    @app.route("/remove-admin/<int:id>")
    def remove_admin(id):

        if session.get("role") != "admin":
            return "Access Denied"

        conn = get_connection()
        c = conn.cursor()

        c.execute("UPDATE users SET role='user' WHERE id=?", (id,))
        conn.commit()
        conn.close()

        return redirect("/admin")


    # 🔹 ANALYZE EMAIL
    @app.route("/analyze", methods=["GET", "POST"])
    def analyze():

        if "user_id" not in session:
            return redirect("/login")

        if request.method == "POST":

            email = request.form["email"]

            category, confidence = classify_email(email)
            sentiment = analyze_sentiment(email)
            priority = "Medium"
            response = generate_response(category)

            confidence = random.randint(60, 95)

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO history(email,category,sentiment,priority)
            VALUES (?,?,?,?)
            """, (email, category, sentiment, priority))

            conn.commit()
            conn.close()

            return render_template(
                "result.html",
                email=email,
                category=category,
                sentiment=sentiment,
                priority=priority,
                response=response,
                confidence=confidence
            )

        return render_template("analyze.html")


    # 🔹 HISTORY
    @app.route("/history")
    def history():

        if "user_id" not in session:
            return redirect("/login")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM history ORDER BY id DESC")
        rows = cursor.fetchall()

        conn.close()

        return render_template("history.html", rows=rows)


    # 🔹 STATISTICS (FIXED 🔥)
    @app.route("/statistics")
    def statistics():
        
        if "user_id" not in session:
            return redirect("/login")

        conn = get_connection()
        cursor = conn.cursor()

    # Total emails
        cursor.execute("SELECT COUNT(*) FROM history")
        total = cursor.fetchone()[0]

    # Complaints
        cursor.execute("SELECT COUNT(*) FROM history WHERE category LIKE '%Complaint%'")
        complaints = cursor.fetchone()[0]

    # Queries
        cursor.execute("SELECT COUNT(*) FROM history WHERE category LIKE '%Query%' OR category LIKE '%Order%'")
        queries = cursor.fetchone()[0]

    # Feedback
        cursor.execute("SELECT COUNT(*) FROM history WHERE category LIKE '%Feedback%'")
        feedback = cursor.fetchone()[0]

    # Sentiment counts
        cursor.execute("SELECT COUNT(*) FROM history WHERE sentiment='Positive'")
        positive = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM history WHERE sentiment='Neutral'")
        neutral = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM history WHERE sentiment='Negative'")
        negative = cursor.fetchone()[0]

        conn.close()

        return render_template(
        "statistics.html",
        total=total,
        complaints=complaints,
        queries=queries,
        feedback=feedback,
        positive=positive,
        neutral=neutral,
        negative=negative
    )

    # 🔹 PROFILE
    @app.route("/profile")
    def profile():

        if "user_id" not in session:
            return redirect("/login")

        conn = get_connection()
        c = conn.cursor()

        c.execute("SELECT name, email, role FROM users WHERE id=?", (session["user_id"],))
        user = c.fetchone()

        conn.close()

        return render_template("profile.html", user=user)


    # 🔹 EDIT PROFILE
    @app.route("/edit-profile", methods=["GET", "POST"])
    def edit_profile():

        if "user_id" not in session:
            return redirect("/login")

        conn = get_connection()
        c = conn.cursor()

        if request.method == "POST":
            name = request.form["name"]

            c.execute("UPDATE users SET name=? WHERE id=?", (name, session["user_id"]))
            conn.commit()
            conn.close()

            return redirect("/profile")

        c.execute("SELECT name, email FROM users WHERE id=?", (session["user_id"],))
        user = c.fetchone()

        conn.close()

        return render_template("edit_profile.html", user=user)


    # 🔹 CHANGE PASSWORD (FIXED 🔥)
    @app.route('/change-password', methods=['POST'])
    def change_password():

        if "user_id" not in session:
            return redirect("/login")

        new_pass = generate_password_hash(request.form['password'])

        conn = get_connection()
        c = conn.cursor()

        c.execute(
            "UPDATE users SET password=? WHERE id=?",
            (new_pass, session["user_id"])
        )

        conn.commit()
        conn.close()

        return redirect('/profile')


    # 🔹 ABOUT
    @app.route("/about")
    def about():

        if "user_id" not in session:
            return redirect("/login")

        return render_template("about.html")
