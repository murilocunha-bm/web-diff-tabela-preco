# 📊 App Flask de Atualização de Preços

Aplicação web desenvolvida em **Python (Flask)** para gerenciamento e atualização de preços de produtos.  
O sistema permite importar arquivos (ex: Excel/CSV), processar os dados e exibir relatórios através de uma interface web simples e eficiente.

---

## 🚀 Funcionalidades
- Upload de arquivos com novos preços (Excel/CSV).  
- Processamento e validação automática dos dados.  
- Exibição dos preços em tabela via interface web.  
- Histórico de atualizações.  
- API para integração com outros sistemas (opcional).  

---

## 🛠️ Tecnologias Utilizadas
- [Python 3.x](https://www.python.org/)  
- [Flask](https://flask.palletsprojects.com/)  
- [Pandas](https://pandas.pydata.org/)  
- [Bootstrap](https://getbootstrap.com/) para o front-end  
- [SQLite/PostgreSQL/MySQL] (dependendo do banco configurado)  

---

## 📂 Estrutura do Projeto
```yaml
app/
│── static/ # Arquivos estáticos (CSS, JS, imagens)
│── templates/ # Páginas HTML (Jinja2)
│── routes/ # Rotas Flask
│── services/ # Regras de negócio (processamento de preços)
│── models/ # Modelos do banco de dados
│── init.py # Inicialização da aplicação
│── app.py # Ponto de entrada principal
config.py # Configurações do projeto
requirements.txt # Dependências do projeto
README.md # Documentação
```

---

## ⚙️ Instalação e Execução

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 2️⃣ Criar ambiente virtual e instalar dependências

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3️⃣ Configurar variáveis de ambiente
```ini
# Crie um arquivo .env na raiz do projeto:
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///precos.db
SECRET_KEY=sua_chave_secreta
```

### 4️⃣ Executar a aplicação
```bash
flask run
# Acesse em: http://localhost:5000
```

---

### ✅ Exemplo de Uso
---
Acesse a aplicação no navegador.

Faça upload de um arquivo .xlsx

O sistema processará e exibirá os preços atualizados em tabela.

Baixe ou visualize relatórios conforme necessário.

📦 Deploy em Produção:
---
Servidores recomendados: Gunicorn + Nginx ou Waitress (Windows).

Banco de dados: PostgreSQL em produção é recomendado.

🤝 Contribuição
---
Faça um fork do projeto.

Crie uma branch para sua feature (git checkout -b minha-feature).

Commit suas alterações (git commit -m 'Adicionando nova feature').

Push para a branch (git push origin minha-feature).

Abra um Pull Request.

📜 Licença
---

Este projeto está licenciado sob a MIT License.

Sinta-se à vontade para usar e modificar conforme necessário.