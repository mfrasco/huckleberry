"""Entry point for the application."""
import os
from dotenv import load_dotenv
from huckleberry import create_app

# Load environment variables from .env file if it exists
load_dotenv()

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)