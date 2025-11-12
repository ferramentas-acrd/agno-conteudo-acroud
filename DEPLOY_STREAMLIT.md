# 🚀 Deploy no Streamlit Cloud - Guia Completo

Deploy sua aplicação em 10 minutos e deixe ela online 24/7 **GRATUITAMENTE**!

---

## 🌟 Por que Streamlit Cloud?

- ✅ **100% Gratuito** para apps públicos
- ✅ **Deploy automático** a cada push no GitHub
- ✅ **SSL/HTTPS** grátis
- ✅ **Escalável** automaticamente
- ✅ **Logs** em tempo real
- ✅ **Secrets** seguros para API keys
- ✅ **Custom domain** (opcional)

---

## 📋 Pré-requisitos

- [x] Código no GitHub ✅ (já temos!)
- [x] Conta no GitHub ✅
- [ ] Conta no Streamlit Cloud (vamos criar!)
- [ ] API Keys (Groq, Tavily)

---

## 🚀 Passo a Passo Completo

### **PASSO 1: Criar Conta no Streamlit Cloud**

1. Acesse: **https://share.streamlit.io**
2. Clique em **"Sign up"**
3. Escolha **"Continue with GitHub"**
4. Autorize o Streamlit a acessar sua conta GitHub
5. ✅ Conta criada!

---

### **PASSO 2: Preparar Repositório (Já feito!)**

O repositório já está pronto com:
- ✅ `requirements.txt` (dependências)
- ✅ Código organizado
- ✅ `.gitignore` configurado

---

### **PASSO 3: Criar Novo App no Streamlit**

1. No dashboard do Streamlit Cloud, clique **"New app"**

2. Preencha os campos:
   ```
   Repository: ferramentas-acrd/agno-conteudo-acroud
   Branch: main
   Main file path: redator_app/app.py
   ```

3. Clique em **"Advanced settings..."**

4. **Python version:** 3.11

5. **NÃO clique em "Deploy" ainda!** Vamos configurar os Secrets primeiro.

---

### **PASSO 4: Configurar Secrets (API Keys)**

🔒 **IMPORTANTE:** Nunca coloque API keys no código!

#### 4.1 - No Streamlit Cloud:

1. Antes de fazer deploy, clique em **"Advanced settings"**
2. Encontre a seção **"Secrets"**
3. Cole o conteúdo abaixo (substitua pelos seus valores reais):

```toml
# === OBRIGATÓRIAS ===
GROQ_API_KEY = "gsk_seu_groq_api_key_aqui"
TAVILY_API_KEY = "tvly_seu_tavily_api_key_aqui"

# === OPCIONAIS (descomente se tiver) ===
# SUPABASE_URL = "https://seu-projeto.supabase.co"
# SUPABASE_KEY = "sua_chave_supabase_aqui"
# OPENAI_API_KEY = "sk-seu_openai_key_aqui"
# REPLICATE_API_TOKEN = "r8_seu_replicate_token_aqui"
```

**⚠️ IMPORTANTE:**
- Use o formato TOML (com aspas)
- Uma variável por linha
- Substitua pelos seus valores reais

#### 4.2 - Onde Pegar as API Keys:

**GROQ_API_KEY:**
- https://console.groq.com/keys
- Copie sua chave existente ou crie uma nova

**TAVILY_API_KEY:**
- https://tavily.com
- Dashboard → API Key

**SUPABASE (opcional):**
- https://supabase.com
- Seu projeto → Settings → API
- Copie URL e anon/public key

**OPENAI (opcional):**
- https://platform.openai.com/api-keys

**REPLICATE (opcional):**
- https://replicate.com/account/api-tokens

---

### **PASSO 5: Deploy! 🚀**

1. Após configurar os Secrets, clique **"Deploy!"**
2. Aguarde 2-3 minutos enquanto o Streamlit:
   - Clona o repositório
   - Instala dependências
   - Inicia a aplicação
3. ✅ App online!

**URL gerada:**
```
https://agno-conteudo-acroud.streamlit.app
```

Ou similar (o Streamlit gera automaticamente)

---

## 🔧 Configurações Adicionais

### **Arquivo de Configuração (Opcional)**

Crie `.streamlit/config.toml` no repositório para customizar:

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

### **Adicionar Custom Domain (Opcional)**

1. Settings → General
2. Custom subdomain: `seu-nome.streamlit.app`
3. Ou configure seu próprio domínio (DNS CNAME)

---

## 📊 Monitoramento

### **Ver Logs em Tempo Real:**

1. Dashboard → Seu app
2. Menu "⋮" → **Logs**
3. Veja todos os prints e erros

### **Métricas:**

- Dashboard → Analytics
- Visitantes únicos
- Tempo de uso
- Região dos usuários

---

## 🔄 Atualizações Automáticas

### **Como funciona:**

```
1. Você faz alterações localmente
2. git add . && git commit -m "Update"
3. git push
4. Streamlit Cloud detecta automaticamente
5. Faz rebuild e redeploy
6. ✅ App atualizado em 2-3 minutos!
```

### **Forçar Rebuild:**

- Dashboard → App → Menu "⋮" → **Reboot**

---

## 🐛 Solução de Problemas

### **Erro: ModuleNotFoundError**

**Causa:** Dependência faltando em `requirements.txt`

**Solução:**
```bash
# No seu computador
cd /Users/caiobessa/Desktop/Agno\ Acroud
uv pip freeze > redator_app/requirements.txt
git add redator_app/requirements.txt
git commit -m "Update requirements"
git push
```

### **Erro: API Key não encontrada**

**Causa:** Secrets não configurados

**Solução:**
1. Dashboard → App → Settings → Secrets
2. Adicione ou corrija as API keys
3. Clique **"Save"**
4. App reinicia automaticamente

### **Erro: File not found**

**Causa:** Caminho do arquivo errado

**Solução:**
1. Dashboard → App → Settings
2. Main file path: `redator_app/app.py`
3. Save

### **App muito lento**

**Causa:** Cold start (app inativo por 7 dias)

**Solução:**
- Primeira visita pode demorar ~30s
- Após isso, fica rápido
- Plano pago mantém sempre ativo

### **Erro: Memory limit exceeded**

**Causa:** App usando muita RAM (limite free: 1GB)

**Solução:**
- Otimize código
- Use cache (`@st.cache_data`)
- Ou upgrade para plano pago

---

## 💰 Planos e Limites

### **Plano Free (Gratuito):**

| Recurso | Limite |
|---------|--------|
| Apps públicos | Ilimitado |
| Apps privados | 1 |
| CPU | Shared |
| RAM | 1 GB |
| Storage | 1 GB |
| Uptime | ~7 dias inativo = sleep |

### **Plano Paid ($20/mês):**

- Apps privados ilimitados
- 2 GB RAM
- 10 GB Storage
- Always-on (sem sleep)
- Prioridade no suporte

**Para maioria dos casos, o FREE é suficiente!**

---

## 🔐 Segurança

### **✅ Boas Práticas:**

1. **Nunca** commite API keys no código
2. Use **Secrets** para credenciais
3. Ative **autenticação** (apps privados)
4. Configure **allowlist** de IPs (opcional)
5. Use **HTTPS** (automático)

### **Tornar App Privado:**

1. Settings → Sharing
2. **Private** (requer plano pago)
3. Adicione emails de usuários permitidos

---

## 📱 Compartilhar App

### **URL Pública:**

```
https://seu-app.streamlit.app
```

### **Embed no Site:**

```html
<iframe 
  src="https://seu-app.streamlit.app/?embed=true" 
  height="800" 
  width="100%"
  frameborder="0"
></iframe>
```

### **Compartilhar Social:**

O Streamlit gera automaticamente:
- Preview image
- Meta tags
- Open Graph tags

---

## 🎨 Personalização

### **Adicionar Logo:**

No código (`app.py`):

```python
st.set_page_config(
    page_title="ACROUD - Redator IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### **Analytics:**

Adicione Google Analytics em `.streamlit/config.toml`:

```toml
[browser]
gatherUsageStats = true
```

---

## 📈 Otimização de Performance

### **1. Use Cache:**

```python
@st.cache_data(ttl=3600)
def carregar_dados():
    return dados

@st.cache_resource
def inicializar_modelo():
    return modelo
```

### **2. Lazy Loading:**

```python
# Carregue apenas quando necessário
if st.button("Gerar Conteúdo"):
    # Carrega modelo aqui
    pass
```

### **3. Minimize Reruns:**

```python
# Use session_state para persistir dados
if 'dados' not in st.session_state:
    st.session_state.dados = carregar_dados()
```

---

## ✅ Checklist de Deploy

**Antes do Deploy:**
- [ ] Código testado localmente
- [ ] `requirements.txt` atualizado
- [ ] `.gitignore` protegendo `.env`
- [ ] Push para GitHub

**Durante Deploy:**
- [ ] Conta criada no Streamlit Cloud
- [ ] Repositório conectado
- [ ] Secrets configurados (API keys)
- [ ] Deploy iniciado

**Após Deploy:**
- [ ] App carregou com sucesso
- [ ] Testar todas as funcionalidades
- [ ] Verificar logs (sem erros)
- [ ] Compartilhar URL

---

## 🆘 Suporte

### **Documentação Oficial:**
- https://docs.streamlit.io/streamlit-community-cloud

### **Community Forum:**
- https://discuss.streamlit.io

### **GitHub Issues:**
- https://github.com/streamlit/streamlit/issues

### **Status Page:**
- https://streamlit.statuspage.io

---

## 🎯 Resumo - 5 Minutos

```bash
1. ✅ Código no GitHub (já temos!)
2. 🌐 Acessar: https://share.streamlit.io
3. 🔐 Login com GitHub
4. ➕ New app → Selecionar repositório
5. 🔑 Configurar Secrets (API keys)
6. 🚀 Deploy!
7. ⏰ Aguardar 2-3 min
8. 🎉 App online!
```

**URL:** `https://seu-app.streamlit.app`

---

## 🎊 Pronto!

Sua aplicação estará online, acessível de qualquer lugar do mundo, com:

✅ HTTPS automático  
✅ Deploy contínuo  
✅ Logs em tempo real  
✅ Secrets seguros  
✅ 100% GRATUITO  

**Tempo total:** ~10 minutos  
**Custo:** $0  
**Resultado:** App profissional online! 🚀

---

**Dúvidas?** Veja os logs ou abra uma issue!

**Boa sorte com o deploy! 🎉**

