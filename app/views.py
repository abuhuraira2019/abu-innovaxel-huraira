from flask import Blueprint, request, jsonify
import random
import string
from app.models import get_db_connection

shorten_url = Blueprint('shorten_url', __name__)

#1 POST /shorten - Create a short URL and save it in the database
@shorten_url.route('/shorten', methods=['POST'])
def create_short_url():
    url = request.json.get('url')

    # Generate a random short code (6 characters)
    short_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

    # Save to database
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO urls (original_url, short_code, access_count) VALUES (%s, %s, 0)', (url, short_code))
    connection.commit()

    return jsonify({
        'id': cursor.lastrowid,  # Last inserted row ID (from auto_increment)
        'url': url,
        'shortCode': short_code,
        'createdAt': '2021-09-01T12:00:00Z',  # Replace with dynamic date if needed
        'updatedAt': '2021-09-01T12:00:00Z',  # Replace with dynamic date if needed
    }), 201


#2 GET /shorten/<short_code> - Retrieve the original URL from the database
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
            'id': 1,  # Replace with dynamic ID if needed
            'url': original_url,
            'shortCode': short_code,
            'createdAt': '2021-09-01T12:00:00Z',  # Replace with dynamic date if needed
            'updatedAt': '2021-09-01T12:00:00Z',  # Replace with dynamic date if needed
        })
    else:
        return jsonify({"error": "Short URL not found"}), 404
#3 PUT /shorten/<short_code> - Update an existing short URL
@shorten_url.route('/shorten/<short_code>', methods=['PUT'])
def update_short_url(short_code):
    # Get the new URL from the request body
    new_url = request.json.get('url')

    # Validate the request body
    if not new_url:
        return jsonify({"error": "URL is required"}), 400

    # Check if the short code exists
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM urls WHERE short_code = %s', (short_code,))
    result = cursor.fetchone()

    if result:
        # Update the URL
        cursor.execute('UPDATE urls SET original_url = %s, updated_at = NOW() WHERE short_code = %s', (new_url, short_code))
        connection.commit()

        return jsonify({
            'id': result[0],
            'url': new_url,
            'shortCode': short_code,
            'createdAt': result[3],  # Get dynamic createdAt
            'updatedAt': '2021-09-01T12:30:00Z',  # Replace with dynamic time
        })
    else:
        return jsonify({"error": "Short URL not found"}), 404


#5 GET /shorten/<short_code>/stats - Get access count and increment it
@shorten_url.route('/shorten/<short_code>/stats', methods=['GET'])
def get_url_statistics(short_code):
    # Query the database for the short code
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT access_count FROM urls WHERE short_code = %s', (short_code,))
    result = cursor.fetchone()

    if result:
        access_count = result[0]
        # Increment access count
        cursor.execute('UPDATE urls SET access_count = %s WHERE short_code = %s', (access_count + 1, short_code))
        connection.commit()

        return jsonify({
            'id': 1,  # Replace with dynamic ID if needed
            'url': 'https://www.example.com/some/long/url',  # You might want to replace this with actual URL
            'shortCode': short_code,
            'createdAt': '2021-09-01T12:00:00Z',
            'updatedAt': '2021-09-01T12:00:00Z',
            'accessCount': access_count + 1  # Return the incremented access count
        })
    else:
        return jsonify({"error": "Short URL not found"}), 404

