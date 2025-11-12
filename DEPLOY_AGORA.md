# 🚀 DEPLOY AGORA - 5 Minutos

## ⚠️ ERRO QUE VOCÊ VIU

O botão **"Deploy"** da aplicação **local** (localhost) **NÃO funciona** para deploy em produção!

---

## ✅ PROCESSO CORRETO

### **PASSO 1: Abra o Streamlit Cloud**

🔗 **Clique aqui:** https://share.streamlit.io

---

### **PASSO 2: Login com GitHub**

1. Clique **"Sign in"** (ou "Sign up" se for primeira vez)
2. Clique **"Continue with GitHub"**
3. Autorize o Streamlit
4. ✅ Login feito!

---

### **PASSO 3: Criar Novo App**

1. Dashboard → Botão **"New app"** (canto superior direito)

2. Preencha EXATAMENTE assim:

```
Repository: ferramentas-acrd/agno-conteudo-acroud
Branch: main
Main file path: redator_app/app.py
```

3. **IMPORTANTE:** Clique em **"Advanced settings"** ⚙️

---

### **PASSO 4: Advanced Settings**

#### **Python version:**
```
3.11
```

#### **Secrets (COPIE E COLE ISSO):**

```toml
GROQ_API_KEY = "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"
TAVILY_API_KEY = "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"
```

⚠️ **Se tiver outras API keys (OpenAI, Replicate), adicione também:**

```toml
# Descomentar e adicionar se tiver:
# OPENAI_API_KEY = "sk-..."
# REPLICATE_API_TOKEN = "r8_..."
```

---

### **PASSO 5: Deploy! 🚀**

1. Clique no botão azul **"Deploy!"**
2. Aguarde 2-3 minutos
3. Veja os logs carregando
4. ✅ **App online!**

---

## 🎉 Pronto!

Sua URL será algo como:

```
https://agno-acroud.streamlit.app
```

ou

```
https://agno-conteudo-acroud.streamlit.app
```

---

## 🐛 Se der erro:

### **Erro: "Repository is private"**

1. Vá em: https://github.com/ferramentas-acrd/agno-conteudo-acroud/settings
2. Scroll até **Danger Zone**
3. **"Change repository visibility"** → **Public**
4. Confirme
5. Volte ao Streamlit Cloud e tente novamente

### **Erro: "Module not found"**

Os módulos já estão atualizados! Se der erro, me avise o nome do módulo faltando.

### **Erro: "API key not found"**

1. No Streamlit Cloud
2. Seu app → **Settings** → **Secrets**
3. Cole novamente as API keys
4. **Save**
5. Reboot app

---

## 📱 Compartilhar

Depois do deploy, compartilhe:

```
https://seu-app.streamlit.app
```

---

## 🎯 Resumo - 1 Minuto

```
1. https://share.streamlit.io
2. Login com GitHub
3. New app
4. Repository: ferramentas-acrd/agno-conteudo-acroud
5. Main file: redator_app/app.py
6. Advanced → Secrets → Cole API keys
7. Deploy!
8. Aguarde 2-3 min
9. ✅ App online!
```

---

**Tempo:** 5 minutos  
**Custo:** $0 (gratuito!)  
**Resultado:** App profissional online 24/7! 🎊

---

**Está com dúvida?** Me avise que te ajudo!

