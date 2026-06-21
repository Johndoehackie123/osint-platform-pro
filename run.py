from app.main import app

if __name__ == "__main__":
    # For local development, we run with debug=True
    # In production, Gunicorn handles the execution
    app.run(host='0.0.0.0', port=5000, debug=True)
