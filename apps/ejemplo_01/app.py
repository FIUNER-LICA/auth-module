from flask import Flask, request, Blueprint
from auth_module import AuthModule

app = Flask(__name__)
bp = Blueprint("auth", __name__, url_prefix="/auth")

auth = AuthModule(title="Demo Auth")

# Layout base como string
def render_layout(content: str) -> str:
    return f"""
    <!doctype html>
    <html>
    <head><title>Mi App</title></head>
    <body>
        <header><h1>Mi Aplicación Web</h1></header>
        <main>
            {content}
        </main>
        <footer><p>Pie de página</p></footer>
    </body>
    </html>
    """

@bp.route("/")
def index():
    return render_layout("""
        <p><a href="/auth/register">Registro</a></p>
        <p><a href="/auth/login">Login</a></p>
    """)

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        ok, msg = auth.register_user(request.form)
        return render_layout(f"<p>{msg}</p><a href='/auth/'>Volver</a>")
    return render_layout(auth.render_register_form())

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        ok, msg = auth.authenticate(request.form)
        return render_layout(f"<p>{msg}</p><a href='/auth/'>Volver</a>")
    return render_layout(auth.render_login_form())

# Registrar el blueprint
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
