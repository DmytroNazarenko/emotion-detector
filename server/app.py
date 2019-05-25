import time
import os
from flask import Flask, request, Response

app = Flask(__name__)


@app.route('/my', methods=['GET'])
def execute_script():
    start_time = time.time()
    print('aaaaa')
    response = Response(
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(debug=True, port='5000', host='0.0.0.0', use_reloader=False)