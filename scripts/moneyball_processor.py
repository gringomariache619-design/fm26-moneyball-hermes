"""
Moneyball Processor - Core analysis engine
Processes screenshots, CSV, and HTML data with Mustermann FM methodology
"""

import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import pytesseract
from PIL import Image
import re

class MoneyballProcessor:
    """Main processing engine for Moneyball analysis"""
    
    def __init__(self):
        self.benchmarks = self._load_benchmarks()
        self.cache = {}
    
    def _load_benchmarks(self):
        """Load Mustermann FM benchmarks"""
        return {
            'CB': {
                'excellent': {'tackle_win': 76.7, 'pass_pct': 69.88, 'interceptions_p90': 3.12, 'blocks_p90': 0.75},
                'good': {'tackle_win': 74.7, 'pass_pct': 62.33, 'interceptions_p90': 2.88, 'blocks_p90': 0.68},
                'fair': {'tackle_win': 72.4, 'pass_pct': 56.45, 'interceptions_p90': 2.65, 'blocks_p90': 0.62},
                'poor': {'tackle_win': 70.0, 'pass_pct': 50.96, 'interceptions_p90': 2.38, 'blocks_p90': 0.56}
            },
            'FB': {
                'excellent': {'tackle_win': 74.7, 'pass_pct': 69.88, 'interceptions_p90': 2.88, 'blocks_p90': 0.75},
                'good': {'tackle_win': 72.4, 'pass_pct': 62.33, 'interceptions_p90': 2.65, 'blocks_p90': 0.68},
                'fair': {'tackle_win': 70.1, 'pass_pct': 56.45, 'interceptions_p90': 2.52, 'blocks_p90': 0.62},
                'poor': {'tackle_win': 68.0, 'pass_pct': 50.96, 'interceptions_p90': 2.38, 'blocks_p90': 0.56}
            },
            'DM': {
                'excellent': {'tackle_win': 74.7, 'pass_pct': 68.83, 'interceptions_p90': 2.86, 'key_passes_p90': 2.08},
                'good': {'tackle_win': 72.4, 'pass_pct': 60.74, 'interceptions_p90': 2.52, 'key_passes_p90': 1.6},
                'fair': {'tackle_win': 69.8, 'pass_pct': 54.66, 'interceptions_p90': 2.32, 'key_passes_p90': 1.2},
                'poor': {'tackle_win': 67.3, 'pass_pct': 48.62, 'interceptions_p90': 1.96, 'key_passes_p90': 0.87}
            },
            'CM': {
                'excellent': {'tackle_win': 72.4, 'pass_pct': 68.83, 'key_passes_p90': 2.08, 'goals_p90': 0.20},
                'good': {'tackle_win': 70.0, 'pass_pct': 60.74, 'key_passes_p90': 1.6, 'goals_p90': 0.15},
                'fair': {'tackle_win': 68.0, 'pass_pct': 54.66, 'key_passes_p90': 1.2, 'goals_p90': 0.10},
                'poor': {'tackle_win': 65.0, 'pass_pct': 48.62, 'key_passes_p90': 0.87, 'goals_p90': 0.05}
            },
            'AM': {
                'excellent': {'pass_pct': 68.83, 'key_passes_p90': 2.08, 'goals_p90': 0.25, 'assists_p90': 0.20},
                'good': {'pass_pct': 60.74, 'key_passes_p90': 1.6, 'goals_p90': 0.18, 'assists_p90': 0.15},
                'fair': {'pass_pct': 54.66, 'key_passes_p90': 1.2, 'goals_p90': 0.12, 'assists_p90': 0.10},
                'poor': {'pass_pct': 48.62, 'key_passes_p90': 0.87, 'goals_p90': 0.07, 'assists_p90': 0.05}
            },
            'W': {
                'excellent': {'goals_p90': 0.47, 'xg_p90': 0.40, 'assists_p90': 0.27, 'dribbles_p90': 5.62},
                'good': {'goals_p90': 0.37, 'xg_p90': 0.32, 'assists_p90': 0.22, 'dribbles_p90': 3.43},
                'fair': {'goals_p90': 0.29, 'xg_p90': 0.26, 'assists_p90': 0.17, 'dribbles_p90': 1.63},
                'poor': {'goals_p90': 0.22, 'xg_p90': 0.21, 'assists_p90': 0.12, 'dribbles_p90': 0.84}
            },
            'ST': {
                'excellent': {'goals_p90': 0.47, 'xg_p90': 0.40, 'shots_p90': 2.81, 'assists_p90': 0.27},
                'good': {'goals_p90': 0.37, 'xg_p90': 0.32, 'shots_p90': 2.47, 'assists_p90': 0.22},
                'fair': {'goals_p90': 0.29, 'xg_p90': 0.26, 'shots_p90': 2.22, 'assists_p90': 0.17},
                'poor': {'goals_p90': 0.22, 'xg_p90': 0.21, 'shots_p90': 1.96, 'assists_p90': 0.12}
            },
            'GK': {
                'excellent': {'pass_pct': 26.06, 'progressive_passes_p90': 0.98, 'possession_lost_p90': 2.35},
                'good': {'pass_pct': 24.38, 'progressive_passes_p90': 0.74, 'possession_lost_p90': 3.67},
                'fair': {'pass_pct': 23.26, 'progressive_passes_p90': 0.58, 'possession_lost_p90': 6.04},
                'poor': {'pass_pct': 21.58, 'progressive_passes_p90': 0.37, 'possession_lost_p90': 8.21}
            }
        }
    
    def process_file(self, filepath, squad_type='principal'):
        """Process uploaded file (CSV, screenshot, HTML)"""
        filepath = Path(filepath)
        
        if filepath.suffix.lower() == '.csv':
            return self._process_csv(filepath)
        elif filepath.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            return self._process_screenshot(filepath)
        elif filepath.suffix.lower() == '.html':
            return self._process_html(filepath)
        else:
            raise ValueError(f"Unsupported file type: {filepath.suffix}")
    
    def _process_csv(self, filepath):
        """Process CSV file"""
        try:
            df = pd.read_csv(filepath)
            data = df.to_dict(orient='records')
            return {
                'type': 'csv',
                'records': data,
                'count': len(data)
            }
        except Exception as e:
            raise Exception(f"CSV processing error: {str(e)}")
    
    def _process_screenshot(self, filepath):
        """Process screenshot using OCR"""
        try:
            image = Image.open(filepath)
            text = pytesseract.image_to_string(image)
            
            # Parse player data from OCR text
            players = self._parse_player_data(text)
            
            return {
                'type': 'screenshot',
                'players': players,
                'count': len(players)
            }
        except Exception as e:
            raise Exception(f"Screenshot processing error: {str(e)}")
    
    def _process_html(self, filepath):
        """Process HTML export"""
        try:
            import re
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract table data
            tables = pd.read_html(filepath)
            if tables:
                df = tables[0]
                data = df.to_dict(orient='records')
                return {
                    'type': 'html',
                    'records': data,
                    'count': len(data)
                }
            else:
                return {'type': 'html', 'records': [], 'count': 0}
        
        except Exception as e:
            raise Exception(f"HTML processing error: {str(e)}")
    
    def _parse_player_data(self, text):
        """Parse player data from OCR text"""
        # This is a template - customize based on your FM26 screenshot format
        players = []
        
        # Example pattern matching for FM26 player rows
        lines = text.split('\n')
        
        for line in lines:
            if 'GR' in line or 'D(' in line or 'M' in line or 'PL' in line:
                # Parse player data
                parts = line.split()
                if len(parts) >= 5:
                    player = {
                        'name': ' '.join(parts[:-4]),
                        'position': parts[-4],
                        'age': parts[-3],
                        'minutes': parts[-2],
                        'goals': parts[-1]
                    }
                    players.append(player)
        
        return players
    
    def generate_insights(self, scores, team_level):
        """Generate actionable insights from scores"""
        insights = []
        
        # Analyze strengths and weaknesses
        players = scores['players']
        
        # Top performers
        top_performers = sorted(
            [p for p in players if p['status'] == 'Active'],
            key=lambda x: x['mustermann_score'],
            reverse=True
        )[:5]
        
        if top_performers:
            insights.append({
                'type': 'strength',
                'title': '⭐ Top Performers',
                'description': f"Your best players are {', '.join([p['name'] for p in top_performers])}",
                'players': [p['name'] for p in top_performers]
            })
        
        # Underperformers
        underperformers = [p for p in players if p['mustermann_score'] < 6.5 and p['status'] == 'Active']
        if underperformers:
            insights.append({
                'type': 'warning',
                'title': '⚠️ Underperformers',
                'description': f"{len(underperformers)} players are underperforming",
                'players': [p['name'] for p in underperformers[:5]]
            })
        
        # Position gaps
        position_coverage = {}
        for p in players:
            pos = p.get('position', 'Unknown')
            position_coverage[pos] = position_coverage.get(pos, 0) + 1
        
        gaps = [pos for pos, count in position_coverage.items() if count < 2]
        if gaps:
            insights.append({
                'type': 'opportunity',
                'title': '🎯 Position Gaps',
                'description': f"Consider recruiting in: {', '.join(gaps)}",
                'positions': gaps
            })
        
        return insights
    
    def generate_recommendations(self, scores, team_level):
        """Generate recruitment recommendations"""
        recommendations = []
        
        if team_level == 'title_contender':
            recommendations = [
                {
                    'priority': 'high',
                    'type': 'upgrade',
                    'description': 'Sign elite players (0.70+ Goals/90 for ST/W)',
                    'budget_range': '€15-50M'
                },
                {
                    'priority': 'high',
                    'type': 'strength',
                    'description': 'Recruit proven leaders in defense',
                    'budget_range': '€10-30M'
                }
            ]
        
        elif team_level == 'mid_table':
            recommendations = [
                {
                    'priority': 'high',
                    'type': 'quality',
                    'description': 'Sign good value players (0.45+ Goals/90)',
                    'budget_range': '€3-15M'
                },
                {
                    'priority': 'medium',
                    'type': 'depth',
                    'description': 'Build squad depth with young prospects',
                    'budget_range': '€1-5M'
                }
            ]
        
        elif team_level == 'relegation':
            recommendations = [
                {
                    'priority': 'critical',
                    'type': 'survival',
                    'description': 'Cheap proven strikers (0.30+ Goals/90)',
                    'budget_range': '€0.5-3M'
                },
                {
                    'priority': 'critical',
                    'type': 'defense',
                    'description': 'Solid defensive signings',
                    'budget_range': '€0.2-1M'
                }
            ]
        
        return recommendations
    
    def scout_search(self, criteria):
        """Search for undervalued players matching criteria"""
        # This would connect to a database of scouts players
        # For now, return template
        return {
            'criteria': criteria,
            'results': [],
            'message': 'Scout database integration coming soon'
        }
    
    def compare_squads(self, squads):
        """Compare multiple squads"""
        return {
            'squads': squads,
            'comparison': {}
        }
