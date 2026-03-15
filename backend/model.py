import os
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "..", "models", "email_classifier.pkl")

model, vectorizer = joblib.load(model_path)


def classify_email(text):

    text_lower = text.lower()

    # manual rule for query
    if "where" in text_lower or "when" in text_lower or "status" in text_lower:
        return "Query", 90

    if "delay" in text_lower or "late" in text_lower or "not received" in text_lower:
        return "Complaint", 88

    if "thank" in text_lower or "great service" in text_lower:
        return "Feedback", 92

    X = vectorizer.transform([text])

    prediction = model.predict(X)[0]

    confidence = max(model.predict_proba(X)[0]) * 100

    return prediction, round(confidence,2)