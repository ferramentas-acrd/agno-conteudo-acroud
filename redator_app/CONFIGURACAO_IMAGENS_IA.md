# 🎨 Configuração de Geração de Imagens com IA

Guia completo para configurar APIs de geração de imagens (DALL-E 3, Replicate/Flux)

## 📊 Comparação de APIs

| API | Qualidade | Velocidade | Custo | Melhor Para |
|-----|-----------|-----------|-------|-------------|
| **DALL-E 3** ⭐ | Excelente | Média (15-30s) | $0.04-0.08/img | Qualidade máxima |
| **Replicate (Flux)** | Muito Boa | Rápida (5-10s) | $0.003/img ou GRÁTIS | Melhor custo-benefício |
| **Fallback (Texto)** | Boa | Instantânea | Grátis | Sempre funciona |

---

## 🥇 OPÇÃO 1: DALL-E 3 (Recomendado)

### ✨ Por que DALL-E 3?

- 🎯 **Melhor qualidade** do mercado
- 🇧🇷 **Entende português** perfeitamente
- 🎨 **Estilos variados** (realista, artístico, etc)
- 🔒 **API oficial** da OpenAI
- ⚡ **Fácil configuração**

### 📝 Passo a Passo

#### 1️⃣ Criar Conta na OpenAI

1. Acesse: https://platform.openai.com/signup
2. Crie sua conta (pode usar Google)
3. Verifique seu email

#### 2️⃣ Adicionar Créditos

1. Acesse: https://platform.openai.com/account/billing
2. Clique em **"Add payment method"**
3. Adicione cartão de crédito
4. **Importante:** Defina um limite de gastos
   - Settings > Billing > Usage limits
   - Recomendo: $5-10/mês para começar

#### 3️⃣ Criar API Key

1. Acesse: https://platform.openai.com/api-keys
2. Clique em **"+ Create new secret key"**
3. Dê um nome: "Redator Automático"
4. Copie a chave (começa com `sk-proj-...`)
5. **⚠️ IMPORTANTE:** Salve agora! Não poderá ver novamente

#### 4️⃣ Configurar no Projeto

Adicione ao arquivo `.env`:

```bash
# OpenAI API (DALL-E 3)
OPENAI_API_KEY=sk-proj-sua_chave_aqui
```

### 💰 Custos DALL-E 3

| Tamanho | Qualidade | Preço |
|---------|-----------|-------|
| 1024×1024 | Standard | $0.040 |
| 1024×1024 | HD | $0.080 |
| 1792×1024 | Standard | $0.080 |
| 1792×1024 | HD | $0.120 |

**Nossa aplicação usa:** 1792×1024 Standard = **$0.08 por imagem**

**Exemplo de uso:**
- 100 imagens/mês = $8
- 50 imagens/mês = $4
- 10 imagens/mês = $0.80

### ⚙️ Configurações Disponíveis

No código (`gerador_imagem.py`), você pode ajustar:

```python
payload = {
    "model": "dall-e-3",
    "size": "1792x1024",  # ou "1024x1024" (mais barato)
    "quality": "standard",  # ou "hd" (melhor qualidade, 2x mais caro)
    "style": "natural"  # ou "vivid" (cores mais vivas)
}
```

---

## 🥈 OPÇÃO 2: Replicate (Flux) - Custo-Benefício

### ✨ Por que Replicate?

- 💰 **Muito mais barato** (~$0.003/img)
- 🆓 **Flux Schnell GRATUITO!**
- ⚡ **Muito rápido** (5-10s)
- 🎨 **Qualidade excelente**
- 🔄 **Vários modelos** disponíveis

### 📝 Passo a Passo

#### 1️⃣ Criar Conta no Replicate

1. Acesse: https://replicate.com/signin
2. Clique em **"Sign in with GitHub"** (recomendado)
3. Ou use email/senha

#### 2️⃣ Obter API Token

1. Acesse: https://replicate.com/account/api-tokens
2. Clique em **"+ New token"**
3. Dê um nome: "Redator App"
4. Copie o token (começa com `r8_...`)

#### 3️⃣ Adicionar Créditos (Opcional)

**Flux Schnell é GRÁTIS!** Mas se quiser modelos premium:

1. Acesse: https://replicate.com/account/billing
2. Adicione créditos ($10 rende ~3000 imagens!)

#### 4️⃣ Configurar no Projeto

Adicione ao arquivo `.env`:

```bash
# Replicate API (Flux)
REPLICATE_API_TOKEN=r8_sua_chave_aqui
```

### 💰 Custos Replicate

| Modelo | Velocidade | Custo | Qualidade |
|--------|-----------|-------|-----------|
| **Flux Schnell** ⭐ | 5s | **GRÁTIS** | Excelente |
| Flux Pro | 10s | $0.055 | Melhor |
| SDXL | 15s | $0.003 | Muito Boa |

**Nossa aplicação usa:** Flux Schnell = **GRATUITO!** 🎉

### 🎨 Modelos Disponíveis

Para trocar de modelo, edite `gerador_imagem.py`:

**Flux Schnell (Atual - GRÁTIS):**
```python
"version": "f2ab8a5569479b796f8986afbd7f96745c4d0c81be6d7dddeb8f71a34e5f3e3c"
```

**Flux Pro (Melhor Qualidade):**
```python
"version": "d...", # Ver: https://replicate.com/black-forest-labs/flux-pro
```

**SDXL (Stable Diffusion):**
```python
"version": "7...", # Ver: https://replicate.com/stability-ai/sdxl
```

---

## 🎯 Qual Escolher?

### Use DALL-E 3 se:
- ✅ Quer a **melhor qualidade** possível
- ✅ Precisa de **imagens realistas**
- ✅ Está disposto a pagar ~$0.08/imagem
- ✅ Quer **suporte oficial** OpenAI

### Use Replicate (Flux) se:
- ✅ Quer **economia** (~97% mais barato ou grátis!)
- ✅ Precisa gerar **muitas imagens**
- ✅ Quer **velocidade** (5s vs 20s)
- ✅ Qualidade "muito boa" é suficiente

### Use ambas (Configuração Atual):
1. **DALL-E 3** como principal
2. **Replicate** como backup
3. **Texto estilizado** como fallback

A aplicação tenta nesta ordem automaticamente! 🎉

---

## 📦 Instalação de Dependências

Não precisa instalar nada extra! Já usamos:
- ✅ `requests` (HTTP)
- ✅ `Pillow` (processamento de imagem)
- ✅ `dotenv` (variáveis de ambiente)

---

## 🧪 Testando a Configuração

### Teste 1: Verificar APIs Configuradas

Execute na aplicação Streamlit:
- Sidebar mostrará status das APIs
- ✅ Verde = Configurada
- ❌ Vermelho = Faltando

### Teste 2: Gerar Imagem de Teste

```python
from agents.gerador_imagem import GeradorImagem

gerador = GeradorImagem()
imagem_path = gerador.gerar_imagem(
    titulo="Python para Iniciantes",
    descricao="Tutorial completo de Python"
)
print(f"Imagem gerada: {imagem_path}")
```

### Teste 3: Ver Logs

Ao gerar imagem, você verá:
```
🎨 Gerando imagem para: Python para Iniciantes
→ Usando DALL-E 3 (OpenAI)...
✅ Imagem salva em: imagens_geradas/Python_para_Iniciantes_20250112_143022.png
```

---

## 🔧 Configuração do .env Completo

```bash
# ===============================================
# CONFIGURAÇÃO - REDATOR AUTOMÁTICO COM IA
# ===============================================

# APIs de IA e Pesquisa (OBRIGATÓRIAS)
GROQ_API_KEY=gsk_sua_chave_groq
TAVILY_API_KEY=tvly-sua_chave_tavily

# Google APIs (OBRIGATÓRIAS para Google Docs)
GOOGLE_APPLICATION_CREDENTIALS=redator_app/config/credentials.json

# ===============================================
# GERAÇÃO DE IMAGENS (ESCOLHA UMA OU AMBAS)
# ===============================================

# OPÇÃO 1: OpenAI DALL-E 3 (Melhor Qualidade)
# Custo: ~$0.08 por imagem
# https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-sua_chave_openai

# OPÇÃO 2: Replicate Flux (Grátis ou $0.003/img)
# Flux Schnell é GRATUITO!
# https://replicate.com/account/api-tokens
REPLICATE_API_TOKEN=r8_sua_chave_replicate

# ===============================================
# Se nenhuma API estiver configurada,
# a aplicação usará gerador de texto estilizado (sempre funciona!)
# ===============================================
```

---

## 🐛 Solução de Problemas

### Erro: "OpenAI API key not found"
**Solução:** Verifique se a chave no `.env` começa com `sk-proj-` ou `sk-`

### Erro: "Insufficient quota" (OpenAI)
**Solução:** 
1. Acesse: https://platform.openai.com/account/billing
2. Adicione créditos
3. Verifique se o cartão está ativo

### Erro: "Invalid authentication" (Replicate)
**Solução:** Verifique se o token começa com `r8_`

### Imagem demora muito
**DALL-E:** Normal, 15-30s
**Replicate:** 5-10s normal, >30s indica problema

### Qualidade baixa
**Solução:** 
- DALL-E: Mude `quality` para `"hd"`
- Replicate: Troque para Flux Pro
- Ajuste os prompts em `gerador_imagem.py`

---

## 💡 Dicas de Otimização

### 1. Economizar com DALL-E
```python
# Usar tamanho menor
"size": "1024x1024"  # $0.04 vs $0.08
```

### 2. Melhorar Qualidade Replicate
```python
# Aumentar steps (mais lento mas melhor)
"num_inference_steps": 8  # padrão: 4
```

### 3. Cache de Imagens
A aplicação já salva localmente! Reutilize imagens quando possível.

### 4. Batch Processing
Para múltiplos artigos, gere imagens em lote:
```python
for titulo in titulos:
    gerador.gerar_imagem(titulo)
```

---

## 📊 Monitoramento de Custos

### OpenAI
- Dashboard: https://platform.openai.com/usage
- Veja gastos em tempo real
- Configure alertas de limite

### Replicate
- Dashboard: https://replicate.com/account/billing
- Créditos restantes
- Histórico de uso

---

## 🎓 Recursos Adicionais

### Documentação Oficial
- **OpenAI DALL-E 3:** https://platform.openai.com/docs/guides/images
- **Replicate:** https://replicate.com/docs
- **Flux:** https://replicate.com/black-forest-labs/flux-schnell

### Exemplos de Prompts
- https://prompthero.com/dall-e-3-prompts
- https://replicate.com/explore

### Comunidades
- **OpenAI Discord:** https://discord.gg/openai
- **Replicate Discord:** https://discord.gg/replicate

---

## ✅ Checklist de Configuração

- [ ] Criar conta OpenAI ou Replicate
- [ ] Obter API key
- [ ] Adicionar créditos (se necessário)
- [ ] Configurar no `.env`
- [ ] Testar geração de imagem
- [ ] Verificar custos no dashboard
- [ ] Ajustar configurações se necessário

---

**Pronto! Agora você tem geração de imagens profissionais com IA! 🎨🚀**

Recomendação: **Comece com Replicate (Flux Schnell) pois é GRÁTIS!**  
Se precisar de qualidade máxima, ative DALL-E 3.

