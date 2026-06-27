#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONEYBALL FM26 - HERMES SYSTEM
Dashboard 100% INLINE - SEM ficheiros externos!
"""

import os
import csv
import tempfile
from flask import Flask, render_template_string, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'csv', 'png', 'jpg', 'jpeg', 'html'}

BENCHMARKS = {
    'GK': {'goals_90': 0.00, 'pass_pct': 75},
    'CB': {'goals_90': 0.05, 'pass_pct': 82},
    'FB': {'goals_90': 0.10, 'pass_pct': 78},
    'DM': {'goals_90': 0.08, 'pass_pct': 85},
    'CM': {'goals_90': 0.15, 'pass_pct': 83},
    'AM': {'goals_90': 0.25, 'pass_pct': 80},
    'W': {'goals_90': 0.35, 'pass_pct': 75},
    'ST': {'goals_90': 0.45, 'pass_pct': 70},
}

def calculate_score(player_data, position):
    if position not in BENCHMARKS:
        position = 'CM'
    benchmarks = BENCHMARKS[position]
    goals_90 = float(player_data.get('goals_90', 0))
    pass_pct = float(player_data.get('pass_pct', 0))
    score = 0
    score += (goals_90 / benchmarks['goals_90']) * 3 if benchmarks['goals_90'] > 0 else 0
    score += (pass_pct / benchmarks['pass_pct']) * 4
    return min(score, 10)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏆 Moneyball FM26</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0a0e27; color: #e0e0e0; min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: #1a1f3a; border-radius: 12px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5); overflow: hidden; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; color: white; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 0.95em; opacity: 0.9; }
        .tabs { display: flex; border-bottom: 2px solid #2a2f4a; background: #151b2f; }
        .tab-btn { flex: 1; padding: 15px 20px; background: none; border: none; color: #b0b0b0; cursor: pointer; font-size: 0.95em; font-weight: 500; transition: all 0.3s; border-bottom: 3px solid transparent; }
        .tab-btn:hover { color: #fff; background: rgba(102, 126, 234, 0.1); }
        .tab-btn.active { color: #667eea; border-bottom-color: #667eea; }
        .tab-content { display: none; padding: 30px; animation: fadeIn 0.3s ease-in; }
        .tab-content.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .upload-area { border: 2px dashed #667eea; border-radius: 8px; padding: 40px; text-align: center; cursor: pointer; transition: all 0.3s; background: rgba(102, 126, 234, 0.05); }
        .upload-area:hover { border-color: #764ba2; background: rgba(102, 126, 234, 0.1); }
        .upload-area p { font-size: 1.1em; margin-bottom: 10px; }
        .upload-area small { color: #b0b0b0; }
        #fileInput { display: none; }
        .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 12px 30px; border-radius: 6px; cursor: pointer; font-size: 0.95em; font-weight: 600; transition: transform 0.2s; margin-top: 20px; }
        .btn:hover { transform: translateY(-2px); }
        .results { margin-top: 20px; }
        .player-card { background: #252d45; border-left: 4px solid #667eea; padding: 15px; margin: 10px 0; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; }
        .player-card.elite { border-left-color: #4ade80; }
        .player-card.good { border-left-color: #60a5fa; }
        .player-card.fair { border-left-color: #fbbf24; }
        .scout-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-top: 20px; }
        .scout-card { background: #252d45; padding: 15px; border-radius: 6px; border-top: 3px solid #667eea; }
        .scout-card h3 { margin-bottom: 8px; color: #667eea; }
        .scout-card p { font-size: 0.9em; margin: 5px 0; color: #b0b0b0; }
        .badge { display: inline-block; background: #667eea; color: white; padding: 4px 10px; border-radius: 4px; font-size: 0.8em; margin-right: 5px; }
        .insight { background: rgba(102, 126, 234, 0.1); border-left: 4px solid #667eea; padding: 15px; margin: 10px 0; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 MONEYBALL FM26</h1>
            <p>Sistema de Análise Inteligente para Football Manager</p>
        </div>
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('upload')">📁 UPLOAD</button>
            <button class="tab-btn" onclick="switchTab('analyse')">📊 ANÁLISE</button>
            <button class="tab-btn" onclick="switchTab('scout')">🏆 SCOUT</button>
        </div>
        <div id="upload" class="tab-content active">
            <h2>Upload de Dados</h2>
            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                <p>📁 Arraste ficheiros aqui ou clique</p>
                <small>CSV, PNG, JPG ou HTML</small>
            </div>
            <input type="file" id="fileInput" onchange="handleFileUpload(event)">
            <button class="btn" onclick="processUpload()">PROCESSAR UPLOAD</button>
            <div id="uploadResult"></div>
        </div>
        <div id="analyse" class="tab-content">
            <h2>Análise Moneyball</h2>
            <div id="analyseResult">Carregue um ficheiro para começar...</div>
        </div>
        <div id="scout" class="tab-content">
            <h2>Scout Search</h2>
            <div id="scoutResult" class="scout-grid"></div>
            <button class="btn" onclick="loadScouts()">PESQUISAR SCOUTS</button>
        </div>
    </div>
    <script>
        let uploadedData = null;
        function switchTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        function handleFileUpload(event) {
            const file = event.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (e) => {
                const text = e.target.result;
                const lines = text.split('\\n');
                const headers = lines[0].split(',').map(h => h.trim());
                uploadedData = [];
                for (let i = 1; i < lines.length; i++) {
                    if (lines[i].trim()) {
                        const values = lines[i].split(',').map(v => v.trim());
                        const obj = {};
                        headers.forEach((header, index) => { obj[header] = values[index]; });
                        uploadedData.push(obj);
                    }
                }
                document.getElementById('uploadResult').innerHTML = `<div class="insight">✅ Ficheiro carregado! ${uploadedData.length} jogadores encontrados.</div>`;
            };
            reader.readAsText(file);
        }
        function processUpload() {
            if (!uploadedData) { alert('Carregue um ficheiro primeiro!'); return; }
            const analyseResult = document.getElementById('analyseResult');
            analyseResult.innerHTML = '<div style="text-align:center;color:#667eea;">⏳ A processar...</div>';
            setTimeout(() => {
                let html = '<h3>📊 Resultados:</h3><div class="results">';
                uploadedData.forEach((player, i) => {
                    const position = player.Position || 'CM';
                    const goals90 = parseFloat(player.Goals90) || 0;
                    const passPct = parseFloat(player.PassPct) || 0;
                    const score = goals90 * 3 + (passPct / 75) * 4;
                    const rating = score > 7 ? 'elite' : score > 5 ? 'good' : 'fair';
                    html += `<div class="player-card ${rating}"><div><strong>${player['Player Name'] || 'N/A'}</strong><p>${position} | ${player.Age || 'N/A'} anos</p></div><div><span class="badge">${score.toFixed(1)}/10</span></div></div>`;
                });
                html += '</div>';
                analyseResult.innerHTML = html;
            }, 500);
        }
        function loadScouts() {
            const scoutResult = document.getElementById('scoutResult');
            scoutResult.innerHTML = '';
            const scouts = [
                { name: 'Nelson Bazetch', pos: 'ST', goals: '0.90', value: '€24M' },
                { name: 'Tora Leah', pos: 'ST', goals: '0.76', value: '€8M' },
                { name: 'Mohamed Sylla', pos: 'CB', goals: '0.00', value: '€5M' },
                { name: 'Habibu Aliyu', pos: 'ST', goals: '0.69', value: '€4.5M' },
                { name: 'Mohammed Douff', pos: 'W', goals: '0.81', value: '€28M' },
            ];
            scouts.forEach(scout => {
                const card = document.createElement('div');
                card.className = 'scout-card';
                card.innerHTML = `<h3>${scout.name}</h3><p><span class="badge">${scout.pos}</span></p><p>Goals/90: ${scout.goals}</p><p>Valor: ${scout.value}</p>`;
                scoutResult.appendChild(card);
            });
        }
    </script>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Sem ficheiro'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Ficheiro vazio'}), 400
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
        return jsonify({'status': 'success', 'filename': filename, 'players': players}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
