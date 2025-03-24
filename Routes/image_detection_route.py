from flask import Blueprint
from Controllers.image_detection_controller import ImageDetection

image_bp = Blueprint('Image', __name__)

image_bp.add_url_rule('/postImage', view_func=ImageDetection.process_image, methods=['POST'])
