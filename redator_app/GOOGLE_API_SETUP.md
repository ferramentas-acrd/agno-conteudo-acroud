# 📝 Configuração das APIs do Google

Este guia mostra como configurar as APIs do Google Drive e Google Docs para usar na aplicação de redação automática.

## 🚀 Passo a Passo

### 1️⃣ Criar Projeto no Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Clique em **"Select a project"** (topo da página)
3. Clique em **"NEW PROJECT"**
4. Dê um nome ao projeto (ex: "Redator Automático")
5. Clique em **"CREATE"**

### 2️⃣ Ativar as APIs Necessárias

#### Google Docs API

1. No menu lateral, vá em **"APIs & Services" > "Library"**
2. Procure por **"Google Docs API"**
3. Clique nela e depois em **"ENABLE"**

#### Google Drive API

1. Na mesma tela de Library
2. Procure por **"Google Drive API"**
3. Clique nela e depois em **"ENABLE"**

### 3️⃣ Criar Credenciais OAuth 2.0

1. No menu lateral, vá em **"APIs & Services" > "Credentials"**
2. Clique em **"+ CREATE CREDENTIALS"** (topo da página)
3. Selecione **"OAuth client ID"**

#### Configurar Tela de Consentimento (se solicitado)

Se for a primeira vez, você precisará configurar:

1. Clique em **"CONFIGURE CONSENT SCREEN"**
2. Escolha **"External"** e clique em **"CREATE"**
3. Preencha os campos obrigatórios:
   - **App name**: Redator Automático
   - **User support email**: seu email
   - **Developer contact email**: seu email
4. Clique em **"SAVE AND CONTINUE"**
5. Em "Scopes", clique em **"ADD OR REMOVE SCOPES"**
6. Procure e adicione:
   - `https://www.googleapis.com/auth/documents`
   - `https://www.googleapis.com/auth/drive.file`
7. Clique em **"UPDATE"** e depois **"SAVE AND CONTINUE"**
8. Em "Test users", clique em **"+ ADD USERS"**
9. Adicione seu email do Google
10. Clique em **"SAVE AND CONTINUE"**
11. Revise e clique em **"BACK TO DASHBOARD"**

#### Criar o OAuth Client ID

1. Volte para **"Credentials"**
2. Clique em **"+ CREATE CREDENTIALS" > "OAuth client ID"**
3. Em "Application type", selecione **"Desktop app"**
4. Dê um nome (ex: "Redator Desktop Client")
5. Clique em **"CREATE"**
6. Uma janela aparecerá com Client ID e Client Secret
7. Clique em **"DOWNLOAD JSON"**
8. Salve o arquivo como `credentials.json`

### 4️⃣ Configurar na Aplicação

1. Crie uma pasta `config` no diretório `redator_app`:
   ```bash
   mkdir -p redator_app/config
   ```

2. Mova o arquivo `credentials.json` para `redator_app/config/`:
   ```bash
   mv ~/Downloads/credentials.json redator_app/config/
   ```

3. Adicione ao seu arquivo `.env`:
   ```bash
   GOOGLE_APPLICATION_CREDENTIALS=redator_app/config/credentials.json
   ```

### 5️⃣ Primeira Autenticação

Na primeira vez que você rodar a aplicação:

1. Um navegador abrirá automaticamente
2. Faça login com sua conta Google
3. Clique em **"Continue"** para permitir acesso
4. Um arquivo `token.json` será criado automaticamente
5. Das próximas vezes, não precisará autenticar novamente!

---

## 🔧 Outras APIs Necessárias

### Groq API (já configurada)

✅ Você já tem configurada no `.env`:
```bash
GROQ_API_KEY=gsk_...
```

### Tavily API (já configurada)

✅ Você já tem configurada no `.env`:
```bash
TAVILY_API_KEY=tvly-...
```

### RapidAPI (Opcional - para geração de imagens com IA)

#### O que é?
RapidAPI é um marketplace de APIs. Você pode usar para acessar APIs de geração de imagens como DALL-E, Stable Diffusion, etc.

#### Como Configurar:

1. **Criar Conta**
   - Acesse: https://rapidapi.com/
   - Clique em **"Sign Up"**
   - Crie sua conta (gratuita)

2. **Escolher API de Imagens**
   
   Opções recomendadas:
   
   **Opção 1: AI Image Generator** (Mais simples)
   - Procure por: "AI Image Generator"
   - URL: https://rapidapi.com/ai-image-generator/api/ai-image-generator3
   - Plano Free: 50 requisições/mês
   
   **Opção 2: Stable Diffusion**
   - Procure por: "Stable Diffusion"
   - Vários provedores disponíveis
   - Verifique planos gratuitos

3. **Obter API Key**
   - Na página da API escolhida, clique em **"Subscribe to Test"**
   - Escolha o plano **"Basic"** (geralmente gratuito)
   - Clique em **"Subscribe"**
   - Vá para a aba **"Endpoints"**
   - No código de exemplo, você verá:
     ```javascript
     'X-RapidAPI-Key': 'SUA_CHAVE_AQUI'
     'X-RapidAPI-Host': 'nome-do-host.p.rapidapi.com'
     ```

4. **Adicionar ao `.env`**
   ```bash
   RAPIDAPI_KEY=sua_chave_aqui
   RAPIDAPI_HOST=nome-do-host.p.rapidapi.com
   ```

#### Importante sobre Imagens

**Sem RapidAPI:**
- A aplicação ainda funciona!
- Ela cria imagens com texto estilizado (bonitas e profissionais)
- Tamanho perfeito para redes sociais (1200x630px)

**Com RapidAPI:**
- Gera imagens com IA super realistas
- Mais profissional para artigos
- Custo: geralmente 50-100 imagens grátis/mês

---

## 📋 Checklist Final

Certifique-se de ter configurado:

- [ ] ✅ GROQ_API_KEY (já tem)
- [ ] ✅ TAVILY_API_KEY (já tem)
- [ ] ✅ Google Docs API ativada
- [ ] ✅ Google Drive API ativada
- [ ] ✅ arquivo `credentials.json` em `config/`
- [ ] ✅ GOOGLE_APPLICATION_CREDENTIALS no `.env`
- [ ] ⬜ RAPIDAPI_KEY (opcional)
- [ ] ⬜ RAPIDAPI_HOST (opcional)

---

## 🐛 Solução de Problemas

### Erro: "credentials.json not found"
**Solução:** Verifique se o arquivo está em `redator_app/config/credentials.json`

### Erro: "Access denied" ou "Insufficient permissions"
**Solução:** 
1. Delete o arquivo `config/token.json`
2. Execute a aplicação novamente
3. Refaça a autenticação

### Erro: "API not enabled"
**Solução:** Certifique-se de ter ativado as APIs no Google Cloud Console

### Navegador não abre na autenticação
**Solução:** 
1. Copie a URL que aparece no terminal
2. Cole em um navegador manualmente
3. Complete a autenticação

---

## 💡 Dicas

### Segurança
- **NUNCA** compartilhe seu arquivo `credentials.json`
- **NUNCA** commite `credentials.json` ou `token.json` no Git
- Adicione ao `.gitignore`:
  ```
  config/credentials.json
  config/token.json
  .env
  ```

### Custos
- **Google Docs/Drive API**: Totalmente GRATUITO para uso normal
- **Groq API**: Plano gratuito generoso
- **Tavily API**: Plano free disponível
- **RapidAPI**: Planos free para começar

### Limites
- Google Docs API: 300 requisições/minuto (mais que suficiente!)
- Google Drive API: 1000 requisições/100 segundos

---

## 📞 Precisa de Ajuda?

Se tiver problemas:
1. Verifique os logs da aplicação
2. Confirme que todas as APIs estão ativadas
3. Tente deletar `token.json` e autenticar novamente
4. Verifique se seu email está na lista de "Test users"

---

Pronto! Agora você está pronto para usar a aplicação de redação automática! 🎉

