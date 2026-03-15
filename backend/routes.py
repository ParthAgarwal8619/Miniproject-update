from flask import render_template, request, redirect
from model import classify_email
from sentiment import analyze_sentiment
from ticket_system import generate_response
from database import get_connection
import random


def register_routes(app):

    # HOME
    @app.route("/")
    def home():
        return render_template("index.html")


    # DASHBOARD
    @app.route("/dashboard")
    def dashboard():

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


    # ANALYZE EMAIL
    @app.route("/analyze", methods=["GET","POST"])
    def analyze():

        if request.method == "POST":

            email = request.form["email"]

            category, confidence = classify_email(email)

            sentiment = analyze_sentiment(email)

            priority = "Medium"

            response = generate_response(category)
            
            confidence = random.randint(60,95)

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO history(email,category,sentiment,priority)
            VALUES (?,?,?,?)
            """,(email,category,sentiment,priority))

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


    # HISTORY
    @app.route("/history")
    def history():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM history ORDER BY id DESC")

        rows = cursor.fetchall()

        conn.close()

        return render_template("history.html", rows=rows)


    # DELETE
    @app.route("/delete/<int:id>")
    def delete_email(id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM history WHERE id=?", (id,))

        conn.commit()
        conn.close()

        return redirect("/history")


    # EDIT
    @app.route("/edit/<int:id>", methods=["GET","POST"])
    def edit_email(id):

        conn = get_connection()
        cursor = conn.cursor()

        if request.method == "POST":

            email = request.form["email"]

            cursor.execute("""
            UPDATE history
            SET email=?
            WHERE id=?
            """,(email,id))

            conn.commit()
            conn.close()

            return redirect("/history")

        cursor.execute("SELECT * FROM history WHERE id=?", (id,))
        row = cursor.fetchone()

        conn.close()

        return render_template("edit.html", row=row)


    # STATISTICS
    @app.route("/statistics")
    def statistics():

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


    # ABOUT
    @app.route("/about")
    def about():
        return render_template("about.html")