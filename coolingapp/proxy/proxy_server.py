from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/proxy', methods=['GET'])
def proxy():
    # Get the URL to proxy from the query parameters
    url = request.args.get('url')

    if url:
        try:
            # Send a request to the specified URL
            response = requests.get(url)

            # Return the response content with the appropriate headers
            return response.content, response.status_code, {'Content-Type': response.headers['Content-Type']}
        except Exception as e:
            return str(e), 500
    else:
        return 'URL parameter is missing', 400

if __name__ == '__main__':
    app.run()
