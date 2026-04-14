# run.py
import os

from app import create_app   # assuming your package is named "app"

app = create_app()

if __name__ == "__main__":
    # For local testing only
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8090)), debug=False)