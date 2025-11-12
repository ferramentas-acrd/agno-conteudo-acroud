# ✍️ Redator Automático com IA

Aplicação completa para criação automatizada de conteúdo otimizado para SEO, com pesquisa em tempo real, geração de imagens e publicação direta no Google Docs.

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🚀 Funcionalidades

### ✨ Principais Recursos

- **🤖 Redação Automatizada**: Cria conteúdo completo usando IA (Llama 3.3 70B via Groq)
- **🔍 Pesquisa em Tempo Real**: Busca informações atualizadas automaticamente (Tavily API)
- **📝 Otimização SEO**: Formata conteúdo com headings, meta descriptions, keywords
- **🎨 Geração de Imagens**: Cria imagens personalizadas 1200x630px
- **📄 Publicação Automática**: Salva direto no Google Docs formatado
- **🧠 Sistema de Memória**: Aprende com exemplos de cada categoria
- **📊 Multi-Projetos**: Gerencia múltiplos projetos e categorias

### 🎯 Fluxo de Trabalho

```
1. Selecionar Projeto → 2. Escolher Categoria → 3. Palavra-chave
                                ↓
4. Pesquisa Automática → 5. Redação IA → 6. Gerar Imagem
                                ↓
7. Revisão → 8. Publicar no Google Docs
```

## 📋 Pré-requisitos

- Python 3.12+
- Conta Google (para Google Docs/Drive)
- API Keys (veja seção de Configuração)

## 🔧 Instalação

### 1. Instalar Dependências

**Usando UV (recomendado):**
```bash
cd redator_app
uv add streamlit google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pillow requests
```

**Ou usando pip:**
```bash
cd redator_app
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

Crie ou atualize o arquivo `.env` na raiz do projeto:

```bash
# IA e Pesquisa (já configuradas)
GROQ_API_KEY=gsk_...
TAVILY_API_KEY=tvly-...

# Google APIs (configure seguindo GOOGLE_API_SETUP.md)
GOOGLE_APPLICATION_CREDENTIALS=redator_app/config/credentials.json

# RapidAPI (Opcional - para imagens com IA)
RAPIDAPI_KEY=sua_chave  # Opcional
RAPIDAPI_HOST=host_da_api  # Opcional
```

### 3. Configurar Google APIs

📖 **Siga o guia completo:** [GOOGLE_API_SETUP.md](./GOOGLE_API_SETUP.md)

**Resumo rápido:**
1. Criar projeto no Google Cloud Console
2. Ativar Google Docs API e Google Drive API
3. Criar credenciais OAuth 2.0
4. Baixar `credentials.json` e colocar em `config/`
5. Na primeira execução, autenticar no navegador

## 🎮 Como Usar

### Iniciar a Aplicação

```bash
cd redator_app
streamlit run app.py
```

A aplicação abrirá automaticamente em: http://localhost:8501

### Primeiros Passos

#### 1️⃣ Criar Projeto

- Clique em **"Novo Projeto"**
- Dê um nome (ex: "Blog da Empresa")
- Adicione uma descrição

#### 2️⃣ Adicionar Categorias

Cada projeto pode ter várias categorias. Para cada categoria, forneça:

- **Nome**: Ex: "Tutorial", "Notícia", "Review"
- **Exemplo**: Cole um exemplo de conteúdo desta categoria
- **Regras**: Defina diretrizes (tom, estrutura, comprimento)

**Exemplo de Categoria:**

**Nome:** Tutorial Técnico

**Exemplo:**
```
Neste tutorial, você aprenderá passo a passo como...

## O que você precisa
- Requisito 1
- Requisito 2

## Passo 1: Configuração
Primeiro, vamos configurar...
```

**Regras:**
```
- Use tom didático e claro
- Inclua exemplos práticos
- Mínimo 1000 palavras
- Adicione screenshots quando possível
- Termine com próximos passos
```

#### 3️⃣ Gerar Conteúdo

1. Selecione o projeto
2. Escolha a categoria
3. Digite a palavra-chave (ex: "Python para iniciantes")
4. Clique em **"Gerar Conteúdo Completo"**

A IA irá:
- 🔍 Pesquisar informações atualizadas
- ✍️ Escrever o artigo completo
- 🎨 Gerar imagem personalizada
- 📊 Otimizar para SEO

#### 4️⃣ Revisar e Publicar

- Revise o conteúdo gerado
- Edite se necessário
- Clique em **"Salvar no Google Docs"**
- Ou baixe como HTML

## 📁 Estrutura do Projeto

```
redator_app/
├── app.py                          # Aplicação principal Streamlit
├── memoria/
│   ├── gerenciador_memoria.py      # Gerencia projetos e categorias
│   └── dados/
│       └── projetos.json           # Banco de dados local
├── agents/
│   ├── agente_pesquisador.py       # Pesquisa com Tavily
│   ├── agente_redator.py           # Gera conteúdo SEO
│   └── gerador_imagem.py           # Cria imagens
├── utils/
│   └── google_docs_handler.py      # Integração Google Docs
├── config/
│   ├── credentials.json            # Credenciais Google (você cria)
│   └── token.json                  # Token OAuth (gerado automaticamente)
├── imagens_geradas/                # Imagens criadas
├── requirements.txt                # Dependências Python
├── GOOGLE_API_SETUP.md            # Guia de configuração das APIs
└── README.md                       # Este arquivo
```

## 🎨 Exemplos de Uso

### Exemplo 1: Blog de Tecnologia

**Projeto:** Blog Tech News  
**Categoria:** Análise de Produto  
**Palavra-chave:** "iPhone 15 Pro Max"

**Resultado:**
- Artigo de 1200+ palavras
- Pesquisa sobre especificações atuais
- Comparação com concorrentes
- Imagem de destaque profissional
- Otimizado para SEO

### Exemplo 2: E-commerce

**Projeto:** Loja Virtual Fashion  
**Categoria:** Guia de Estilo  
**Palavra-chave:** "como combinar tênis branco"

**Resultado:**
- Guia completo com dicas
- Tendências atuais de moda
- Sugestões de combinações
- Imagem atraente
- Keywords de produtos

## 🔒 Segurança e Boas Práticas

### Não Compartilhe

- ❌ `credentials.json`
- ❌ `token.json`
- ❌ `.env`

### Adicione ao .gitignore

```gitignore
# Credenciais
config/credentials.json
config/token.json
.env

# Dados sensíveis
memoria/dados/

# Imagens geradas
imagens_geradas/

# Cache Python
__pycache__/
*.pyc
.streamlit/
```

## 🐛 Solução de Problemas

### Erro: "Module 'agno' not found"

```bash
cd /Users/caiobessa/Desktop/Agno\ Acroud
uv add agno
```

### Erro: "Google credentials not found"

Certifique-se de ter configurado as APIs do Google.  
Veja: [GOOGLE_API_SETUP.md](./GOOGLE_API_SETUP.md)

### Erro: "GROQ_API_KEY not set"

Verifique se o arquivo `.env` está na raiz do projeto principal.

### Imagens não estão sendo geradas

**Solução 1:** Sem RapidAPI (usa gerador de texto estilizado)
- Funciona automaticamente
- Cria imagens bonitas com texto

**Solução 2:** Com RapidAPI (imagens IA)
- Configure RAPIDAPI_KEY no `.env`
- Veja seção de RapidAPI no guia

## 📊 Estatísticas e Métricas

A aplicação fornece:

- ✅ Contagem de palavras
- ✅ Tempo estimado de leitura
- ✅ Total de parágrafos
- ✅ Densidade de palavra-chave
- ✅ SEO score (básico)

## 🔄 Atualizações Futuras

### Em Desenvolvimento

- [ ] Análise de concorrentes
- [ ] Integração com WordPress
- [ ] Agendamento de posts
- [ ] A/B Testing de títulos
- [ ] Analytics integrado
- [ ] Sugestões de imagens do Unsplash

## 📝 Licença

MIT License - veja LICENSE para detalhes

## 🤝 Contribuindo

Contribuições são bem-vindas!

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 💬 Suporte

Encontrou um problema ou tem uma sugestão?
- 📧 Email: seu@email.com
- 🐛 Issues: GitHub Issues

## 🙏 Agradecimentos

- **Groq** - IA ultrarrápida
- **Tavily** - Pesquisa otimizada para IA
- **Google** - APIs de documentos
- **Streamlit** - Framework web incrível
- **Agno** - Framework de agentes

---

**Feito com ❤️ usando IA e Python**

🚀 **Pronto para criar conteúdo incrível automaticamente!**

