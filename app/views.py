from flask import Blueprint, request, jsonify
import random
import string

shorten_url = Blueprint('shorten_url', __name__)

@shorten_url.route('/shorten', methods=['POST'])
def create_short_url():
    url = request.json.get('url')

    # Generate a random short code (6 characters)
    short_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

    # Normally, you would save the mapping to a database here

    return jsonify({
        'id': 1,  # Replace with dynamic ID
        'url': url,
        'shortCode': short_code,
        'createdAt': '2021-09-01T12:00:00Z',  # Static example time
        'updatedAt': '2021-09-01T12:00:00Z',  # Static example time
    }), 201

