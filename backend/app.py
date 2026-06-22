"""
🎯 MONEYBALL FM26 - Backend API
Modern Performance Analysis System for FM26
Compatible: Mac / PC | Input: Screenshots / CSV / HTML
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
import json
import os
import sys
import pandas as pd
from pathlib import Path
import io

# Import processing scripts
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../scripts'))
from moneyball_processor import MoneyballProcessor
from mustermann_calculator import MustermannCalculator

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')
CORS(app)

# Initialize processors
processor = MoneyballProcessor()
calculator = MustermannCalculator()

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../data/uploads')
ALLOWED_EXTENSIONS = {'csv', 'png', 'jpg', 'jpeg', 'html'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============ ROUTES ============

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'online',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'system': 'Moneyball FM26 Backend'
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file uploads (CSV, screenshots, HTML)"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        squad_type = request.form.get('squad_type', 'principal')
        
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Save file
        filename = f"{datetime.now().timestamp()}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process file
        result = processor.process_file(filepath, squad_type)
        
        return jsonify({
            'success': True,
            'file': filename,
            'data': result,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_squad():
    """Analyze squad performance with Mustermann methodology"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'squad' not in data:
            return jsonify({'error': 'Squad data required'}), 400
        
        squad_data = data['squad']
        team_level = data.get('team_level', 'mid_table')  # title_contender, mid_table, relegation
        
        # Calculate Mustermann scores
        scores = calculator.calculate_squad_scores(squad_data)
        
        # Analyze performance
        analysis = {
            'squad_size': len(squad_data),
            'analysis_date': datetime.now().isoformat(),
            'team_level': team_level,
            'players': scores['players'],
            'summary': scores['summary'],
            'insights': processor.generate_insights(scores, team_level),
            'recommendations': processor.generate_recommendations(scores, team_level)
        }
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scout-search', methods=['POST'])
def scout_search():
    """Search for undervalued players based on criteria"""
    try:
        data = request.get_json()
        
        criteria = {
            'position': data.get('position'),
            'min_goals_per_90': float(data.get('min_goals_per_90', 0.3)),
            'max_price': float(data.get('max_price', 10)),
            'league': data.get('league'),
            'age_min': int(data.get('age_min', 18)),
            'age_max': int(data.get('age_max', 32)),
            'team_level': data.get('team_level', 'all')
        }
        
        results = processor.scout_search(criteria)
        
        return jsonify({
            'success': True,
            'criteria': criteria,
            'results': results,
            'count': len(results),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/<format>', methods=['POST'])
def export_analysis(format):
    """Export analysis to CSV, Excel or PDF"""
    try:
        data = request.get_json()
        
        if format == 'csv':
            df = pd.DataFrame(data['data'])
            output = io.StringIO()
            df.to_csv(output, index=False)
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode()),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f"moneyball_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
        
        elif format == 'json':
            return jsonify(data)
        
        else:
            return jsonify({'error': 'Unsupported format'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare-squads', methods=['POST'])
def compare_squads():
    """Compare multiple squads side by side"""
    try:
        data = request.get_json()
        squads = data.get('squads', [])
        
        comparison = processor.compare_squads(squads)
        
        return jsonify({
            'success': True,
            'comparison': comparison,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mustermann-benchmarks', methods=['GET'])
def get_benchmarks():
    """Get Mustermann FM benchmarks for all positions"""
    try:
        benchmarks = calculator.get_benchmarks()
        return jsonify({
            'success': True,
            'benchmarks': benchmarks
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============ MAIN ============

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
