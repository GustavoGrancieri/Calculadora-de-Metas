from flask import Flask, render_template, request
import os
import pandas as pd
from xhtml2pdf import pisa 
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

EMAIL_REMETENTE = "email@email.com" 
SENHA_REMETENTE = "Senha"
EMAIL_DESTINO_TESTE = "gustavograncieri@outlook.com"

def enviar_email(nome_vendedor, caminho_pdf, resumo_venda, resumo_meta, resumo_falta):
    msg = EmailMessage()
    msg['Subject'] = f'Resumo do seu desempenho - Agosto 2026 ({nome_vendedor})'
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINO_TESTE
    
    corpo = f"""🚀 Olá {nome_vendedor}! Resumo do seu desempenho - Agosto 2026

💰 Venda: R$ {resumo_venda:,.2f}
🔴 Meta: R$ {resumo_meta:,.2f}
⚠️ Falta para bater a meta: R$ {resumo_falta:,.2f}
Vamos melhorar!

📎 Em anexo seu relatório completo.
Bons negócios!"""
    msg.set_content(corpo)

    with open(caminho_pdf, 'rb') as f:
        pdf_data = f.read()
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=f'Relatorio_{nome_vendedor}.pdf')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA_REMETENTE)
            smtp.send_message(msg)
        print(f"E-mail de {nome_vendedor} enviado com sucesso para {EMAIL_DESTINO_TESTE}!")
    except Exception as e:
        print(f"Erro ao enviar email para {nome_vendedor}: {e}")

# ROTAS DO FLASK
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar_arquivos():
    if 'meta_file' not in request.files or 'vendas_file' not in request.files:
        return "Erro: Faltando arquivos."

    meta_file = request.files['meta_file']
    vendas_file = request.files['vendas_file']

    caminho_metas = os.path.join(app.config['UPLOAD_FOLDER'], meta_file.filename)
    caminho_vendas = os.path.join(app.config['UPLOAD_FOLDER'], vendas_file.filename)
    
    meta_file.save(caminho_metas)
    vendas_file.save(caminho_vendas)

    try:
        df_vendas = pd.read_excel(caminho_vendas, skiprows=8)
        df_vendas.columns = ['Emitente', 'Dt.Emissão', 'NFe', 'Série', 'Operação', 'Cliente', 
                             'Valor Total', 'Valor Desconto', 'Valor Líquido', 'Vendedor Nome', 
                             'Descrição Produto', 'Lista Grupo Produtos']
        df_vendas = df_vendas.dropna(subset=['Vendedor Nome'])
        df_vendas['Valor Líquido'] = pd.to_numeric(df_vendas['Valor Líquido'], errors='coerce')

        vendas_agrupadas = df_vendas.groupby('Vendedor Nome')['Valor Líquido'].sum().reset_index()

        meta_padrao = 457000.00 
        
        for index, row in vendas_agrupadas.iterrows():
            nome = row['Vendedor Nome']
            total_vendido = row['Valor Líquido']
            
            falta_para_meta = meta_padrao - total_vendido
            if falta_para_meta < 0: 
                falta_para_meta = 0

            df_vendedor_atual = df_vendas[df_vendas['Vendedor Nome'] == nome]
            grupos_produtos = df_vendedor_atual.groupby('Lista Grupo Produtos')['Valor Líquido'].sum().reset_index()

            linhas_tabela = ""
            for _, g_row in grupos_produtos.iterrows():
                grupo_nome = g_row['Lista Grupo Produtos']
                grupo_valor = g_row['Valor Líquido']
                linhas_tabela += f"<tr><td>{grupo_nome}</td><td>R$ {grupo_valor:,.2f}</td></tr>"

            html_content = f"""
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <style>
                    @page {{
                        size: A4;
                        margin: 2cm;
                    }}
                    body {{
                        font-family: Helvetica, Arial, sans-serif;
                        color: #333333;
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 30px;
                    }}
                    .header h1 {{
                        color: #2c3e50;
                        margin: 0;
                        font-size: 26px;
                    }}
                    .header p {{
                        color: #7f8c8d;
                        margin: 5px 0 0 0;
                        font-size: 14px;
                    }}
                    .resumo-box {{
                        background-color: #f8f9fa;
                        padding: 20px;
                        border-radius: 8px;
                        margin-bottom: 30px;
                        border-left: 6px solid #3498db;
                    }}
                    .resumo-box h2 {{
                        margin-top: 0;
                        font-size: 20px;
                        color: #2c3e50;
                    }}
                    .valor {{
                        font-size: 16px;
                        font-weight: bold;
                    }}
                    .venda {{ color: #27ae60; }}
                    .falta {{ color: #e74c3c; }}
                    
                    h3 {{
                        color: #2c3e50;
                        border-bottom: 2px solid #3498db;
                        padding-bottom: 5px;
                        margin-top: 30px;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 15px;
                    }}
                    th {{
                        background-color: #2c3e50;
                        color: #ffffff;
                        padding: 12px;
                        text-align: left;
                        font-size: 14px;
                    }}
                    td {{
                        padding: 10px 12px;
                        border-bottom: 1px solid #dddddd;
                        font-size: 13px;
                        color: #555555;
                    }}
                    tr:nth-child(even) {{
                        background-color: #f4f7f6;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Relatório de Desempenho</h1>
                    <p>Referência: Agosto 2026</p>
                </div>
                
                <div class="resumo-box">
                    <h2>Vendedor: {nome}</h2>
                    <p>Meta Global: <span class="valor">R$ {meta_padrao:,.2f}</span></p>
                    <p>Total Vendido: <span class="valor venda">R$ {total_vendido:,.2f}</span></p>
                    <p>Falta para Bater a Meta: <span class="valor falta">R$ {falta_para_meta:,.2f}</span></p>
                </div>

                <h3>Detalhamento por Grupo de Produtos</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Grupo de Produtos</th>
                            <th>Total Vendido (R$)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {linhas_tabela}
                    </tbody>
                </table>
            </body>
            </html>
            """

            caminho_pdf = os.path.join(app.config['UPLOAD_FOLDER'], f"Relatorio_{nome}.pdf")
            with open(caminho_pdf, "w+b") as pdf_file:
                pisa.CreatePDF(src=html_content, dest=pdf_file)

            enviar_email(nome, caminho_pdf, total_vendido, meta_padrao, falta_para_meta)

        return render_template('sucesso.html')

    except Exception as e:
        return f"<h1>Erro no processamento:</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
