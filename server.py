import os
from flask import Flask, request
from hmac import HMAC, compare_digest
from hashlib import sha1

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def webhook():
    """."""
    app.logger.debug(os.environ)
    # if request.method == 'POST':
    #     if verify_signature(request):
    #         # make something
    #         return 'Successfully', 200
    #     return 'Forbidden', 403
    # return 'Not allowed', 405


def verify_signature(req):
    received_sign = req.headers.get(
        'X-Hub-Signature-256').split('sha256=')[-1].strip()
    secret = 'my_secret_string'.encode()
    expected_sign = HMAC(key=secret, msg=req.data, digestmod=sha1).hexdigest()
    return compare_digest(received_sign, expected_sign)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True, )
