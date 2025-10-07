import json
from app import create_app, db
from app.models import Feedback

def load_fixture():
    app = create_app()
    with app.app_context():
        with open("app/fixtures/aspect-dataset.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        records = []
        for item in data:
            feedback = Feedback(
                text=item["text"],
                aspect=item["aspect"],
                sentiment=item["sentiment"]
            )
            records.append(feedback)

        db.session.bulk_save_objects(records)
        db.session.commit()
        print(f"✅ Loaded {len(records)} feedback records into the database.")

if __name__ == "__main__":
    load_fixture()
