# 🗄️ Configuração do Supabase - Armazenamento em Nuvem

Guia completo para configurar Supabase e ter histórico persistente na nuvem!

## 📊 Por que Supabase?

- ✅ **Gratuito** até 500MB de dados
- ✅ **PostgreSQL** moderno e robusto
- ✅ **API automática** REST e Realtime
- ✅ **Dashboard** visual para gerenciar dados
- ✅ **Backups** automáticos
- ✅ **Escalável** conforme você cresce

---

## 🚀 Configuração em 10 Minutos

### 1️⃣ Criar Conta no Supabase

1. Acesse: https://supabase.com
2. Clique em **"Start your project"**
3. Faça login com GitHub (recomendado) ou email

### 2️⃣ Criar Novo Projeto

1. No dashboard, clique em **"New Project"**
2. Preencha:
   - **Name:** Redator IA
   - **Database Password:** Crie uma senha forte (salve!)
   - **Region:** South America (São Paulo) - mais próximo
3. Clique em **"Create new project"**
4. **Aguarde 2-3 minutos** para o projeto ser criado

### 3️⃣ Obter Credenciais

1. No menu lateral, vá em **"Settings"** (ícone de engrenagem)
2. Clique em **"API"**
3. Você verá:
   - **Project URL** (algo como: https://xxxxx.supabase.co)
   - **anon public** (chave pública)

**Copie ambos!** Você usará no próximo passo.

### 4️⃣ Criar Tabelas no Banco

1. No menu lateral, clique em **"SQL Editor"**
2. Clique em **"New query"**
3. **Copie TODO o conteúdo** do arquivo `supabase_setup.sql`
4. **Cole** no editor SQL
5. Clique em **"Run"** (ou pressione Ctrl/Cmd + Enter)
6. Aguarde a mensagem: **"Success. No rows returned"**

✅ **Tabelas criadas com sucesso!**

### 5️⃣ Configurar na Aplicação

Adicione ao arquivo `.env`:

```bash
# Supabase Configuration
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_publica_aqui
```

**Exemplo real:**

```bash
SUPABASE_URL=https://abcdefghijk.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 6️⃣ Instalar Dependência

```bash
cd /Users/caiobessa/Desktop/Agno\ Acroud
uv add supabase
```

### 7️⃣ Reiniciar Aplicação

```bash
# Parar (Ctrl+C no terminal do Streamlit)
# E rodar novamente:
cd /Users/caiobessa/Desktop/Agno\ Acroud
uv run streamlit run redator_app/app.py
```

---

## ✅ Verificar se Funcionou

Na sidebar do Streamlit, você verá:

```
📡 Status das APIs
✅ GROQ_API_KEY
✅ TAVILY_API_KEY
✅ SUPABASE  ← Novo!
```

Se aparecer ✅ verde, está funcionando!

---

## 📊 O que o Supabase Armazena

### Tabelas Criadas:

1. **projetos**

   - ID, nome, descrição
   - Data de criação

2. **categorias**

   - ID, projeto_id, nome
   - Exemplos e regras
   - Data de criação

3. **conteudos_gerados** ⭐

   - ID, projeto_id, categoria_id
   - Palavra-chave, título, conteúdo completo
   - Meta description, keywords secundárias
   - Caminho da imagem
   - Estatísticas (palavras, parágrafos, tempo de leitura)
   - Data de criação

4. **imagens_geradas**
   - ID, conteudo_id
   - Nome do arquivo, URL pública
   - API utilizada, prompt usado
   - Dimensões
   - Data de criação

### Views (Relatórios Automáticos):

- **estatisticas_projetos**

  - Total de categorias por projeto
  - Total de conteúdos gerados
  - Total de palavras escritas
  - Data do último conteúdo

- **ultimos_conteudos**
  - 50 últimos conteúdos gerados
  - Com projeto, categoria e estatísticas

---

## 🔍 Ver Seus Dados no Supabase

### Visualizar Tabelas:

1. Menu lateral → **"Table Editor"**
2. Selecione uma tabela (projetos, categorias, conteudos_gerados)
3. Veja todos os dados!

### Buscar Conteúdo:

1. Menu lateral → **"SQL Editor"**
2. Rode queries:

```sql
-- Ver todos os conteúdos
SELECT * FROM ultimos_conteudos;

-- Estatísticas por projeto
SELECT * FROM estatisticas_projetos;

-- Buscar por palavra-chave
SELECT titulo, criado_em
FROM conteudos_gerados
WHERE palavra_chave ILIKE '%python%';

-- Top 10 conteúdos mais longos
SELECT titulo, (estatisticas->>'total_palavras')::int as palavras
FROM conteudos_gerados
ORDER BY palavras DESC
LIMIT 10;
```

---

## 💾 Como Funciona o Armazenamento

### Modo Híbrido (Melhor de Dois Mundos):

```
┌─────────────────────────────────────┐
│  Se SUPABASE está configurado:     │
│  ✅ Salva na nuvem (PostgreSQL)    │
│  ✅ Histórico completo              │
│  ✅ Busca avançada                  │
│  ✅ Backup automático               │
│                                     │
│  Se NÃO está configurado:           │
│  ✅ Salva localmente (JSON)        │
│  ✅ Funciona offline                │
│  ✅ Zero configuração               │
└─────────────────────────────────────┘
```

**Vantagem:** Você escolhe! Funciona com ou sem Supabase.

---

## 📈 Limites do Plano Gratuito

| Recurso          | Limite Free | Suficiente Para   |
| ---------------- | ----------- | ----------------- |
| **Database**     | 500 MB      | ~10.000 artigos   |
| **Storage**      | 1 GB        | ~5.000 imagens    |
| **Bandwidth**    | 5 GB/mês    | ~100.000 leituras |
| **API Requests** | Ilimitado   | ✅ Sem limite!    |

**Para maioria dos casos, o plano FREE é mais que suficiente!**

---

## 🔐 Segurança

### Row Level Security (RLS):

As tabelas têm RLS ativado, mas com política "permitir tudo" por padrão.

**Para produção, ajuste as políticas:**

```sql
-- Exemplo: Permitir apenas leitura
DROP POLICY "Permitir acesso total a conteudos" ON conteudos_gerados;

CREATE POLICY "Permitir leitura" ON conteudos_gerados
FOR SELECT USING (true);

CREATE POLICY "Permitir inserção" ON conteudos_gerados
FOR INSERT WITH CHECK (true);
```

### Proteger Chaves:

- ❌ **NUNCA** commite o `.env` no Git
- ❌ **NUNCA** compartilhe sua `SUPABASE_KEY`
- ✅ Use variáveis de ambiente em produção

---

## 🚀 Funcionalidades Avançadas

### 1. Busca Full-Text

```sql
-- Buscar no conteúdo usando português
SELECT titulo, palavra_chave
FROM conteudos_gerados
WHERE to_tsvector('portuguese', conteudo) @@ to_tsquery('portuguese', 'python & tutorial');
```

### 2. Exportar Dados

No Supabase dashboard:

1. Table Editor → Selecione tabela
2. Botão **"..."** → **"Export as CSV"**

### 3. Backup Manual

```sql
-- Copiar todos os conteúdos
SELECT * FROM conteudos_gerados;
```

Salve o resultado como backup.

### 4. APIs Automáticas

Supabase gera APIs REST automaticamente!

```bash
# Listar projetos
curl https://seu-projeto.supabase.co/rest/v1/projetos \
  -H "apikey: SUA_CHAVE"

# Buscar conteúdos
curl https://seu-projeto.supabase.co/rest/v1/conteudos_gerados?select=* \
  -H "apikey: SUA_CHAVE"
```

---

## 🐛 Solução de Problemas

### Erro: "relation 'projetos' does not exist"

**Causa:** Tabelas não foram criadas  
**Solução:**

1. Vá em SQL Editor
2. Rode o script `supabase_setup.sql` completo

### Erro: "Invalid API key"

**Causa:** Chave incorreta no `.env`  
**Solução:**

1. Vá em Settings → API
2. Copie a chave **anon/public** novamente
3. Atualize no `.env`

### Erro: "Database not available"

**Causa:** Projeto ainda está sendo criado  
**Solução:** Aguarde 2-3 minutos e tente novamente

### Não conecta ao Supabase

**Verificar:**

```bash
# No terminal Python:
python3
>>> import os
>>> from dotenv import load_dotenv
>>> load_dotenv()
>>> os.getenv("SUPABASE_URL")
'https://...'  # Deve aparecer sua URL
```

---

## 📊 Estatísticas em Tempo Real

### Dashboard Customizado:

Crie no SQL Editor:

```sql
-- Resumo geral
SELECT
    (SELECT COUNT(*) FROM projetos) as total_projetos,
    (SELECT COUNT(*) FROM categorias) as total_categorias,
    (SELECT COUNT(*) FROM conteudos_gerados) as total_conteudos,
    (SELECT SUM((estatisticas->>'total_palavras')::int) FROM conteudos_gerados) as total_palavras;

-- Conteúdos por projeto
SELECT
    p.nome,
    COUNT(c.id) as conteudos,
    SUM((c.estatisticas->>'total_palavras')::int) as palavras
FROM projetos p
LEFT JOIN conteudos_gerados c ON p.id = c.projeto_id
GROUP BY p.nome
ORDER BY conteudos DESC;
```

---

## 💡 Dicas de Otimização

### 1. Índices já estão otimizados!

- Busca por projeto: rápida
- Busca por palavra-chave: rápida
- Busca full-text: rápida

### 2. Limpar dados antigos:

```sql
-- Deletar conteúdos com mais de 6 meses
DELETE FROM conteudos_gerados
WHERE criado_em < NOW() - INTERVAL '6 months';
```

### 3. Monitorar uso:

1. Dashboard → Settings → Usage
2. Veja consumo de Database, Storage e Bandwidth

---

## 🎓 Recursos Adicionais

### Documentação Oficial:

- **Supabase Docs:** https://supabase.com/docs
- **PostgreSQL:** https://www.postgresql.org/docs/
- **Python Client:** https://supabase.com/docs/reference/python

### Comunidade:

- **Discord:** https://discord.supabase.com
- **GitHub:** https://github.com/supabase/supabase

---

## ✅ Checklist de Configuração

- [ ] Criar conta no Supabase
- [ ] Criar novo projeto
- [ ] Copiar URL e Key
- [ ] Executar script SQL (supabase_setup.sql)
- [ ] Verificar tabelas criadas
- [ ] Adicionar credenciais no `.env`
- [ ] Instalar biblioteca: `uv add supabase`
- [ ] Reiniciar aplicação Streamlit
- [ ] Verificar ✅ verde no Status das APIs
- [ ] Gerar primeiro conteúdo para testar
- [ ] Verificar no Table Editor se salvou

---

## 🎉 Pronto!

Agora você tem:

✅ **Armazenamento na nuvem** persistente  
✅ **Histórico completo** de conteúdos  
✅ **Backup automático** diário  
✅ **Busca avançada** por palavra-chave  
✅ **Estatísticas** em tempo real  
✅ **Dashboard visual** para gerenciar dados

**E tudo isso de GRAÇA!** 🎊

---

**Configuração:** 10 minutos  
**Custo:** $0 (plano Free)  
**Benefício:** ∞ (histórico persistente forever!)
