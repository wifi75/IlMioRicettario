from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import check_password_hash

from models.user import User


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(
            url_for("admin.dashboard")
        )

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password_hash,
            password
        ):

            login_user(user)

            return redirect(
                url_for("admin.dashboard")
            )

        flash(
            "Credenziali non valide",
            "danger"
        )

    return render_template(
        "admin/login.html"
    )


@admin_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("admin.login")
    )


@admin_bp.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "admin/dashboard.html"
    )