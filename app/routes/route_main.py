from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from os import path, getenv
#
from app.models.precos.dif_df import main
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

        # criar as planilhas de diferencas
        resultado = main(xls_preco_novo=path.join(pasta_xls, file.filename), codigo_tabela=tabela)

        if resultado.empty:
            resultado = None
        else:
            # resultado = df_diff.to_html(index=False, classes="table table-striped")
            resultado = resultado.to_dict(orient="records")
        return render_template("precos_resultado.html", resultado=resultado, mensagens=msgs.log_messages)


@main_bp.route("/custos_resultado", methods=["POST"])
def custos_resultado():
    arquivo = request.files.get("file")

    if not arquivo or arquivo.filename == "":
        flash("⚠️ Você precisa selecionar um arquivo antes de continuar.", "warning")
        return redirect(url_for("main.custos"))    
    else:
        # if request.method == "POST":
        msgs.log_messages.clear()

        # COLOCAR AQUI AS TRATATIVAS PARA O CSV

        if resultado.empty:
            resultado = None
        else:
            # resultado = df_diff.to_html(index=False, classes="table table-striped")
            resultado = resultado.to_dict(orient="records")
        return render_template("custos_resultado.html", resultado=resultado, mensagens=msgs.log_messages)


# @main_bp.route("/nova")
# def nova():
#     return render_template(".html")
