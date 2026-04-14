# run.py
import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))   # Render often uses 10000 internally
    app.run(host="0.0.0.0", port=port, debug=False)