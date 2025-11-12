# 🔧 PASSO A PASSO - Corrigir API Key OpenAI

## 🚨 ERRO ATUAL:
```
Erro ao gerar conteúdo: Incorrect API key provided: sk-proj-***...***ZdsA
```

---

## ✅ SOLUÇÃO EM 5 MINUTOS

### **PASSO 1: Obter Nova Chave da OpenAI**

1. **Abra esta URL:** https://platform.openai.com/api-keys

2. **Faça Login** na sua conta OpenAI

3. **Clique em:** `+ Create new secret key`

4. **Nomeie:** "Streamlit-Redator-Nov2025"

5. **COPIE A CHAVE COMPLETA** (ela começa com `sk-proj-`)
   - ⚠️ **IMPORTANTE:** Essa é a ÚNICA vez que você verá ela!
   - Cole num arquivo temporário para não perder

6. **Clique em:** "Done"

**Exemplo de chave válida:**
```
sk-proj-ABCDefgh123456789XYZabcdefgh123456789XYZabcdefgh123456
```

---

### **PASSO 2: Atualizar no Streamlit Cloud**

1. **Abra esta URL:** https://share.streamlit.io

2. **Encontre seu app:** `conteudo-automacao`

3. **Clique no menu:** `⋮` (três pontinhos no canto direito)

4. **Clique em:** `Settings`

5. **No menu lateral esquerdo, clique em:** `Secrets`

6. **APAGUE TUDO** que está lá

7. **COLE EXATAMENTE ISTO:**

```toml
OPENAI_API_KEY = "COLE_SUA_CHAVE_AQUI"
TAVILY_API_KEY = "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"
SUPABASE_URL = "https://oykubgmipbeqdcsgqfnz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im95a3ViZ21pcGJlcWRjc2dxZm56Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI5NDg4ODksImV4cCI6MjA3ODUyNDg4OX0.goO0SOdOUp3_RZ85QviNqdEVNIX98H5BcgxJHH9DEgk"
```

8. **SUBSTITUA** `COLE_SUA_CHAVE_AQUI` pela chave que você copiou no Passo 1

9. **Verifique:**
   - ✅ Tem espaços ao redor do `=`
   - ✅ Tem aspas duplas `"` ao redor da chave
   - ✅ A chave começa com `sk-proj-`
   - ✅ NÃO tem vírgulas no final das linhas

**Exemplo CORRETO:**
```toml
OPENAI_API_KEY = "sk-proj-ABCDefgh123456789XYZabcdefgh123456"
```

**Exemplos ERRADOS:**
```toml
OPENAI_API_KEY="sk-proj-abc"     ❌ Sem espaços
OPENAI_API_KEY = sk-proj-abc     ❌ Sem aspas
OPENAI_API_KEY = 'sk-proj-abc'   ❌ Aspas simples
```

10. **Clique em:** `Save`

---

### **PASSO 3: Aguardar Rebuild**

1. **Aguarde 2-3 minutos** (o app vai reiniciar sozinho)

2. **Você verá uma mensagem:** "Restarting app..."

3. **NÃO feche a página**, espere completar

---

### **PASSO 4: Verificar se Funcionou**

1. **Recarregue a página:** https://conteudo-automacao.streamlit.app

2. **Clique na seta** ao lado de "Status das APIs" (sidebar)

3. **Verifique:**
   - ✅ OPENAI_API_KEY deve estar **VERDE**
   - ✅ TAVILY_API_KEY deve estar **VERDE**
   - ✅ SUPABASE_URL deve estar **VERDE**

4. **Se algum estiver VERMELHO:**
   - Volte ao Passo 2
   - Verifique o formato
   - Certifique-se de usar aspas duplas `"`
   - Certifique-se de ter espaços ao redor do `=`

---

### **PASSO 5: Testar Geração de Conteúdo**

1. **Selecione um projeto:** Tecmundo

2. **Selecione uma categoria:** Promocoes

3. **Digite uma palavra-chave:** "Promocao Tigrinho Giros Gratis"

4. **Clique em:** `🚀 Gerar Conteúdo Completo`

5. **Aguarde:** 30-60 segundos

6. **Se funcionar:**
   - ✅ Você verá o conteúdo gerado
   - ✅ Você verá uma imagem relevante ao tema
   - ✅ Problema resolvido!

7. **Se AINDA der erro:**
   - Vá para "SOLUÇÃO DE PROBLEMAS" abaixo

---

## 🆘 SOLUÇÃO DE PROBLEMAS

### Problema 1: Ainda diz "Incorrect API key"

**Causa possível:** Chave ainda não foi atualizada corretamente

**Solução:**
1. Volte para https://share.streamlit.io
2. Settings → Secrets
3. **APAGUE TUDO de novo**
4. **Cole novamente** o bloco TOML
5. Verifique **caractere por caractere** se não tem erros
6. Save e aguarde 3 minutos

---

### Problema 2: Diz "You exceeded your current quota"

**Causa:** Sua conta OpenAI não tem créditos

**Solução:**
1. Acesse: https://platform.openai.com/account/billing
2. Clique em: "Add payment method"
3. Adicione um cartão de crédito
4. Adicione pelo menos $5 de créditos
5. Aguarde 5-10 minutos
6. Teste novamente

**Custos:**
- Cada artigo: ~$0.01 (GPT-4 Turbo)
- Cada imagem: ~$0.08 (DALL-E 3)
- Total: ~$0.09 por conteúdo completo

---

### Problema 3: APIs continuam vermelhas

**Causa:** Formato incorreto no TOML

**Solução:** Use este template EXATO:

```toml
OPENAI_API_KEY = "sua_chave_aqui"
TAVILY_API_KEY = "sua_chave_aqui"
SUPABASE_URL = "sua_url_aqui"
SUPABASE_KEY = "sua_chave_aqui"
```

**Regras:**
- Nome da variável em MAIÚSCULAS
- Espaço antes do `=`
- Espaço depois do `=`
- Aspas duplas `"` ao redor do valor
- SEM vírgulas
- SEM ponto e vírgula
- Uma variável por linha

---

### Problema 4: App não reinicia

**Solução:**
1. Vá para: https://share.streamlit.io
2. Encontre seu app
3. Menu `⋮` → **Reboot app**
4. Aguarde 2-3 minutos
5. Recarregue a página

---

### Problema 5: Chave não funciona mesmo correta

**Causa:** Chave pode estar desabilitada ou expirada

**Solução:**
1. Acesse: https://platform.openai.com/api-keys
2. **DELETE** a chave antiga
3. **Crie uma NOVA** chave
4. Copie a nova chave
5. Atualize no Streamlit Cloud
6. Save e teste novamente

---

## 🎯 CHECKLIST FINAL

Antes de pedir ajuda, verifique:

- [ ] Criei uma NOVA chave na OpenAI Platform
- [ ] A chave começa com `sk-proj-` ou `sk-`
- [ ] Copiei a chave COMPLETA (50+ caracteres)
- [ ] Fui em Settings → Secrets no Streamlit Cloud
- [ ] APAGUEI tudo e colei o novo bloco TOML
- [ ] Substituí `COLE_SUA_CHAVE_AQUI` pela chave real
- [ ] Usei aspas DUPLAS `"` (não simples)
- [ ] Tem espaços ao redor do `=`
- [ ] Cliquei em Save
- [ ] Aguardei 2-3 minutos para rebuild
- [ ] Recarreguei https://conteudo-automacao.streamlit.app
- [ ] Verifiquei que OPENAI_API_KEY está VERDE
- [ ] Minha conta OpenAI tem créditos

---

## 📞 AINDA NÃO FUNCIONA?

Se você seguiu TODOS os passos acima e ainda não funciona:

### Opção 1: Use Replicate (GRATUITO)

1. Acesse: https://replicate.com/signin
2. Crie uma conta (pode usar Google)
3. Vá em: https://replicate.com/account/api-tokens
4. Copie seu token (começa com `r8_`)
5. Adicione no Streamlit Secrets:

```toml
REPLICATE_API_TOKEN = "r8_seu_token_aqui"
```

6. A aplicação vai usar Replicate (Flux) para imagens
7. **Flux Schnell é GRATUITO!** 🎉

---

### Opção 2: Desabilitar Geração de Imagens

Temporariamente, se você só quer testar a geração de texto:

1. Gere o conteúdo normalmente
2. A aplicação vai usar o gerador de texto fallback
3. Ainda terá uma imagem (com gradiente colorido)
4. Configure a OpenAI depois com calma

---

## ✅ SUCESSO!

Se tudo funcionou:

- ✅ APIs todas VERDES na sidebar
- ✅ Conteúdo gerado sem erros
- ✅ Imagem relevante ao tema
- ✅ Pode salvar no Google Docs

**Parabéns! Agora você pode:**
- Criar conteúdos ilimitados
- Gerar imagens com IA
- Salvar tudo no Supabase
- Exportar para Google Docs

---

## 📚 DOCUMENTOS DE APOIO

- **Instruções Globais:** `INSTRUCOES_GLOBAIS.md`
- **Melhorias de Imagens:** `MELHORIAS_IMAGENS.md`
- **Setup do Supabase:** `SUPABASE_SETUP.md`
- **Troubleshooting OpenAI:** `CORRIGIR_OPENAI_KEY.md`

---

**Atualizado:** Novembro 2025  
**Versão:** Guia Definitivo de Correção  
**Status:** Completo e Testado

