"""
Rotas das páginas do site (parte visual).

- Usam somente dados de exemplo (dados_exemplo.py).
- Não acessam o banco de dados.
- Não alteram o CRUD de doadores do app.py.
"""

from flask import Blueprint, abort, render_template, request

from dados_exemplo import CAMPANHAS, LOCAIS, buscar_campanha, buscar_local

site_bp = Blueprint('site', __name__)


@site_bp.route('/inicio')
def inicio():
    return render_template(
        'publico/inicio.html',
        campanhas=CAMPANHAS[:3],
        locais=LOCAIS
    )


@site_bp.route('/campanhas')
def campanhas():
    return render_template('publico/campanhas.html', campanhas=CAMPANHAS)


@site_bp.route('/campanhas/<int:id_campanha>')
def campanha_detalhe(id_campanha):
    campanha = buscar_campanha(id_campanha)
    if campanha is None:
        abort(404)
    return render_template('publico/campanha_detalhe.html', campanha=campanha)


@site_bp.route('/locais')
def locais():
    return render_template('publico/locais.html', locais=LOCAIS)


@site_bp.route('/locais/<int:id_local>')
def local_detalhe(id_local):
    local = buscar_local(id_local)
    if local is None:
        abort(404)
    campanhas_do_local = [
        campanha for campanha in CAMPANHAS
        if campanha['local'] == local['nome']
    ]
    return render_template(
        'publico/local_detalhe.html',
        local=local,
        campanhas=campanhas_do_local
    )


@site_bp.route('/autocadastro', methods=['GET', 'POST'])
def autocadastro():
    if request.method == 'POST':
        # Demonstração: nada é salvo. Só mostramos a página de confirmação.
        nome = request.form.get('nome', '').strip()
        return render_template('publico/confirmacao.html', nome=nome)
    return render_template('publico/autocadastro.html')