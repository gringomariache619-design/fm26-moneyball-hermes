# 🎯 Moneyball FM26 - Modern Performance Analysis System

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey.svg)](https://flask.palletsprojects.com)
[![Railway Ready](https://img.shields.io/badge/Railway-Ready-0B0D47.svg)](https://railway.app)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 🚀 **Análise profissional de performance em FM26 com Metodologia Mustermann FM**
> 
> Suporta: **Screenshots** | **CSV** | **HTML** | **Mac & PC** | **Deploy em Railway + Hermes**

---

## ✨ Características Principais

### 📊 Análise Avançada
- ✅ **Scoring Mustermann FM** - Benchmarks por posição
- ✅ **Performance Analysis** - Identifique problemas
- ✅ **Undervalue Detection** - Encontre bargains no mercado
- ✅ **Position Intelligence** - Análise por posição

### 📤 Input Flexível
- ✅ **Screenshots** - Arraste screenshots do FM26 (OCR automático)
- ✅ **CSV** - Exporte dados em CSV
- ✅ **HTML** - Importe exports HTML do FM26
- ✅ **Multi-file** - Processe múltiplos ficheiros

### 🎨 Dashboard Moderno
- ✅ **Dark Mode** - Design moderno e profissional
- ✅ **Responsive** - Funciona em qualquer dispositivo
- ✅ **Tabbed Interface** - Navegação intuitiva
- ✅ **Real-time Stats** - Atualizações ao vivo

### 🌍 Scouts Inteligentes
- ✅ **Multi-liga** - Ligue 2, LaLiga2, Liga 3 PT, Serie B, etc
- ✅ **Critérios Flexíveis** - Goals/90, Preço, Posição, Idade
- ✅ **Estratificado** - Candidatos, Meio, Descer
- ✅ **Análise de Valor** - Encontre undervalued players

### 🚀 Deployment Profissional
- ✅ **Railway Ready** - Deploy em 1 clique
- ✅ **Hermes Integration** - Automação com webhooks
- ✅ **Mac & PC** - Funciona em qualquer OS
- ✅ **Docker Support** - Containerizado

---

## 🚀 Quick Start (3 minutos)

### 1️⃣ Clone / Download

```bash
git clone https://github.com/username/fm26-moneyball-hermes.git
cd fm26-moneyball-hermes
```

### 2️⃣ Setup

**Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
brew install tesseract
cd backend && python app.py
```

**Windows:**
```batch
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
cd backend && python app.py
```

### 3️⃣ Abrir Dashboard

Navegue para: **http://localhost:5000**

---

## 📖 Como Usar

### Passo 1: Upload de Dados

```
Suportados:
✓ CSV files
✓ Screenshots PNG/JPG (com OCR automático)
✓ HTML exports do FM26
```

Arraste ou clique para fazer upload → Sistema processa automaticamente

### Passo 2: Análise

Veja:
- 📊 **Top Performers** - Melhores players
- ⚠️ **Underperformers** - Problemas a resolver
- 📍 **Position Analysis** - Cobertura por posição
- 💡 **Insights** - Recomendações actionáveis

### Passo 3: Scout Search

Pesquise undervalued players:
- Selecione posição
- Escolha campeonato (Ligue 2, LaLiga2, etc)
- Define Goals/90 mínimo
- Define preço máximo
- Filtro por nível de equipa

### Passo 4: Exportar

Export para:
- 📊 CSV (Excel/Sheets)
- 📄 JSON (API/Programação)
- 🔒 PDF (em desenvolvimento)

---

## 🎯 Metodologia Mustermann FM

Sistema baseado em benchmarks comprovados por posição:

### ST (Striker)
```
Elite:    Goals/90 ≥ 0.47 | xG/90 ≥ 0.40
Good:     Goals/90 ≥ 0.37 | xG/90 ≥ 0.32
Fair:     Goals/90 ≥ 0.29 | xG/90 ≥ 0.26
Poor:     Goals/90 < 0.22
```

### W (Winger)
```
Elite:    Goals/90 ≥ 0.47 | Assists/90 ≥ 0.27
Good:     Goals/90 ≥ 0.37 | Assists/90 ≥ 0.22
Fair:     Goals/90 ≥ 0.29 | Assists/90 ≥ 0.17
Poor:     Goals/90 < 0.22
```

### CB (Centre Back)
```
Elite:    Tackles Won % ≥ 76.7 | Pass % ≥ 69.88
Good:     Tackles Won % ≥ 74.7 | Pass % ≥ 62.33
Fair:     Tackles Won % ≥ 72.4 | Pass % ≥ 56.45
Poor:     Tackles Won % < 72.0
```

> **Nota:** Benchmarks completos incluem DM, CM, AM, FB, GK, etc.

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────┐
│         Frontend (HTML/CSS/JS)          │
│    Modern Dashboard with Dark Mode      │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Flask Backend API (Python)         │
│  • File Processing (CSV/IMG/HTML)       │
│  • Moneyball Calculations               │
│  • Scout Search                         │
│  • Export Functions                     │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Processing Engines                 │
│  • MoneyballProcessor                   │
│  • MustermannCalculator                 │
│  • OCR (Tesseract)                      │
│  • CSV/HTML Parser                      │
└─────────────────────────────────────────┘
```

---

## 🚀 Deploy em Railway

### 1. Push para GitHub

```bash
git add .
git commit -m "Moneyball FM26 system"
git push origin main
```

### 2. Railway Dashboard

1. Ir para https://railway.app
2. New Project → Deploy from GitHub
3. Conectar repositório
4. Railway detecta `Procfile` automaticamente

### 3. Set Environment Variables

```
FLASK_ENV=production
PORT=8080
TESSERACT_PATH=/usr/bin/tesseract
```

### 4. Deploy

```bash
# Automático ao fazer push
git push origin main

# Ver live em: https://your-app.railway.app
```

---

## 🔗 Hermes Integration (Automação)

Configure webhooks automáticos para scout searches:

```bash
# .hermes/config.yml
triggers:
  - schedule: "0 */6 * * *"  # A cada 6 horas
    action: "POST /api/scout-search"
    
  - webhook: "/hermes/scout"
    action: "Notificar players encontrados"
```

---

## 📋 Requisitos

- **Python 3.8+**
- **Tesseract OCR**
- **Git** (para deploy)
- **Railway Account** (para deploy na cloud)

---

## 📁 Estrutura

```
fm26-moneyball-hermes/
├── backend/
│   └── app.py              # API Principal
├── frontend/
│   └── templates/
│       └── index.html      # Dashboard
├── scripts/
│   ├── moneyball_processor.py
│   └── mustermann_calculator.py
├── data/
│   └── uploads/            # Ficheiros
├── SETUP.md                # Guia Completo
├── README.md               # Este ficheiro
├── requirements.txt
├── Procfile
└── Dockerfile
```

---

## 🔧 Troubleshooting

| Erro | Solução |
|------|---------|
| `ModuleNotFoundError` | `pip install -r requirements.txt --force-reinstall` |
| `Tesseract not found` | `brew install tesseract` (Mac) ou download Windows |
| `Port 5000 in use` | Mudar porta: `python app.py --port 8000` |
| `Screenshot não funciona` | Verificar qualidade/contraste do screenshot |

---

## 📊 Exemplos

### Upload CSV
```csv
Player Name,Position,Age,Minutes,Goals,Pass %,Goals/90
João Silva,ST,23,2400,12,75%,0.45
```

### Scout Search
```json
{
  "position": "ST",
  "league": "ligue2",
  "min_goals_per_90": 0.40,
  "max_price": 10,
  "team_level": "title"
}
```

### Export Results
```bash
# CSV Export
GET /api/export/csv

# JSON Export
GET /api/export/json
```

---

## 🤝 Contribuições

Pull requests são bem-vindos! Para mudanças maiores, abra uma issue primeiro.

---

## 📝 Licença

MIT License - Veja LICENSE para detalhes

---

## 👤 Autor

**Hugo** - Football Manager Analytics
- GitHub: [@username]
- Email: seu.email@example.com
- Discord: yourdiscord#1234

---

## 🎯 Roadmap

- [x] Dashboard moderno
- [x] Upload multifile
- [x] Scoring Mustermann
- [x] Scout search
- [ ] PDF export
- [ ] Machine learning predictions
- [ ] Real-time transfermarkt sync
- [ ] Mobile app

---

## 💬 Suporte

Tem dúvidas ou encontrou um bug?
- 🐛 **GitHub Issues**: Reporte aqui
- 💬 **Discussions**: Pergunte na comunidade
- 📧 **Email**: seu.email@example.com

---

**Made with ❤️ for Football Manager lovers**

🚀 **Deploy Ready** | 🎯 **Modern Design** | 📊 **Professional Analysis** | ⚡ **Fast Processing**

---

Last Updated: June 2026 | Version: 1.0.0 | Status: ✅ Production Ready
