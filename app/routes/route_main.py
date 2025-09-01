from datetime import datetime
from flask import Blueprint, render_template, request
from os import path, getenv
#
from app.models.diferenca_preco.dif_df import main


main_bp = Blueprint(
    name = "main",
    import_name = __name__,
    template_folder = '',
    static_folder = '',
    url_prefix = '',
    )


@main_bp.route("/")
def home():
    return render_template("/tab_preco/index.html", resultado=None)


@main_bp.route("/diferencas", methods=["POST"])
def diferencas():
    file = request.files["file"]
    
    pasta_xls = getenv('PASTA_XLS')
    resultado = main(path.join(pasta_xls, file.filename))

    if resultado.empty:
        resultado = None
    else:
        # resultado = df_diff.to_html(index=False, classes="table table-striped")
        resultado = resultado.to_dict(orient="records")
    
    return render_template("/tab_preco/index.html", resultado=resultado)
    
    # # pega o arquivo enviado
    # file = request.files["file"]

    # # carrega a planilha enviada
    # df_novo = pd.read_excel(file)

    # # planilha de referência (poderia vir do banco ou de outro arquivo)
    # df_ref = pd.DataFrame(
    #     {
    #         "Produto": ["Arroz", "Feijão", "Macarrão", "Óleo"],
    #         "Preço": [10.0, 7.5, 6.0, 8.0]
    #     }
    # )

    # # junta pelo nome do produto
    # df_merge = df_ref.merge(df_novo, on="Produto", suffixes=("_ref", "_novo"))

    # # encontra diferenças de preço
    # df_diff = df_merge[df_merge["Preço_ref"] != df_merge["Preço_novo"]]


# @main_bp.route("/nova")
# def nova():
#     return render_template(".html")

