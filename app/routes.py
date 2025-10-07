from flask import Blueprint, request, jsonify
from app.models import db, Feedback
from datetime import datetime
from sqlalchemy import func

bp = Blueprint('routes', __name__)
# Simule une prédiction (à remplacer par appel à ton modèle)
def predict_sentiment(text, aspect):
    # Ici on appellera ton modèle BERT fine-tuné
    return "neutral"  # exemple

# Route : prédiction
@bp.route('/', methods = ['GET'])
def hello():
    return jsonify({'message': "hello world"}), 201

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
# @bp.route('/api/feedbacks', methods=['POST'])
# def save_feedback():
#     data = request.get_json()
#     text = data.get("text")
#     aspect = data.get("aspect")
#     sentiment = data.get("sentiment")

#     feedback = Feedback(text=text, aspect=aspect, sentiment=sentiment)
#     db.session.add(feedback)
#     db.session.commit()

#     return jsonify({"message": "Feedback saved"}), 201

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


@bp.route('/api/stats/summary', methods=['GET'])
def stats_summary():
    total = db.session.query(func.count(Feedback.id)).scalar()
    sentiments = db.session.query(
        Feedback.sentiment, func.count(Feedback.id)
    ).group_by(Feedback.sentiment).all()

    sentiment_counts = {s: c for s, c in sentiments}
    positive = sentiment_counts.get("positive", 0)
    negative = sentiment_counts.get("negative", 0)
    neutral = sentiment_counts.get("neutral", 0)

    return jsonify({
        "total_feedbacks": total,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "positive_pct": round(positive / total * 100, 2) if total else 0,
        "negative_pct": round(negative / total * 100, 2) if total else 0,
        "neutral_pct": round(neutral / total * 100, 2) if total else 0,
    })

@bp.route('/api/stats/aspects', methods=['GET'])
def aspect_stats():
    data = db.session.query(
        Feedback.aspect,
        Feedback.sentiment,
        func.count(Feedback.id)
    ).group_by(Feedback.aspect, Feedback.sentiment).all()

    aspect_data = {}
    for aspect, sentiment, count in data:
        aspect_data.setdefault(aspect, {"positive": 0, "negative": 0, "neutral": 0})
        aspect_data[aspect][sentiment] = count

    return jsonify(aspect_data)

@bp.route("/api/stats/timeline", methods=["GET"])
def timeline_stats():
    from datetime import datetime

    rows = db.session.query(Feedback.created_at, Feedback.sentiment).all()
    stats = {}

    for created_at, sentiment in rows:
        # Ensure we always have a datetime object
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at)
            except ValueError:
                continue  # skip invalid date strings

        key = created_at.strftime("%Y-%m-%d")
        stats.setdefault(key, {"positive": 0, "negative": 0, "neutral": 0})
        if sentiment in stats[key]:
            stats[key][sentiment] += 1

    return jsonify(stats)
