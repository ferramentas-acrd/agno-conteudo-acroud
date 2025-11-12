#!/bin/bash

# Script de Instalação - Redator Automático com IA
# Este script configura tudo automaticamente

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🚀 INSTALANDO REDATOR AUTOMÁTICO COM IA                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Verificar Python
echo "📋 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.12+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION encontrado"
echo ""

# Verificar UV
echo "📋 Verificando UV package manager..."
if ! command -v uv &> /dev/null; then
    echo "⚠️  UV não encontrado. Usando pip..."
    USE_UV=false
else
    echo "✅ UV encontrado"
    USE_UV=true
fi
echo ""

# Criar diretórios necessários
echo "📁 Criando estrutura de diretórios..."
mkdir -p config
mkdir -p memoria/dados
mkdir -p imagens_geradas
echo "✅ Diretórios criados"
echo ""

# Instalar dependências
echo "📦 Instalando dependências..."
if [ "$USE_UV" = true ]; then
    echo "Usando UV..."
    cd ..
    uv add streamlit google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pillow requests
    cd redator_app
else
    echo "Usando pip..."
    pip3 install -r requirements.txt
fi
echo "✅ Dependências instaladas"
echo ""

# Configurar .env
echo "⚙️  Configurando variáveis de ambiente..."
if [ ! -f "../.env" ]; then
    echo "❌ Arquivo .env não encontrado no diretório pai"
    echo "📝 Criando .env de exemplo..."
    cp .env.example ../.env
    echo "✅ Arquivo .env criado. Por favor, configure suas API keys!"
else
    echo "✅ Arquivo .env já existe"
fi
echo ""

# Verificar APIs configuradas
echo "🔍 Verificando configuração de APIs..."

if grep -q "GROQ_API_KEY=gsk_" ../.env 2>/dev/null; then
    echo "✅ GROQ_API_KEY configurada"
else
    echo "⚠️  GROQ_API_KEY não configurada"
fi

if grep -q "TAVILY_API_KEY=tvly-" ../.env 2>/dev/null; then
    echo "✅ TAVILY_API_KEY configurada"
else
    echo "⚠️  TAVILY_API_KEY não configurada"
fi

if [ -f "config/credentials.json" ]; then
    echo "✅ Google credentials.json encontrado"
else
    echo "⚠️  Google credentials.json não encontrado"
    echo "📖 Veja GOOGLE_API_SETUP.md para instruções"
fi
echo ""

# Criar .gitignore
echo "🔒 Configurando .gitignore..."
cat > .gitignore << 'EOF'
# Credenciais e Segurança
config/credentials.json
config/token.json
.env

# Dados
memoria/dados/

# Imagens Geradas
imagens_geradas/*.png
imagens_geradas/*.jpg

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# Streamlit
.streamlit/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
EOF
echo "✅ .gitignore criado"
echo ""

# Mensagem final
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   ✅ INSTALAÇÃO CONCLUÍDA!                                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📝 PRÓXIMOS PASSOS:"
echo ""
echo "1. Configure suas API Keys no arquivo .env:"
echo "   - GROQ_API_KEY (obrigatória)"
echo "   - TAVILY_API_KEY (obrigatória)"
echo ""
echo "2. Configure Google APIs:"
echo "   📖 Siga: GOOGLE_API_SETUP.md"
echo "   - Ative Google Docs e Drive APIs"
echo "   - Baixe credentials.json"
echo "   - Coloque em: config/credentials.json"
echo ""
echo "3. (Opcional) Configure RapidAPI para imagens com IA"
echo ""
echo "4. Execute a aplicação:"
echo "   cd redator_app"
echo "   streamlit run app.py"
echo ""
echo "🚀 Pronto para criar conteúdo incrível automaticamente!"
echo ""

