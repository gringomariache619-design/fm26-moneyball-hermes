# 🎯 Moneyball FM26 - Setup & Deployment Guide

## 📋 Índice
1. [Requisitos](#requisitos)
2. [Setup Local (Mac/PC)](#setup-local)
3. [Deploy em Railway + Hermes](#deploy-railway)
4. [Como Usar](#como-usar)
5. [Troubleshooting](#troubleshooting)

---

## 📦 Requisitos

### Dependências Globais
- **Python 3.8+** (https://python.org)
- **Git** (https://git-scm.com)
- **Tesseract OCR** (para processamento de screenshots)

### Instalar Tesseract

**macOS:**
```bash
brew install tesseract
```

**Windows:**
1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer (use default path: `C:\Program Files\Tesseract-OCR`)
3. Add to PATH se necessário

---

## 🖥️ Setup Local

### Opção 1: Mac

```bash
# Clone ou download do projeto
cd ~/fm26-moneyball-hermes

# Criar virtual environment
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar Tesseract (se não instalado)
brew install tesseract

# Rodar em local
cd backend
python app.py

# Dashboard acessível em: http://localhost:5000
```

### Opção 2: Windows (PC)

```batch
# Clone ou download do projeto
cd C:\Users\YourUser\fm26-moneyball-hermes

# Criar virtual environment
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar Tesseract
# Download e instalar: https://github.com/UB-Mannheim/tesseract/wiki

# Rodar em local
cd backend
python app.py

# Dashboard acessível em: http://localhost:5000
```

### Opção 3: Docker (Mac/PC)

```bash
# Build da imagem
docker build -t moneyball-fm26 .

# Rodar container
docker run -p 5000:5000 moneyball-fm26

# Dashboard acessível em: http://localhost:5000
```

---

## 🚀 Deploy em Railway + Hermes

### Passo 1: Preparar GitHub

```bash
# Inicializar git (se não feito)
git init
git add .
git commit -m "Initial Moneyball FM26 system"

# Push para GitHub
git remote add origin https://github.com/USERNAME/fm26-moneyball-hermes.git
git branch -M main
git push -u origin main
```

### Passo 2: Conectar Railway

1. Ir para https://railway.app
2. Criar novo projeto → "Deploy from GitHub"
3. Conectar a sua conta GitHub
4. Selecionar o repositório `fm26-moneyball-hermes`
5. Railway vai detectar automaticamente o `Procfile`

### Passo 3: Configurar Variáveis de Ambiente

Em Railway Dashboard:
```
FLASK_ENV=production
PORT=8080
```

### Passo 4: Deploy

```bash
# Railway faz deploy automaticamente quando faz push para main
git push origin main

# Ver logs em Railway Dashboard → Logs
```

### Passo 5: Hermes Integration (Opcional)

Hermes permite webhooks para automação de scouting:

```bash
# Criar ficheiro: .hermes/config.yml

version: 1
name: "Moneyball FM26 Scout"
triggers:
  - type: "schedule"
    cron: "0 */6 * * *"  # A cada 6 horas
    action: "POST /api/scout-search"
    
  - type: "github"
    event: "push"
    action: "POST /api/analyze"
    
  - type: "webhook"
    path: "/hermes/scout-webhook"
    action: "POST /api/scout-search"

notifications:
  - type: "telegram"
    chat_id: "YOUR_CHAT_ID"
    template: "Scout found: {name} - {position} - €{price}M"
```

---

## 📖 Como Usar

### Upload de Dados

**Opção 1: CSV**
```
Formato esperado:
Player Name, Position, Age, Club, Minutes, Goals, Assists, Pass %, Goals/90, ...
João Silva, ST, 23, Sporting, 2400, 12, 3, 75%, 0.45, ...
```

**Opção 2: Screenshots FM26**
- Abra FM26 e faça screenshot da squad
- Arraste para o upload area
- Sistema processa automaticamente com OCR

**Opção 3: Export HTML do FM26**
- File → Export Data as HTML
- Arraste para o upload area

### Análise de Performance

1. **Upload** → Carregue dados
2. **Analysis** → Veja:
   - Top performers
   - Underperformers
   - Análise por posição
   - Recomendações Moneyball

### Scout Search

Pesquise undervalued players:
- Posição
- Campeonato (Ligue 2, LaLiga2, Campeonato PT, etc)
- Goals/90 mínimo
- Preço máximo
- Nível da equipa (Título, Meio, Descer)

Resultados estratificados por valor:
- **Candidatos ao Título**: Elite players €10-50M
- **Meio da Tabela**: Good value €3-15M
- **Candidatos a Descer**: Cheap €0.5-3M

### Exportar Análise

- CSV: para Excel/Sheets
- JSON: para programação
- PDF: (em desenvolvimento)

---

## 🔧 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'flask'"

```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Erro: "Tesseract not found"

**Mac:**
```bash
brew install tesseract
```

**Windows:**
- Instalar em: `C:\Program Files\Tesseract-OCR`
- Ou adicionar ao PATH

### Porta 5000 já em uso

```bash
# Mac/Linux: Encontrar processo
lsof -i :5000
kill -9 PID

# Windows: Usar porta diferente
python app.py --port 8000
```

### Railway deploy fails

```bash
# Verificar logs
railway logs

# Ver output do build
railway logs --builder

# Restart
railway down && railway up
```

### Screenshots não processam

- Certifique-se Tesseract está instalado
- Screenshot deve ter boa qualidade/contraste
- Suporta: PNG, JPG (recomendado PNG)

---

## 📊 Estrutura do Projeto

```
fm26-moneyball-hermes/
├── backend/
│   └── app.py              # Flask API principal
├── frontend/
│   └── templates/
│       └── index.html      # Dashboard moderno
├── scripts/
│   ├── moneyball_processor.py
│   └── mustermann_calculator.py
├── data/
│   └── uploads/            # Ficheiros uploaded
├── docs/
│   └── SETUP.md
├── Procfile                # Railway config
├── requirements.txt        # Dependencies
├── Dockerfile             # Docker config
└── .hermes/
    └── config.yml         # Hermes automation
```

---

## 🎯 Metodologia Mustermann FM

### Scoring por Posição

**ST (Striker):**
- Goals/90: 0.47 = Excellent
- xG/90: 0.40 = Excellent
- Shots/90: 2.81 = Excellent

**W (Winger):**
- Goals/90: 0.47 = Excellent
- Assists/90: 0.27 = Excellent
- Dribbles/90: 5.62 = Excellent

**AM (Attacking Mid):**
- Pass %: 68.83 = Excellent
- Key Passes/90: 2.08 = Excellent
- Goals/90: 0.25 = Excellent

**CM (Central Mid):**
- Pass %: 68.83 = Excellent
- Key Passes/90: 2.08 = Excellent
- Tackles Won %: 72.4 = Excellent

**DM (Defensive Mid):**
- Interceptions/90: 2.86 = Excellent
- Tackles Won %: 74.7 = Excellent
- Pass %: 68.83 = Excellent

**CB (Centre Back):**
- Tackles Won %: 76.7 = Excellent
- Pass %: 69.88 = Excellent
- Blocks/90: 0.75 = Excellent

**FB (Fullback):**
- Tackles Won %: 74.7 = Excellent
- Pass %: 69.88 = Excellent
- Interceptions/90: 2.88 = Excellent

**GK (Goalkeeper):**
- Pass %: 26.06 = Excellent
- Progressive Passes/90: 0.98 = Excellent

---

## 📞 Suporte

- **GitHub Issues**: Reporte bugs
- **Telegram**: @yourtelegramhandle
- **Email**: seu.email@example.com

---

## 📄 Licença

MIT License - Sinta-se livre para usar e modificar

---

**Última atualização**: Junho 2026
**Versão**: 1.0.0
**Status**: Production Ready ✅
