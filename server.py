import os
from flask import Flask, request
app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def hello_world():
    """."""
    json_body = request.get_json()
    headers = request.headers
    app.logger.debug({"body": json_body, "headers": headers})
    return 'Hello, World!'


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True, )
