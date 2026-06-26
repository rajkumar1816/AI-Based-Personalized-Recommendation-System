"""Favorites routes for CRUD operations."""
from flask import Blueprint, request, jsonify, render_template
from models.favorites_manager import FavoritesManager
from utils.helper import build_error_message

fav_bp = Blueprint('favorites', __name__)


@fav_bp.route('/favorites', methods=['GET'])
def view_favorites():
    rows = FavoritesManager.list_all()
    return render_template('favorites.html', favorites=rows)


@fav_bp.route('/favorites', methods=['POST'])
def add_favorite():
    data = request.json or request.form
    title = (data.get('title') or '').strip()
    genre = (data.get('genre') or '').strip()
    if not title:
        return jsonify(build_error_message('Favorite title is required.')), 400
    FavoritesManager.add(title, genre)
    return jsonify({'status': 'ok'})


@fav_bp.route('/favorites', methods=['DELETE'])
def delete_favorite():
    data = request.json or request.form
    record_id = data.get('id')
    if not record_id:
        return jsonify(build_error_message('Favorite identifier is required.')), 400
    FavoritesManager.delete(int(record_id))
    return jsonify({'status': 'deleted'})
