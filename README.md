# 🤖 Agno Conteúdo ACROUD - Redator Automático com IA

Sistema inteligente para geração de conteúdo automatizado usando IA, com suporte a múltiplos projetos, categorias e geração de imagens.

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 🎯 Sobre o Projeto

O **Agno Conteúdo ACROUD** é uma plataforma completa para geração automatizada de conteúdo de alta qualidade usando inteligência artificial. Ideal para blogs, sites de notícias, e-commerce e marketing de conteúdo.

### ✨ Principais Funcionalidades

- 🔍 **Pesquisa Automática:** Busca informações atualizadas na web usando Tavily API
- ✍️ **Redação com IA:** Gera conteúdo otimizado para SEO usando Groq (Llama 3.3 70B)
- 🎨 **Geração de Imagens:** Suporta DALL-E 3, Replicate (Flux) e fallback com texto
- 💾 **Armazenamento Híbrido:** Local (JSON) ou nuvem (Supabase PostgreSQL)
- 📂 **Multi-Projetos:** Organize conteúdos por projetos e categorias
- 🧠 **Memória Inteligente:** Exemplos e regras por categoria para consistência
- 📊 **Estatísticas:** Histórico completo com busca e analytics
- 📄 **Google Docs:** Publicação automática (em desenvolvimento)

---

## 🚀 Quick Start

### Pré-requisitos

- Python 3.10+
- UV (gerenciador de pacotes)
- Chaves de API: Groq, Tavily

### Instalação Rápida

```bash
# 1. Clonar repositório
git clone https://github.com/ferramentas-acrd/agno-conteudo-acroud.git
cd agno-conteudo-acroud

# 2. Instalar UV (se ainda não tiver)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Criar arquivo .env com suas chaves
cp .env.example .env
# Edite .env e adicione suas API keys

# 4. Instalar dependências
uv sync

# 5. Rodar aplicação Streamlit
uv run streamlit run redator_app/app.py
```

Acesse: http://localhost:8501

---

## 📁 Estrutura do Projeto

```
agno-conteudo-acroud/
├── redator_app/                    # Aplicação Streamlit principal
│   ├── app.py                      # Interface principal
│   ├── agents/                     # Agentes de IA
│   │   ├── agente_pesquisador.py   # Pesquisa web
│   │   ├── agente_redator.py       # Geração de conteúdo
│   │   └── gerador_imagem.py       # Geração de imagens
│   ├── memoria/                    # Sistema de memória
│   │   ├── gerenciador_memoria.py  # Gerencia projetos/categorias
│   │   └── dados/                  # Dados locais (JSON)
│   ├── utils/                      # Utilitários
│   │   ├── supabase_handler.py     # Integração Supabase
│   │   └── google_docs_handler.py  # Google Docs API
│   ├── requirements.txt            # Dependências Python
│   └── *.md                        # Documentação
├── agentos.py                      # AgentOS backend
├── pyproject.toml                  # Configuração UV
├── .env.example                    # Exemplo de variáveis
└── README.md                       # Este arquivo
```

---

## 🔑 Configuração de APIs

### Obrigatórias

#### 1. Groq API (LLM)
- **Onde:** https://console.groq.com
- **Como:** Criar conta → API Keys → Criar nova key
- **Custo:** Gratuito (até 14.400 requisições/dia)

#### 2. Tavily API (Pesquisa)
- **Onde:** https://tavily.com
- **Como:** Sign up → Dashboard → Copiar API Key
- **Custo:** Gratuito (1.000 pesquisas/mês)

### Opcionais

#### 3. Supabase (Histórico em Nuvem)
- **Onde:** https://supabase.com
- **Guia:** `redator_app/SUPABASE_SETUP.md`
- **Custo:** Gratuito (500MB)

#### 4. OpenAI / Replicate (Imagens IA)
- **OpenAI:** https://platform.openai.com
- **Replicate:** https://replicate.com
- **Guia:** `redator_app/CONFIGURACAO_IMAGENS_IA.md`

#### 5. Google Cloud (Docs API)
- **Onde:** https://console.cloud.google.com
- **Guia:** `redator_app/GOOGLE_API_SETUP.md`

---

## 📝 Arquivo .env

Crie um arquivo `.env` na raiz:

```bash
# === OBRIGATÓRIAS ===
GROQ_API_KEY=gsk_...
TAVILY_API_KEY=tvly-...

# === OPCIONAIS ===

# Supabase (Histórico)
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=eyJhbG...

# Imagens com IA
OPENAI_API_KEY=sk-...
REPLICATE_API_TOKEN=r8_...

# Google Docs
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
```

---

## 💻 Uso Básico

### 1. Criar Projeto

```
1. Sidebar → "➕ Novo Projeto"
2. Nome: "Meu Blog"
3. Descrição: "Blog sobre tecnologia"
4. Criar
```

### 2. Criar Categoria

```
1. Selecionar projeto
2. "➕ Nova Categoria"
3. Nome: "Tutorial"
4. Exemplo: "Neste tutorial você aprenderá..."
5. Regras: "Use tom didático, passo a passo..."
6. Criar
```

### 3. Gerar Conteúdo

```
1. Selecionar projeto e categoria
2. Digite palavra-chave: "Python para iniciantes"
3. "🚀 Gerar Conteúdo Completo"
4. Aguardar 30-60 segundos
5. Revisar e publicar!
```

---

## 🏗️ Arquitetura

### Backend: Agno AgentOS

```python
# agentos.py - Sistema de agentes
- Web Agent: Pesquisa web geral
- Finance Agent: Dados financeiros (YFinance)
- Research Agent: Pesquisa acadêmica
```

Porta: http://localhost:7777

### Frontend: Streamlit

```python
# redator_app/app.py - Interface visual
- Gerenciamento de projetos
- Geração de conteúdo
- Visualização de resultados
```

Porta: http://localhost:8501

---

## 🎨 Geração de Imagens

### Ordem de Prioridade:

1. **DALL-E 3** (OpenAI) - Melhor qualidade, $0.04/imagem
2. **Flux Schnell** (Replicate) - Grátis, boa qualidade
3. **Fallback** - Texto estilizado, sempre funciona

### Configuração:

Veja documentação completa: `redator_app/CONFIGURACAO_IMAGENS_IA.md`

---

## 💾 Armazenamento

### Modo Local (Padrão)

- Arquivos JSON em `redator_app/memoria/dados/`
- Funciona offline
- Sem histórico persistente de conteúdos

### Modo Supabase (Recomendado)

- PostgreSQL na nuvem
- Histórico completo de todos os conteúdos
- Busca full-text
- Estatísticas em tempo real
- Backup automático

**Guia:** `redator_app/SUPABASE_SETUP.md`

---

## 📊 Tecnologias Utilizadas

### Core

- **[Python 3.10+](https://python.org)** - Linguagem principal
- **[UV](https://github.com/astral-sh/uv)** - Gerenciador de pacotes
- **[Streamlit](https://streamlit.io)** - Interface web
- **[Agno](https://agno.com)** - Framework de agentes

### IA & APIs

- **[Groq](https://groq.com)** - LLM (Llama 3.3 70B)
- **[Tavily](https://tavily.com)** - Busca web para IA
- **[OpenAI](https://openai.com)** - DALL-E 3
- **[Replicate](https://replicate.com)** - Flux models

### Dados

- **[Supabase](https://supabase.com)** - PostgreSQL gerenciado
- **[Google Docs API](https://developers.google.com/docs)** - Publicação

---

## 📚 Documentação Completa

- **[QUICK_START.md](redator_app/QUICK_START.md)** - Início rápido
- **[SUPABASE_SETUP.md](redator_app/SUPABASE_SETUP.md)** - Configurar banco de dados
- **[CONFIGURACAO_IMAGENS_IA.md](redator_app/CONFIGURACAO_IMAGENS_IA.md)** - Geração de imagens
- **[GOOGLE_API_SETUP.md](redator_app/GOOGLE_API_SETUP.md)** - Google Docs
- **[RESUMO_PROJETO.md](redator_app/RESUMO_PROJETO.md)** - Arquitetura técnica

---

## 🐛 Solução de Problemas

### ModuleNotFoundError: No module named 'agno'

```bash
cd /caminho/do/projeto
uv sync
uv run streamlit run redator_app/app.py
```

### API Key não encontrada

```bash
# Verifique se .env existe e está na raiz
cat .env

# Deve conter:
GROQ_API_KEY=...
TAVILY_API_KEY=...
```

### Carregamento infinito

- Verifique se as APIs estão configuradas corretamente
- Veja logs no terminal onde o Streamlit está rodando
- Recarregue a página (F5)

### Mais problemas?

Abra uma [issue no GitHub](https://github.com/ferramentas-acrd/agno-conteudo-acroud/issues)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! 

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

---

## 👥 Autores

**ACROUD Team**

- 🌐 Website: [ferramentas-acrd](https://github.com/ferramentas-acrd)
- 📧 Email: contato@acroud.com

---

## 🙏 Agradecimentos

- [Agno](https://agno.com) - Framework de agentes
- [Groq](https://groq.com) - Inferência rápida de LLMs
- [Tavily](https://tavily.com) - API de busca para IA
- [Supabase](https://supabase.com) - Backend como serviço

---

## 📈 Roadmap

- [x] Sistema de projetos e categorias
- [x] Geração de conteúdo com IA
- [x] Integração Supabase
- [x] Geração de imagens (DALL-E 3 + Replicate)
- [ ] Publicação automática no Google Docs
- [ ] Integração WordPress
- [ ] Agendamento de publicações
- [ ] API REST pública
- [ ] Dashboard de analytics
- [ ] Suporte a múltiplos idiomas
- [ ] Editor de conteúdo WYSIWYG

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ferramentas-acrd/agno-conteudo-acroud&type=Date)](https://star-history.com/#ferramentas-acrd/agno-conteudo-acroud&Date)

---

<div align="center">

**Feito com ❤️ pela equipe ACROUD**

[⬆ Voltar ao topo](#-agno-conteúdo-acroud---redator-automático-com-ia)

</div>

