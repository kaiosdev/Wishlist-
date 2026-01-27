# 🚀 GUIA DE INSTALAÇÃO COMPLETO

## Passo 1: Criar Repositório no GitHub

1. Acesse https://github.com/new
2. Nome do repositório: `minha-wishlist` (ou qualquer nome)
3. Deixe **público** (necessário para GitHub Pages gratuito)
4. ✅ Marque "Add a README file"
5. Clique em **Create repository**

---

## Passo 2: Fazer Upload dos Arquivos

### Opção A: Via Interface Web (Mais Fácil)

1. No repositório criado, clique em **Add file** → **Upload files**
2. Arraste TODOS os arquivos deste projeto:
   ```
   ✅ index.html
   ✅ style.css
   ✅ script.js
   ✅ data.json
   ✅ scraper.py
   ✅ requirements.txt
   ✅ README.md
   ```
3. Para a pasta `.github/workflows/`:
   - Clique em **Create new file**
   - No nome, digite: `.github/workflows/scrape.yml`
   - Cole o conteúdo do arquivo `scrape.yml`
   - Clique em **Commit new file**

### Opção B: Via Git (Usuários Avançados)

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/minha-wishlist.git
cd minha-wishlist

# Copie todos os arquivos do projeto para esta pasta

# Adicione e faça commit
git add .
git commit -m "🎉 Setup inicial da wishlist"
git push origin main
```

---

## Passo 3: Ativar GitHub Pages

1. No repositório, vá em **Settings** (ícone de engrenagem)
2. No menu lateral esquerdo, clique em **Pages**
3. Em **Source**:
   - Branch: `main`
   - Folder: `/ (root)`
4. Clique em **Save**
5. Aguarde 2-3 minutos
6. Acesse: `https://SEU_USUARIO.github.io/minha-wishlist/`

🎉 **Pronto!** Seu site já está no ar!

---

## Passo 4: Adicionar Seus Produtos

### Método Recomendado: Editar `data.json`

1. Abra o arquivo `data.json` no GitHub
2. Clique no ícone de lápis (Edit)
3. Adicione seus produtos (você só precisa da URL):

```json
{
  "last_updated": "2026-01-27 12:00:00",
  "products": [
    {
      "image": "",
      "title": "",
      "price": "",
      "url": "https://www.amazon.com.br/Fone-Bluetooth-JBL-Tune-520BT/dp/B0BXXX",
      "store": ""
    },
    {
      "image": "",
      "title": "",
      "price": "",
      "url": "https://www.mercadolivre.com.br/teclado-mecanico/p/MLB123456",
      "store": ""
    }
  ]
}
```

4. Clique em **Commit changes**

---

## Passo 5: Executar o Scraper Pela Primeira Vez

1. Vá em **Actions** (no topo do repositório)
2. Se aparecer um aviso de workflows, clique em **I understand my workflows, go ahead and enable them**
3. Clique em **🤖 Atualizar Preços da Wishlist** (menu lateral)
4. Clique em **Run workflow** → **Run workflow** (botão verde)
5. Aguarde 1-3 minutos
6. ✅ Quando aparecer um ✓ verde, o scraping foi concluído!

---

## Passo 6: Verificar o Resultado

1. Abra o arquivo `data.json` no GitHub
2. Você verá que ele foi atualizado automaticamente com:
   - ✅ Imagens dos produtos
   - ✅ Títulos
   - ✅ Preços
   - ✅ Nome das lojas
3. Acesse seu site: `https://SEU_USUARIO.github.io/minha-wishlist/`
4. 🎉 **Seus produtos estão lá com imagens e preços!**

---

## 🔄 Atualizações Automáticas

A partir de agora, o sistema rodará automaticamente:
- ⏰ **Todos os dias às 5h da manhã** (horário de Brasília)
- 🔄 **Sempre que você modificar o `data.json`**

Você pode rodar manualmente a qualquer momento seguindo o Passo 5!

---

## 🎨 Personalização Rápida

### Alterar Título do Site

Edite `index.html` (linha 9):
```html
<title>🎁 Minha Lista de Desejos</title>
```

### Alterar Cores

Edite `style.css` (linhas 8-18):
```css
:root {
    --accent-primary: #00d9ff;    /* Cor principal (azul) */
    --accent-secondary: #7f5af0;  /* Cor secundária (roxo) */
}
```

Paletas recomendadas:
- **Verde/Amarelo**: `#2cb67d` e `#ffc803`
- **Rosa/Roxo**: `#ff006e` e `#8338ec`
- **Azul/Cyan**: `#0077b6` e `#00b4d8`

---

## 📱 Teste Mobile

Abra o site no celular:
- ✅ Deve funcionar perfeitamente
- ✅ Cards responsivos
- ✅ Botão de alternância funcional

---

## ❓ Problemas Comuns

### "Não vejo meus produtos"
- ✅ Verifique se o GitHub Pages está ativo (Settings → Pages)
- ✅ Aguarde 2-3 minutos após cada commit
- ✅ Force refresh: Ctrl+Shift+R (Windows) ou Cmd+Shift+R (Mac)

### "Preços não aparecem"
- ✅ Execute o workflow manualmente (Actions → Run workflow)
- ✅ Verifique os logs na aba Actions
- ✅ Alguns sites bloqueiam scraping (normal)

### "GitHub Action falhou"
- ✅ Verifique se o arquivo `requirements.txt` existe
- ✅ Veja os logs de erro na aba Actions
- ✅ Verifique se as URLs são válidas

---

## 🎯 Próximos Passos

1. ⭐ **Adicione mais produtos** no `data.json`
2. 🎨 **Personalize as cores** no `style.css`
3. 🔔 **Configure notificações** no GitHub para saber quando o preço cair
4. 📱 **Adicione à tela inicial** do celular (PWA-like)
5. 🤝 **Compartilhe** com amigos e família

---

## 💡 Dicas Profissionais

- Use URLs curtas (evite parâmetros de rastreamento `?ref=`)
- Teste o scraper com 2-3 produtos primeiro
- Alguns sites bloqueiam após muitas requisições (normal)
- Amazon geralmente funciona bem
- Mercado Livre tem boa compatibilidade

---

**✨ Parabéns! Sua wishlist automatizada está funcionando!**

Se tiver problemas, abra uma issue no GitHub do projeto.
