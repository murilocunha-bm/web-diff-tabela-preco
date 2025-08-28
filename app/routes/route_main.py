from flask import Blueprint, render_template


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


# @main_bp.route("/nova")
# def nova():
#     return render_template(".html")

