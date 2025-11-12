# 📋 Instruções Globais do Sistema

## 🎯 Objetivo

Este documento explica como as **Instruções Globais** foram implementadas no sistema para garantir que TODOS os conteúdos gerados sigam diretrizes rigorosas de qualidade, SEO, legalidade e E-E-A-T.

---

## 🏗️ Arquitetura

### Arquivo Central: `config/instrucoes_globais.py`

Este arquivo contém **TODAS** as diretrizes que os agentes de IA **NUNCA podem esquecer**:

- ✅ Identidade e papel (jornalista especializado em iGaming)
- ✅ Requisitos de SEO (palavra-chave, headings, meta tags)
- ✅ Legalidade (Lei 14.790/23, operadoras licenciadas)
- ✅ Fontes confiáveis (governo, acadêmicas, internacionais)
- ✅ Qualidade Google (E-E-A-T, YMYL)
- ✅ Formatação (parágrafos, listas, tabelas, negrito)
- ✅ O que evitar (frases vagas, repetições, enchimento)
- ✅ Checklist pré-publicação

---

## 🤖 Integração nos Agentes

### 1. **Agente Pesquisador** (`agents/agente_pesquisador.py`)

```python
from config.instrucoes_globais import get_instrucoes_globais

instrucoes_globais = get_instrucoes_globais()
```

**O que faz:**
- Prioriza fontes confiáveis listadas nas instruções
- Busca dados sobre casas LICENCIADAS
- Inclui contexto geográfico (Brasil) e temporal
- Cita fontes com URLs

### 2. **Agente Redator** (`agents/agente_redator.py`)

```python
from config.instrucoes_globais import get_instrucoes_globais

instrucoes_globais = get_instrucoes_globais()
```

**O que faz:**
- Aplica checklist pré-publicação
- Segue boas práticas de SEO
- Usa formatação específica (parágrafos curtos, listas, tabelas)
- Evita frases vagas e genéricas
- Enriquece com dados reais

---

## 📚 Conteúdo das Instruções Globais

### 🎭 Identidade
- Jornalista brasileiro especializado em iGaming e SEO/GEO
- Estilo profissional e educativo
- Foco em jogo responsável

### 📝 Requisitos de SEO
- Palavra-chave no H1 (MAS NÃO no 1º parágrafo)
- Meta title (até 60 caracteres)
- Meta description (até 160 caracteres)
- Headings estruturados (H1, H2, H3)
- Distribuição natural de palavras-chave

### ⚖️ Legalidade
- Lei 14.790/23 (regulamentação de apostas no Brasil)
- Apenas operadoras licenciadas:
  - bet365, Superbet, Betnacional, Betsson, KTO, Esportivabet, VBet, Esportes da Sorte
- Alertas de jogo responsável

### 📊 Fontes Confiáveis

**Governo:**
- Agência Brasil, Senado, Câmara, Receita Federal, Ministério da Fazenda, Secretaria de Prêmios e Apostas

**Acadêmicas:**
- IBGE, IPEA, FGV, SciELO, Google Scholar

**Internacionais:**
- UK Gambling Commission, GREF, WHO, Statista

**Jogo Responsável:**
- Gambling Therapy, GamCare, Jogo Responsável (Brasil)

### 🎨 Formatação
- Parágrafos curtos (~50 palavras)
- Listas (bullets/numeradas)
- Tabelas para comparações
- Negrito em pontos estratégicos
- FAQs internas

### ❌ O Que Evitar
- "As apostas esportivas têm crescido nos últimos anos..."
- Frases vagas e genéricas
- Repetições desnecessárias
- Enchimento de texto sem valor

### ✅ Checklist Pré-Publicação
1. Responde à intenção de busca?
2. Há dados práticos (odds, estatísticas, leis)?
3. Entrega valor real?
4. Livre de repetições?
5. Menciona jogo responsável?
6. Só cita operadoras licenciadas?
7. Seguiu diretrizes de SEO?
8. Aplicou E-E-A-T?

---

## 🔒 Garantia de Aplicação

### As instruções são aplicadas em **3 níveis**:

#### 1️⃣ **Nível Sistema**
Arquivo `config/instrucoes_globais.py` com função `get_instrucoes_globais()`

#### 2️⃣ **Nível Agente**
Cada agente importa e injeta as instruções no prompt:

```python
instrucoes_completas = [
    instrucoes_globais,
    "---",
    "INSTRUÇÕES ESPECÍFICAS DO AGENTE:",
    *instrucoes_especificas
]
```

#### 3️⃣ **Nível Visual**
Avisos explícitos no prompt:

```
⚠️ INSTRUÇÕES GLOBAIS - NUNCA ESQUECER ⚠️
```

---

## 🧪 Como Testar

### 1. Gerar Conteúdo Padrão
- Selecione projeto e categoria
- Digite palavra-chave
- Gere conteúdo
- **Verifique**: SEO, legalidade, formatação

### 2. Testar Checklist
Pergunte ao conteúdo gerado:
- ✅ Tem meta title e description?
- ✅ Palavra-chave está no H1?
- ✅ Cita apenas operadoras licenciadas?
- ✅ Tem alertas de jogo responsável?
- ✅ Usa parágrafos curtos e listas?
- ✅ Evita frases vagas?

### 3. Verificar Fontes
- ✅ Citou fontes confiáveis?
- ✅ Incluiu URLs entre parênteses?
- ✅ Dados são verificáveis?

---

## 🚀 Benefícios

### Para o SEO
- ✅ Conteúdo otimizado para Google
- ✅ Estrutura E-E-A-T forte
- ✅ YMYL compliance

### Para o Usuário
- ✅ Informações completas e verificáveis
- ✅ Leitura dinâmica e profissional
- ✅ Confiável e ético

### Para o Negócio
- ✅ Conformidade legal (Lei 14.790/23)
- ✅ Reputação e autoridade
- ✅ Performance em buscadores

---

## 📖 Comandos Sugeridos

O sistema está pronto para responder a comandos como:

- "Crie um artigo com os palpites para o jogo entre Flamengo x Palmeiras em 15/11/2025"
- "Escreva um comparativo entre bet365 e Superbet focando em bônus"
- "Qual a nova regulamentação aprovada para apostas no Brasil?"
- "Monte uma meta title e meta description para 'Melhores slots de cassino Novembro 2025'"
- "Crie um guia para iniciantes em apostas esportivas no Brasil"
- "Monte um ranking com as melhores casas de apostas licenciadas no Brasil em 2025"

---

## ⚡ Manutenção

### Para Atualizar Instruções:

1. Edite: `redator_app/config/instrucoes_globais.py`
2. Modifique a constante `INSTRUCOES_GLOBAIS`
3. Commit e push para GitHub
4. Aguarde rebuild do Streamlit Cloud (~2-3 min)

**IMPORTANTE**: Mudanças nas instruções globais afetam **TODOS** os agentes automaticamente.

---

## 🎯 Resumo Executivo

✅ **Instruções centralizadas** em um único arquivo  
✅ **Aplicadas automaticamente** a todos os agentes  
✅ **Nunca esquecidas** pelo sistema  
✅ **Garantem qualidade**, legalidade e SEO  
✅ **Fácil manutenção** e atualização  

---

**Sistema atualizado em:** Novembro 2025  
**Versão:** 2.0 - Instruções Globais Integradas

