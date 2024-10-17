import logging
from flask import Flask, jsonify, request
from services.playlist_manager import PlaylistManager
from services.user_info_viewer import UserInfoViewer
from music_chart_scraper_config import MUSIC_CHART_SCRAPER_CONFIG

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
playlist_manager = PlaylistManager()
user_info_viewer = UserInfoViewer()

def create_playlist_handler(chart_type):
    try:
        logger.info(f"Attempting to create playlist for chart type: {chart_type}")
        playlist_manager.create_playlist(chart_type=chart_type)
        logger.info(f"Successfully created playlist for {chart_type}")
        return jsonify({"message": f"{chart_type.replace('_', ' ').title()} playlist created successfully"}), 201
    except Exception as e:
        logger.error(f"Error creating playlist for {chart_type}: {str(e)}")
        return jsonify({"error": f"Failed to create playlist for {chart_type}"}), 500

@app.route('/create/playlist/billboard_tiktok_top_50', methods=['POST'])
def create_billboard_tiktok_playlist():
    return create_playlist_handler("billboard_tiktok_top_50")

@app.route('/create/playlist/billboard_hot_100', methods=['POST'])
def create_billboard_hot_100_playlist():
    return create_playlist_handler("billboard_hot_100")

@app.route('/create/playlist/billboard_decade_end_hot_100', methods=['POST'])
def create_billboard_decade_end_hot_100_playlist():
    return create_playlist_handler("billboard_decade_end_hot_100")

@app.route('/user/info', methods=['GET'])
def get_user_info():
    try:
        logger.info("Attempting to fetch user information")
        user_info = user_info_viewer.get_user_info()
        if user_info:
            logger.info("Successfully fetched user information")
            return jsonify(user_info), 200
        else:
            logger.warning("No user information available")
            return jsonify({"error": "No user information available"}), 404
    except Exception as e:
        logger.error(f"Error fetching user information: {str(e)}")
        return jsonify({"error": "Failed to fetch user information"}), 500

@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error: {request.url}")
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    logger.info("Starting Flask application")
    app.run(debug=True)