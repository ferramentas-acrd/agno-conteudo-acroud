# 🔑 Corrigir Erro de API Key da OpenAI

## ⚠️ ERRO DETECTADO

```
Erro ao gerar conteúdo: Incorrect API key provided: sk-proj-***...***ZdsA
```

---

## 🎯 SOLUÇÃO RÁPIDA

### **1️⃣ Verificar a Chave da OpenAI**

1. Acesse: https://platform.openai.com/api-keys
2. Faça login na sua conta OpenAI
3. **Crie uma NOVA chave** ou copie uma existente
4. A chave deve começar com: `sk-proj-` ou `sk-`

---

### **2️⃣ Atualizar no Streamlit Cloud**

#### **Passo 1: Acessar Settings**
1. Vá para: https://share.streamlit.io
2. Encontre seu app: **conteudo-automacao**
3. Clique no menu **⋮** (três pontinhos)
4. Clique em **Settings**
5. No menu lateral, clique em **Secrets**

#### **Passo 2: Atualizar a Chave**

**Formato CORRETO (TOML):**

```toml
# === OBRIGATÓRIAS ===
OPENAI_API_KEY = "sk-proj-SUA_CHAVE_COMPLETA_AQUI"
TAVILY_API_KEY = "tvly-SUA_CHAVE_AQUI"

# === OPCIONAIS (Supabase) ===
SUPABASE_URL = "https://oykubgmipbeqdcsgqfnz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im95a3ViZ21pcGJlcWRjc2dxZm56Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI5NDg4ODksImV4cCI6MjA3ODUyNDg4OX0.goO0SOdOUp3_RZ85QviNqdEVNIX98H5BcgxJHH9DEgk"

# === OPCIONAL (Replicate - Geração de Imagens) ===
# REPLICATE_API_TOKEN = "r8_SUA_CHAVE_AQUI"
```

**⚠️ IMPORTANTE:**
- Espaços ao redor do `=`
- Aspas duplas `"` ao redor dos valores
- Uma chave por linha
- Não usar vírgulas no final

---

### **3️⃣ Salvar e Aguardar**

1. Clique em **"Save"**
2. O app vai **reiniciar automaticamente** (1-2 minutos)
3. Aguarde o rebuild completar

---

## 🔍 VERIFICAR SE FUNCIONOU

Após 2-3 minutos:

1. Recarregue: https://conteudo-automacao.streamlit.app
2. Olhe na sidebar, seção **"Status das APIs"**
3. Deve mostrar: **✅ OPENAI_API_KEY**
4. Tente gerar um conteúdo novamente

---

## 🚨 SE O ERRO PERSISTIR

### **Problema 1: Chave Inválida**

**Sintomas:**
- Erro: "Incorrect API key"
- Status: ❌ OPENAI_API_KEY

**Solução:**
1. Acesse: https://platform.openai.com/api-keys
2. **DELETE** a chave antiga
3. **CRIE** uma nova chave
4. Copie a chave COMPLETA (começa com `sk-proj-` ou `sk-`)
5. Cole no Streamlit Cloud Secrets
6. Save e aguarde rebuild

---

### **Problema 2: Sem Créditos na OpenAI**

**Sintomas:**
- Erro: "You exceeded your current quota"
- API key válida, mas sem saldo

**Solução:**
1. Acesse: https://platform.openai.com/account/billing
2. Adicione créditos (cartão de crédito)
3. Aguarde 5-10 minutos
4. Tente novamente

**Custos:**
- GPT-4 Turbo: ~$0.01 por artigo
- DALL-E 3: ~$0.08 por imagem
- Total: ~$0.09 por conteúdo completo

---

### **Problema 3: Formato Incorreto no Secrets**

**Errado:**
```toml
OPENAI_API_KEY=sk-proj-abc123  ❌ Sem aspas
OPENAI_API_KEY:"sk-proj-abc123" ❌ Dois pontos em vez de =
OPENAI_API_KEY = 'sk-proj-abc123' ❌ Aspas simples
```

**Correto:**
```toml
OPENAI_API_KEY = "sk-proj-abc123" ✅
```

---

## 📞 SUPORTE OPENAI

Se continuar com problemas:

1. **Dashboard:** https://platform.openai.com/
2. **API Keys:** https://platform.openai.com/api-keys
3. **Billing:** https://platform.openai.com/account/billing
4. **Usage:** https://platform.openai.com/usage
5. **Help:** https://help.openai.com/

---

## 🎁 ALTERNATIVA: Usar Replicate (GRATUITO)

Se não quiser usar DALL-E 3 para imagens:

1. Crie conta em: https://replicate.com/
2. Copie sua API key
3. Adicione ao Streamlit Secrets:

```toml
REPLICATE_API_TOKEN = "r8_SUA_CHAVE_AQUI"
```

**Vantagens:**
- Flux Schnell é **GRATUITO**
- Boa qualidade de imagens
- Mais barato que DALL-E 3

**Desvantagens:**
- Geração um pouco mais lenta
- Menos controle sobre detalhes

---

## ✅ CHECKLIST FINAL

Antes de fechar este guia:

- [ ] Criei/copiei uma chave válida da OpenAI
- [ ] Atualizei os Secrets no Streamlit Cloud
- [ ] Usei o formato TOML correto (com aspas duplas)
- [ ] Salvei e aguardei 2-3 minutos
- [ ] Recarreguei a aplicação
- [ ] Verifiquei: ✅ OPENAI_API_KEY na sidebar
- [ ] Testei gerar um conteúdo

---

**Se tudo estiver ✅ verde, pode usar normalmente!**

**Atualizado:** Novembro 2025  
**Status:** Guia de Correção de Erros

