from flask import Blueprint, request, jsonify
from app.models import db, Feedback
from datetime import datetime

bp = Blueprint('routes', __name__)

# Simule une prédiction (à remplacer par appel à ton modèle)
def predict_sentiment(text, aspect):
    # Ici on appellera ton modèle BERT fine-tuné
    return "neutral"  # exemple

# Route : prédiction
@bp.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get("text")
    aspect = data.get("aspect")

    if not text or not aspect:
        return jsonify({"error": "Missing text or aspect"}), 400

    sentiment = predict_sentiment(text, aspect)
    return jsonify({
        "text": text,
        "aspect": aspect,
        "sentiment": sentiment
    })

# Route : sauvegarde dans la base
@bp.route('/api/feedbacks', methods=['POST'])
def save_feedback():
    data = request.get_json()
    text = data.get("text")
    aspect = data.get("aspect")
    sentiment = data.get("sentiment")

    feedback = Feedback(text=text, aspect=aspect, sentiment=sentiment)
    db.session.add(feedback)
    db.session.commit()

    return jsonify({"message": "Feedback saved"}), 201

# Route : récupérer tous les feedbacks
@bp.route('/api/feedbacks', methods=['GET'])
def get_feedbacks():
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    result = [{
        "id": f.id,
        "text": f.text,
        "aspect": f.aspect,
        "sentiment": f.sentiment,
        "created_at": f.created_at.isoformat()
    } for f in feedbacks]
    return jsonify(result)

# Route : résumé simple
@bp.route('/api/summary', methods=['GET'])
def summary():
    from collections import Counter
    all_feedbacks = Feedback.query.all()
    sentiments = [f.sentiment for f in all_feedbacks]
    summary = Counter(sentiments)
    return jsonify(summary)
