from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from os import path, getenv
#
import app.controllers.loggers as msgs
from constants import XLS_DIFERENCA_LITORAL, XLS_DIFERENCA_ST, XLS_DIFERENCA_SP2, CSV_CUSTOS
from app.controllers.loggers import logger
from app.models.precos.dif_df import main
from app.models.custos.custo import criar_csv_custos


main_bp = Blueprint(
    name = "main",
    import_name = __name__,
    template_folder = '',
    static_folder = '',
    url_prefix = '',
    )


@main_bp.route("/")
def home():
    return render_template("index.html", resultado=None)


@main_bp.route("/precos")
def precos():
    return render_template("precos.html", resultado=None)


@main_bp.route("/custos")
def custos():
    return render_template("custos.html", resultado=None)


@main_bp.route("/sobre")
def sobre():
    return render_template("sobre.html", resultado=None)


@main_bp.route("/diferencas", methods=["POST"])
def diferencas():
    arquivo = request.files.get("file")

    if not arquivo or arquivo.filename == "":
        flash("⚠️ Você precisa selecionar um arquivo antes de continuar.", "warning")
        return redirect(url_for("main.precos"))    
    else:
        # if request.method == "POST":
        msgs.log_messages.clear()

        # pegar as escolhas do usuario
        file = request.files["file"]
        tabela = request.form.get("optradio")
        pasta_xls = getenv('PASTA_XLS')
        arquivo_com_caminho = path.join(pasta_xls, file.filename)

        # gravar o arquivo selecionado na pasta padrao do servidor
        file.save(arquivo_com_caminho)
        logger.info(f'📥 Arquivo gravado com sucesso: {file.filename}')

        # criar as planilhas de diferencas
        resultado = main(xls_preco_novo=arquivo_com_caminho, codigo_tabela=tabela)

        if resultado.empty:
            resultado = None
        else:
            # resultado = df_diff.to_html(index=False, classes="table table-striped")
            resultado = resultado.to_dict(orient="records")
        return render_template("precos_resultado.html", tabela=tabela, resultado=resultado, mensagens=msgs.log_messages)


@main_bp.route("/custos_resultado", methods=["POST"])
def custos_resultado():
    file = request.files.get("file")

    if not file or file.filename == "":
        flash("⚠️ Você precisa selecionar um arquivo antes de continuar.", "warning")
        return redirect(url_for("main.custos"))    
    else:
        # if request.method == "POST":
        msgs.log_messages.clear()
        pasta_xls = getenv('PASTA_XLS')
        arquivo_com_caminho = path.join(pasta_xls, file.filename)

        file.save(arquivo_com_caminho)
        logger.info(f'📥 Arquivo gravado com sucesso: {file.filename}')

        resultado = criar_csv_custos(xls_filename=arquivo_com_caminho)

        if resultado.empty:
            resultado = None
        else:
            # resultado = df_diff.to_html(index=False, classes="table table-striped")
            resultado = resultado.to_dict(orient="records")
        return render_template("custos_resultado.html", resultado=resultado, mensagens=msgs.log_messages)


@main_bp.route("/download_diferencas/<tabela>", methods=["GET"])
def download_diferencas(tabela):
    # Caminho do arquivo no servidor
    arquivo = {
        'st01': XLS_DIFERENCA_ST,
        'sp02': XLS_DIFERENCA_SP2,
        'st15': XLS_DIFERENCA_LITORAL,
    }
    return send_file(
        arquivo[tabela],
        as_attachment=True,                             # força o download
        download_name=path.basename(arquivo[tabela])    # nome sugerido ao usuário
    )


@main_bp.route("/download_custos", methods=["GET"])
def download_custos():
    return send_file(
        CSV_CUSTOS,
        as_attachment=True,                             # força o download
        download_name=path.basename(CSV_CUSTOS)         # nome sugerido ao usuário
    )


# @main_bp.route("/nova")
# def nova():
#     return render_template(".html")
