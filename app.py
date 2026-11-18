import os
from functools import wraps
import mysql.connector
from dotenv import load_dotenv
from flask import (
    Flask, flash, redirect, render_template,
    request, session, url_for
)
from werkzeug.security import check_password_hash

from banco import obter_conexao

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'chave-apenas-para-desenvolvimento')

TIPOS_SANGUINEOS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']


def login_obrigatorio(funcao):
    @wraps(funcao)
    def decorada(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Faça login para acessar o sistema.', 'erro')
            return redirect(url_for('login'))
        return funcao(*args, **kwargs)
    return decorada


def limpar_texto(valor):
    return valor.strip() if valor else ''


def dados_formulario():
    return {
        'nome': limpar_texto(request.form.get('nome')),
        'data_nascimento': request.form.get('data_nascimento', ''),
        'tipo_sanguineo': request.form.get('tipo_sanguineo', ''),
        'telefone': limpar_texto(request.form.get('telefone')),
        'email': limpar_texto(request.form.get('email')) or None,
        'cidade': limpar_texto(request.form.get('cidade')),
        'estado': limpar_texto(request.form.get('estado')).upper(),
        'ultima_doacao': request.form.get('ultima_doacao') or None,
        'consentimento': 1 if request.form.get('consentimento') == 'on' else 0
    }


def validar_doador(dados):
    erros = []
    if not dados['nome']:
        erros.append('Nome é obrigatório.')
    if not dados['data_nascimento']:
        erros.append('Data de nascimento é obrigatória.')
    if dados['tipo_sanguineo'] not in TIPOS_SANGUINEOS:
        erros.append('Selecione um tipo sanguíneo válido.')
    if not dados['telefone']:
        erros.append('Telefone é obrigatório.')
    if not dados['cidade']:
        erros.append('Cidade é obrigatória.')
    if len(dados['estado']) != 2:
        erros.append('Estado deve ter duas letras, por exemplo PI.')
    if not dados['consentimento']:
        erros.append('O consentimento é obrigatório para o cadastro.')
    return erros


@app.route('/')
def inicio():
    if 'admin_id' in session:
        return redirect(url_for('listar_doadores'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = limpar_texto(request.form.get('email')).lower()
        senha = request.form.get('senha', '')
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM administradores WHERE email = %s',
            (email,)
        )
        administrador = cursor.fetchone()
        cursor.close()
        conexao.close()
        if administrador and check_password_hash(administrador['senha_hash'], senha):
            session.clear()
            session['admin_id'] = administrador['id_administrador']
            session['admin_nome'] = administrador['nome']
            flash('Login realizado com sucesso.', 'sucesso')
            return redirect(url_for('listar_doadores'))
        flash('E-mail ou senha inválidos.', 'erro')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'sucesso')
    return redirect(url_for('login'))


@app.route('/doadores')
@login_obrigatorio
def listar_doadores():
    nome = limpar_texto(request.args.get('nome'))
    tipo = request.args.get('tipo_sanguineo', '')
    cidade = limpar_texto(request.args.get('cidade'))
    sql = 'SELECT * FROM doadores WHERE 1=1'
    parametros = []
    if nome:
        sql += ' AND nome LIKE %s'
        parametros.append(f'%{nome}%')
    if tipo in TIPOS_SANGUINEOS:
        sql += ' AND tipo_sanguineo = %s'
        parametros.append(tipo)
    if cidade:
        sql += ' AND cidade LIKE %s'
        parametros.append(f'%{cidade}%')
    sql += ' ORDER BY nome'
    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute(sql, parametros)
    doadores = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template(
        'lista.html',
        doadores=doadores,
        tipos=TIPOS_SANGUINEOS,
        filtros={'nome': nome, 'tipo': tipo, 'cidade': cidade}
    )


@app.route('/doadores/novo', methods=['GET', 'POST'])
@login_obrigatorio
def novo_doador():
    if request.method == 'POST':
        dados = dados_formulario()
        erros = validar_doador(dados)
        if erros:
            for erro in erros:
                flash(erro, 'erro')
            return render_template(
                'formulario.html', doador=dados,
                tipos=TIPOS_SANGUINEOS, titulo='Novo doador'
            )
        sql = '''
            INSERT INTO doadores
            (nome, data_nascimento, tipo_sanguineo, telefone,
             email, cidade, estado, ultima_doacao, consentimento)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        valores = (
            dados['nome'], dados['data_nascimento'], dados['tipo_sanguineo'],
            dados['telefone'], dados['email'], dados['cidade'], dados['estado'],
            dados['ultima_doacao'], dados['consentimento']
        )
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute(sql, valores)
        conexao.commit()
        cursor.close()
        conexao.close()
        flash('Doador cadastrado com sucesso.', 'sucesso')
        return redirect(url_for('listar_doadores'))
    return render_template(
        'formulario.html', doador=None,
        tipos=TIPOS_SANGUINEOS, titulo='Novo doador'
    )


@app.route('/doadores/<int:id_doador>')
@login_obrigatorio
def detalhes_doador(id_doador):
    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute(
        'SELECT * FROM doadores WHERE id_doador = %s',
        (id_doador,)
    )
    doador = cursor.fetchone()
    cursor.close()
    conexao.close()
    if not doador:
        flash('Doador não encontrado.', 'erro')
        return redirect(url_for('listar_doadores'))
    return render_template('detalhes.html', doador=doador)


@app.route('/doadores/<int:id_doador>/editar', methods=['GET', 'POST'])
@login_obrigatorio
def editar_doador(id_doador):
    if request.method == 'POST':
        dados = dados_formulario()
        erros = validar_doador(dados)
        if erros:
            dados['id_doador'] = id_doador
            for erro in erros:
                flash(erro, 'erro')
            return render_template(
                'formulario.html', doador=dados,
                tipos=TIPOS_SANGUINEOS, titulo='Editar doador'
            )
        sql = '''
            UPDATE doadores SET
                nome=%s, data_nascimento=%s, tipo_sanguineo=%s,
                telefone=%s, email=%s, cidade=%s, estado=%s,
                ultima_doacao=%s, consentimento=%s
            WHERE id_doador=%s
        '''
        valores = (
            dados['nome'], dados['data_nascimento'], dados['tipo_sanguineo'],
            dados['telefone'], dados['email'], dados['cidade'], dados['estado'],
            dados['ultima_doacao'], dados['consentimento'], id_doador
        )
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute(sql, valores)
        conexao.commit()
        cursor.close()
        conexao.close()
        flash('Cadastro atualizado com sucesso.', 'sucesso')
        return redirect(url_for('detalhes_doador', id_doador=id_doador))
    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute('SELECT * FROM doadores WHERE id_doador = %s', (id_doador,))
    doador = cursor.fetchone()
    cursor.close()
    conexao.close()
    if not doador:
        flash('Doador não encontrado.', 'erro')
        return redirect(url_for('listar_doadores'))
    return render_template(
        'formulario.html', doador=doador,
        tipos=TIPOS_SANGUINEOS, titulo='Editar doador'
    )


@app.route('/doadores/<int:id_doador>/excluir', methods=['POST'])
@login_obrigatorio
def excluir_doador(id_doador):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM doadores WHERE id_doador = %s', (id_doador,))
    conexao.commit()
    excluidos = cursor.rowcount
    cursor.close()
    conexao.close()
    if excluidos:
        flash('Doador excluído com sucesso.', 'sucesso')
    else:
        flash('Doador não encontrado.', 'erro')
    return redirect(url_for('listar_doadores'))


@app.errorhandler(mysql.connector.Error)
def erro_banco(erro):
    print(f'Erro do MySQL: {erro}')
    return render_template(
        'base.html', erro_geral='Não foi possível acessar o banco de dados.'
    ), 500


if __name__ == '__main__':
    app.run(debug=True)
