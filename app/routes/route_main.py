from datetime import datetime
from flask import Blueprint, render_template, request
from os import path, getenv
#
from app.models.diferenca_preco.dif_df import main
import app.controllers.loggers as msgs


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
    # if request.method == "POST":
    msgs.log_messages.clear()

    # pegar as escolhas do usuario
    file = request.files["file"]
    tabela = request.form.get("optradio")
    pasta_xls = getenv('PASTA_XLS')

    # criar as planilhas de diferencas
    resultado = main(xls_preco_novo=path.join(pasta_xls, file.filename), codigo_tabela=tabela)

    if resultado.empty:
        resultado = None
    else:
        # resultado = df_diff.to_html(index=False, classes="table table-striped")
        resultado = resultado.to_dict(orient="records")
    return render_template("/tab_preco/index.html", resultado=resultado, mensagens=msgs.log_messages)

# @main_bp.route("/nova")
# def nova():
#     return render_template(".html")

