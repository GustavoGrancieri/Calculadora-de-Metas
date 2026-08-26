#Plataforma de Relatórios de Vendas

Uma aplicação web desenvolvida em Python (Flask) para automatizar a geração de relatórios de vendas, cálculo de metas e envio de resultados para a equipe. 

O sistema processa planilhas de vendas, calcula o atingimento de metas individuais e globais, gera relatórios em PDF com design profissional e dispara automaticamente para os e-mails configurados.

##Funcionalidades

* **Upload de Planilhas:** Interface web moderna (efeito Glassmorphism) para upload de dados de Vendas e Metas.
* **Processamento de Dados:** Utiliza `pandas` para cruzar dados, agrupar vendas por vendedor e por categoria de produtos.
* **Cálculo Automático:** Subtrai o valor vendido da meta e define automaticamente a porcentagem de atingimento.
* **Geração de PDFs Individuais:** Cria relatórios detalhados em PDF para cada vendedor utilizando `xhtml2pdf`.
* **Relatório Consolidado:** Gera um relatório geral com o desempenho de toda a equipe para a supervisão.
* **Disparo de E-mails Automático:** Integração via protocolo SMTP para enviar os PDFs diretamente para a caixa de entrada dos envolvidos.

##Tecnologias Utilizadas

* **Backend:** Python, Flask
* **Processamento de Dados:** Pandas, OpenPyXL
* **Geração de PDF:** xhtml2pdf
* **Frontend:** HTML5, CSS3
* **Envio de E-mails:** smtplib, email.message

##Estrutura do Projeto

```text
/
├── app.py                 # Arquivo principal e rotas do servidor Flask
├── requirements.txt       # Lista de dependências do Python
├── .gitignore             # Arquivos ignorados pelo Git (planilhas, PDFs, etc.)
├── templates/
│   ├── index.html         # Página inicial com formulário de upload
│   └── sucesso.html       # Tela de confirmação de envio
└── static/
    ├── style.css          # Estilização da página (Glassmorphism)
    └── Background.mp4     # Vídeo de fundo da interface web
