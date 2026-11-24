"""
Rotas das páginas do site (parte visual).

- Usam somente dados de exemplo.
- Não acessam o banco de dados.
- Não alteram o CRUD de doadores do app.py.
"""

from flask import Blueprint, render_template

site_bp = Blueprint('site', __name__)


@site_bp.route('/inicio')
def inicio():
    return render_template('publico/inicio.html')