from flask import Blueprint, render_template, request
import pandas as pd


main_bp = Blueprint(
    name = "main",
    import_name = __name__,
    template_folder = '',
    static_folder = '',
    url_prefix = '',
    )


@main_bp.route("/")
def home():
    return render_template("/tab_preco/index.html")


@main_bp.route("/diferencas", methods=["POST"])
def diferencas():
    if "file" not in request.files or request.files["file"].filename == "":
        return "⚠️ Nenhum arquivo selecionado. Por favor, escolha uma planilha!"    
    
    # pega o arquivo enviado
    file = request.files["file"]

    if not file:
        return "Nenhum arquivo enviado!"

    # carrega a planilha enviada
    df_novo = pd.read_excel(file)

    # planilha de referência (poderia vir do banco ou de outro arquivo)
    df_ref = pd.DataFrame({
        "Produto": ["Arroz", "Feijão", "Macarrão", "Óleo"],
        "Preço": [10.0, 7.5, 6.0, 8.0]
    })

    # junta pelo nome do produto
    df_merge = df_ref.merge(df_novo, on="Produto", suffixes=("_ref", "_novo"))

    # encontra diferenças de preço
    df_diff = df_merge[df_merge["Preço_ref"] != df_merge["Preço_novo"]]

    if df_diff.empty:
        return "Nenhuma diferença encontrada ✅"

    # converte resultado em HTML para exibir no navegador
    return df_diff.to_html(index=False, classes="table table-striped")


# @main_bp.route("/nova")
# def nova():
#     return render_template(".html")

