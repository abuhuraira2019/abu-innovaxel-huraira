from flask import Blueprint, request, jsonify
import random
import string

shorten_url = Blueprint('shorten_url', __name__)

@shorten_url.route('/shorten', methods=['POST'])
def create_short_url():
    url = request.json.get('url')

    # Generate a random short code (6 characters)
    short_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        # Save to database
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO urls (original_url, short_code) VALUES (%s, %s)', (url, short_code))
    connection.commit()

    return jsonify({
        'id': cursor.lastrowid,
        'url': url,
        'shortCode': short_code,
        'createdAt': '2021-09-01T12:00:00Z',
        'updatedAt': '2021-09-01T12:00:00Z',
    }), 201

    # Normally, you would save the mapping to a database here

    return jsonify({
        'id': 1,  # Replace with dynamic ID
        'url': url,
        'shortCode': short_code,
        'createdAt': '2021-09-01T12:00:00Z',  # Static example time
        'updatedAt': '2021-09-01T12:00:00Z',  # Static example time
    }), 201
@shorten_url.route('/shorten/<short_code>', methods=['GET'])
def get_original_url(short_code):
    # Query the database for the short code
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT original_url FROM urls WHERE short_code = %s', (short_code,))
    result = cursor.fetchone()

    if result:
        original_url = result[0]
        return jsonify({
            'id': 1,  # Replace with dynamic ID
            'url': original_url,
            'shortCode': short_code,
            'createdAt': '2021-09-01T12:00:00Z',
            'updatedAt': '2021-09-01T12:00:00Z',
        })
    else:
        return jsonify({"error": "Short URL not found"}), 404


