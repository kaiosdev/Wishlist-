# 🎁 Wishlist Serverless

[![Status do Site](https://img.shields.io/github/deployments/kaiosdev/Wishlist-/github-pages?label=Site&style=for-the-badge&logo=github)](https://kaiosdev.github.io/Wishlist-/)
[![Atualização de Preços](https://img.shields.io/github/actions/workflow/status/kaiosdev/Wishlist-/scrape.yml?label=Scraper&style=for-the-badge&color=success)](https://github.com/kaiosdev/Wishlist-/actions)

> **Acesse aqui:** [https://kaiosdev.github.io/Wishlist-/](https://kaiosdev.github.io/Wishlist-/)

Uma solução **100% gratuita e serverless** para monitorar preços de produtos. Hospedado no GitHub Pages, com backend rodando via GitHub Actions.

---

## ✨ Destaques

* 🤖 **Automação Inteligente:** Adicione links direto pelo site. Um robô busca a foto, título e preço automaticamente.
* 🌐 **100% Serverless:** Sem servidores, sem banco de dados, sem custo. Tudo roda no ecossistema GitHub.
* 🎨 **UI Moderna:** Design Dark Mode, responsivo para mobile e com visualização em Grade ou Lista.

---

## 🚀 Como Usar (Adicionar Produtos)

Esqueça a edição de arquivos. O projeto usa **IssueOps** para gerenciar a lista:

1.  Acesse o **[Site da Wishlist](https://kaiosdev.github.io/Wishlist-/)**.
2.  Cole o link do produto (Amazon, Mercado Livre, Kabum, etc.) no campo superior.
3.  Clique no botão **`+`**.
4.  Confirme a abertura da **Issue** no GitHub.

> **O que acontece depois?**
> Um robô detecta a Issue, valida o link, faz o scraping dos dados e atualiza o site em cerca de 2 minutos.

---

## 🛠️ Instalação (Para quem vai fazer Fork)

Se você quiser ter sua própria versão deste projeto:

1.  **Faça o Fork** deste repositório.
2.  Ative as permissões de escrita (Crucial):
    * Vá em `Settings` > `Actions` > `General` > `Workflow permissions`.
    * Marque **Read and write permissions**.
3.  Ative o GitHub Pages:
    * Vá em `Settings` > `Pages` > Source: `Deploy from a branch` > `main`.

---

## ⚙️ Configurações Avançadas

### 🕒 Frequência de Atualização

Os preços são atualizados automaticamente todo dia às **09:00 BRT**.
Para mudar, edite o arquivo `.github/workflows/scrape.yml`:

```yaml
schedule:
  - cron: '0 12 * * *' # Formato Cron UTC
```

### 🏪 Adicionar Novas Lojas

O scraper já suporta Amazon, Mercado Livre, Kabum, Magalu e Shopee.
Para adicionar outros, edite `scraper.py` e inclua o seletor CSS do preço:

```python
price_selectors = [
    '.nova-loja-classe-preco',
    '#id-do-preco',
]
```

### 🎨 Customizar Cores

Edite o arquivo `style.css`:

```css
:root {
    --bg: #0f0f23;     /* Fundo */
    --accent: #00d9ff; /* Destaque */
}
```

---

## 📊 Stack Tecnológico

* **HTML5 & CSS3**
* **JavaScript (Vanilla)**
* **Python 3.10** (BeautifulSoup4, Requests)
* **GitHub Actions** (CI/CD)

---

## ⚠️ Aviso Legal

Este projeto utiliza técnicas de web scraping apenas para dados públicos. Respeite os termos de serviço das lojas e utilize intervalos razoáveis de atualização para não sobrecarregar os servidores.

---

Desenvolvido por [Kaio Sobral](https://github.com/kaiosdev)