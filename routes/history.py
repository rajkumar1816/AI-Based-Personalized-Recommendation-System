"""History routes for viewing and managing search history."""
import os
from flask import Blueprint, request, jsonify, render_template, send_file
from models.history_manager import HistoryManager
from utils.helper import export_history_to_csv, build_error_message
from config import BASE_DIR

history_bp = Blueprint('history', __name__)


@history_bp.route('/history', methods=['GET'])
def view_history():
    rows = HistoryManager.list_all()
    return render_template('history.html', history=rows)


@history_bp.route('/history', methods=['POST'])
def add_history():
    data = request.json or request.form
    query = data.get('query', '').strip()
    category = data.get('category', 'All').strip()
    if not query:
        return jsonify(build_error_message('Search query cannot be empty.')), 400
    HistoryManager.add(query, category)
    return jsonify({'status': 'ok'})


@history_bp.route('/history', methods=['DELETE'])
def delete_history():
    data = request.json or request.form
    record_id = data.get('id')
    if record_id:
        try:
            HistoryManager.delete(int(record_id))
            return jsonify({'status': 'deleted'})
        except ValueError:
            return jsonify(build_error_message('Invalid history record identifier.')), 400
    HistoryManager.clear()
    return jsonify({'status': 'cleared'})


@history_bp.route('/history/export', methods=['GET'])
def export_history():
    rows = HistoryManager.list_all()
    out_path = os.path.join(BASE_DIR, 'database', 'history_export.csv')
    export_history_to_csv(rows, out_path)
    return send_file(out_path, as_attachment=True)
