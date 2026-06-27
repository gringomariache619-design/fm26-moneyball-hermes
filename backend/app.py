#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import csv
import tempfile
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

BASE_DIR = Path(__file__).parent.parent
BACKEND_DIR = Path(__file__).parent
TEMPLATE_DIR = BACKEND_DIR / 'frontend' / 'templates'
STATIC_DIR = BACKEND_DIR / 'frontend' / 'static'

print(f"[INFO] TEMPLATE_DIR: {TEMPLATE_DIR}")
print(f"[INFO] STATIC_DIR: {STATIC_DIR}")

app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR),
    static_url_path='/static'
)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'csv', 'png', 'jpg', 'jpeg', 'html'}

MUSTERMANN_BENCHMARKS = {
    'GK': {'goals_90': 0.00, 'pass_pct': 75, 'xg_90': 0.00},
    'CB': {'goals_90': 0.05, 'pass_pct': 82, 'xg_90': 0.02},
    'FB': {'goals_90': 0.10, 'pass_pct': 78, 'xg_90': 0.05},
    'DM': {'goals_90': 0.08, 'pass_pct': 85, 'xg_90': 0.04},
    'CM': {'goals_90': 0.15, 'pass_pct': 83, 'xg_90': 0.08},
    'AM': {'goals_90': 0.25, 'pass_pct': 80, 'xg_90': 0.15},
    'W': {'goals_90': 0.35, 'pass_pct': 75, 'xg_90': 0.20},
    'ST': {'goals_90': 0.45, 'pass_pct': 70, 'xg_90': 0.35},
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_mustermann_score(player_data, position):
    if position not in MUSTERMANN_BENCHMARKS:
        position = 'CM'
    benchmarks = MUSTERMANN_BENCHMARKS[position]
    goals_90 = float(player_data.get('goals_90', 0))
    pass_pct = float(player_data.get('pass_pct', 0))
    xg_90 = float(player_data.get('xg_90', 0))
    score = 0
    score += (goals_90 / benchmarks['goals_90']) * 3 if benchmarks['goals_90'] > 0 else 0
    score += (pass_pct / benchmarks['pass_pct']) * 4
    score += (xg_90 / benchmarks['xg_90']) * 3 if benchmarks['xg_90'] > 0 else 0
    return min(score, 10)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Sem ficheiro'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Ficheiro vazio'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Ficheiro não permitido'}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    try:
        players = []
        if filename.endswith('.csv'):
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    players.append(row)
        return jsonify({'status': 'success', 'filename': filename, 'players': players[:10]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyse', methods=['POST'])
def analyse():
    data = request.json
    players = data.get('players', [])
    team_type = data.get('team_type', 'principal')
    results = {'team_type': team_type, 'total_players': len(players), 'top_performers': [], 'by_position': {}, 'insights': []}
    for player in players:
        position = player.get('Position', 'CM').upper()
        score = calculate_mustermann_score(player, position)
        player['score'] = score
        player['rating'] = 'Elite' if score >= 7 else 'Good' if score >= 5 else 'Fair'
        if position not in results['by_position']:
            results['by_position'][position] = []
        results['by_position'][position].append(player)
    sorted_players = sorted(players, key=lambda x: x['score'], reverse=True)
    results['top_performers'] = sorted_players[:5]
    if sorted_players:
        results['insights'].append(f"Top: {sorted_players[0].get('Player Name', 'N/A')} ({sorted_players[0]['score']:.1f})")
    return jsonify(results), 200

@app.route('/api/scout-search', methods=['POST'])
def scout_search():
    scouts = [
        {'name': 'Nelson Bazetch', 'position': 'ST', 'goals_90': 0.90, 'value': 24000000},
        {'name': 'Tora Leah', 'position': 'ST', 'goals_90': 0.76, 'value': 8000000},
        {'name': 'Mohamed Sylla', 'position': 'CB', 'goals_90': 0.00, 'value': 5000000},
    ]
    results = scouts
    if request.json.get('position'):
        results = [s for s in results if s['position'] == request.json['position'].upper()]
    return jsonify(results), 200

@app.route('/api/export', methods=['POST'])
def export_data():
    data = request.json
    return jsonify({'status': 'success', 'format': data.get('format', 'csv'), 'data': data.get('data', [])}), 200

@app.route('/static/<path:path>')
def send_static(path):
    try:
        return send_from_directory(app.static_folder, path)
    except:
        return "File not found", 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Página não encontrada'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Erro no servidor'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
