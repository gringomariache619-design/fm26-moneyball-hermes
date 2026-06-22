"""
Mustermann FM Calculator
Implements Mustermann FM scoring methodology for FM26
"""

class MustermannCalculator:
    """Calculate Mustermann FM scores for players"""
    
    def __init__(self):
        self.benchmarks = self._load_benchmarks()
    
    def _load_benchmarks(self):
        """Load Mustermann FM benchmarks"""
        return {
            'CB': {'excellent': {'tackle_win': 76.7, 'pass_pct': 69.88}, 'good': {'tackle_win': 74.7, 'pass_pct': 62.33}},
            'FB': {'excellent': {'tackle_win': 74.7, 'pass_pct': 69.88}, 'good': {'tackle_win': 72.4, 'pass_pct': 62.33}},
            'DM': {'excellent': {'pass_pct': 68.83, 'key_passes_p90': 2.08}, 'good': {'pass_pct': 60.74, 'key_passes_p90': 1.6}},
            'CM': {'excellent': {'pass_pct': 68.83, 'goals_p90': 0.20}, 'good': {'pass_pct': 60.74, 'goals_p90': 0.15}},
            'AM': {'excellent': {'pass_pct': 68.83, 'goals_p90': 0.25}, 'good': {'pass_pct': 60.74, 'goals_p90': 0.18}},
            'W': {'excellent': {'goals_p90': 0.47, 'assists_p90': 0.27}, 'good': {'goals_p90': 0.37, 'assists_p90': 0.22}},
            'ST': {'excellent': {'goals_p90': 0.47, 'xg_p90': 0.40}, 'good': {'goals_p90': 0.37, 'xg_p90': 0.32}},
            'GK': {'excellent': {'pass_pct': 26.06}, 'good': {'pass_pct': 24.38}}
        }
    
    def calculate_squad_scores(self, squad_data):
        """Calculate scores for entire squad"""
        players = []
        
        for player in squad_data:
            score = self._calculate_player_score(player)
            players.append({
                **player,
                'mustermann_score': score['score'],
                'performance_level': score['level']
            })
        
        # Sort by score
        players.sort(key=lambda x: x['mustermann_score'], reverse=True)
        
        # Calculate summary
        summary = {
            'total_players': len(players),
            'average_score': sum(p['mustermann_score'] for p in players) / len(players) if players else 0,
            'elite_count': len([p for p in players if p['mustermann_score'] >= 8.0]),
            'good_count': len([p for p in players if 7.0 <= p['mustermann_score'] < 8.0]),
            'fair_count': len([p for p in players if 6.0 <= p['mustermann_score'] < 7.0]),
            'poor_count': len([p for p in players if p['mustermann_score'] < 6.0])
        }
        
        return {
            'players': players,
            'summary': summary
        }
    
    def _calculate_player_score(self, player):
        """Calculate individual player score"""
        position = player.get('position', 'CM')
        
        # Base scoring logic (simplified)
        score = 6.0  # Base score
        
        # Factor in goals/90 if available
        goals_p90 = float(player.get('goals_p90', 0))
        if goals_p90 > 0:
            score += goals_p90 * 2
        
        # Factor in pass percentage
        pass_pct = float(player.get('pass_pct', 50))
        if pass_pct >= 75:
            score += 1.0
        elif pass_pct >= 65:
            score += 0.5
        
        # Factor in assists
        assists_p90 = float(player.get('assists_p90', 0))
        if assists_p90 > 0:
            score += assists_p90 * 1.5
        
        # Determine level
        if score >= 8.5:
            level = 'Elite'
        elif score >= 7.5:
            level = 'Good'
        elif score >= 6.5:
            level = 'Fair'
        else:
            level = 'Poor'
        
        # Cap at 10
        score = min(score, 10.0)
        score = max(score, 1.0)
        
        return {
            'score': round(score, 2),
            'level': level
        }
    
    def get_benchmarks(self):
        """Return benchmark data"""
        return self.benchmarks
