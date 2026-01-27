# 🎁 Wishlist Serverless com Git Scraping

[![Update Prices](https://github.com/kaiosdev/Wishlist-/actions/workflows/scrape.yml/badge.svg)](https://github.com/kaiosdev/Wishlist-/actions/workflows/scrape.yml)

https://kaiosdev.github.io/Wishlist-/

Sistema automatizado de lista de desejos (wishlist) totalmente serverless, hospedado no GitHub Pages com atualização automática de preços via GitHub Actions.

## ✨ Funcionalidades

- 🤖 **Automação Total**: Atualização automática de preços via GitHub Actions
- 🌐 **100% Serverless**: Hospedado gratuitamente no GitHub Pages
- 🎨 **Interface Moderna**: Design dark mode responsivo com animações suaves
- 🔄 **Duas Visualizações**: Alterne entre Grid View (cards) e List View (linhas)
- 🛍️ **Multi-Lojas**: Suporte para Amazon, Mercado Livre, Magalu, Kabum e mais
- 📱 **Responsivo**: Funciona perfeitamente em mobile, tablet e desktop
- ⚡ **Performance**: Carregamento rápido com lazy loading de imagens
- ♿ **Acessível**: Suporte a leitores de tela e navegação por teclado

## 🚀 Como Usar

### 2. Estrutura de Arquivos

```
seu-repositorio/
├── .github/
│   └── workflows/
│       └── scrape.yml          # Workflow de automação
├── index.html                  # Página principal
├── style.css                   # Estilos
├── script.js                   # JavaScript
├── data.json                   # Dados dos produtos
├── scraper.py                  # Script Python de scraping
├── requirements.txt            # Dependências Python
└── README.md                   # Este arquivo
```

### 3. Configurar GitHub Pages

1. Vá em **Settings** → **Pages**
2. Em **Source**, selecione **Deploy from a branch**
3. Escolha a branch `main` e a pasta `/ (root)`
4. Clique em **Save**
5. Aguarde alguns minutos e acesse: `https://SEU_USUARIO.github.io/SEU_REPOSITORIO/`

### 4. Adicionar Produtos

#### Método 1: Editar `data.json` diretamente

Edite o arquivo `data.json` e adicione suas URLs:

```json
{
  "last_updated": "2026-01-27 00:00:00",
  "products": [
    {
      "image": "",
      "title": "",
      "price": "",
      "url": "https://www.amazon.com.br/produto-exemplo/dp/B08XYZ123",
      "store": ""
    }
  ]
}
```

**Importante**: Você só precisa adicionar o campo `url`. O scraper preencherá automaticamente `image`, `title`, `price` e `store`.

#### Método 2: Usar arquivo `urls.txt` (requer modificação do script)

Descomente as linhas 133-149 em `scraper.py` e crie um arquivo `urls.txt`:

```
https://www.amazon.com.br/produto1
https://www.mercadolivre.com.br/produto2
https://www.kabum.com.br/produto3
```

### 5. Executar a Atualização

#### Manualmente (Recomendado para primeiro teste)

1. Vá em **Actions** no GitHub
2. Clique em **🤖 Atualizar Preços da Wishlist**
3. Clique em **Run workflow** → **Run workflow**
4. Aguarde a execução (1-3 minutos)

#### Automaticamente

O workflow está configurado para rodar:
- 🕐 **Diariamente às 8h UTC** (5h horário de Brasília)
- 🔄 **A cada push** no `data.json` ou `scraper.py`

## 🛠️ Personalização

### Modificar Seletores de Preço (Importante!)

O script possui seletores genéricos, mas cada loja pode ter sua estrutura específica. Edite `scraper.py` na linha 145:

```python
price_selectors = [
    # Amazon
    '.a-price-whole',
    '#priceblock_ourprice',
    
    # Mercado Livre
    '.andes-money-amount__fraction',
    
    # Sua loja específica aqui
    '.sua-classe-de-preco',
]
```

### Alterar Cores do Tema

Edite as variáveis CSS em `style.css` (linhas 6-24):

```css
:root {
    --bg-primary: #0f0f23;        /* Cor de fundo principal */
    --accent-primary: #00d9ff;    /* Cor de destaque */
    --accent-secondary: #7f5af0;  /* Cor secundária */
}
```

### Alterar Frequência de Atualização

Edite `.github/workflows/scrape.yml` (linha 11):

```yaml
schedule:
  - cron: '0 8 * * *'  # Todo dia às 8h UTC
  # Exemplos:
  # '0 */6 * * *'  -> A cada 6 horas
  # '0 0 * * 0'    -> Todo domingo à meia-noite
  # '0 12 * * 1-5' -> Segunda a sexta ao meio-dia
```

## 🔧 Troubleshooting

### ❌ Erro 403 Forbidden

**Causa**: Site bloqueou o scraper  
**Solução**: O script já usa User-Agent realista, mas alguns sites precisam de cookies ou JavaScript

### ❌ Preço não encontrado

**Causa**: Seletor CSS inválido para aquela loja  
**Solução**: 
1. Abra o site no navegador
2. Inspecione o elemento do preço (F12)
3. Adicione a classe/ID no array `price_selectors`

### ❌ Imagem não carrega

**Causa**: URL relativa ou proteção de hotlink  
**Solução**: O script já converte URLs relativas, mas alguns sites bloqueiam hotlinking

### 🔍 Ver logs de execução

1. Vá em **Actions** no GitHub
2. Clique na execução mais recente
3. Expanda os steps para ver logs detalhados

## 🎯 Atalhos de Teclado

- **V**: Alterna entre Grid/Lista
- **R**: Recarrega dados

## 📊 Tecnologias Utilizadas

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python 3.11
- **Libraries**: 
  - `requests` - Requisições HTTP
  - `beautifulsoup4` - Parsing HTML
  - `lxml` - Parser rápido
- **CI/CD**: GitHub Actions
- **Hosting**: GitHub Pages

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para:

1. Fork o projeto
2. Criar uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abrir um Pull Request

## ⚠️ Avisos Legais

- ⚖️ **Respeite os Termos de Serviço**: Alguns sites proíbem scraping. Use por sua conta e risco.
- 🚦 **Rate Limiting**: O script possui delays entre requisições para não sobrecarregar servidores.
- 🔒 **Dados Públicos**: Este script apenas extrai dados públicos visíveis em páginas de produtos.

## 📝 Licença

MIT License - Sinta-se livre para usar e modificar!
