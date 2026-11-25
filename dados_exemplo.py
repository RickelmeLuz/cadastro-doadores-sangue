"""
Dados de exemplo usados nas páginas do site.
Todos os dados são fictícios. 
"""

CAMPANHAS = [
    {
        'id': 1,
        'nome': 'Doe Sangue, Compartilhe Vida',
        'descricao': 'Campanha fictícia de incentivo à doação de sangue.',
        'data_inicio': '01/12/2026',
        'data_fim': '31/12/2026',
        'local': 'Hemocentro Central',
        'cidade': 'Teresina',
        'estado': 'PI',
        'tipo_prioritario': 'O+',
        'vagas': 50,
        'status': 'ATIVA',
        'parceiro': {
            'nome': 'Restaurante Parceiro',
            'descricao': 'Estabelecimento fictício que apoia a campanha.',
            'promocao': 'Benefício promocional informado pelo parceiro',
            'periodo': '01/12/2026 a 31/12/2026',
            'regras': 'Regras fictícias informadas pelo parceiro, sujeitas à disponibilidade.',
        },
    },
    {
        'id': 2,
        'nome': 'Natal Solidário',
        'descricao': 'Mutirão fictício de fim de ano em pontos de coleta da cidade.',
        'data_inicio': '10/12/2026',
        'data_fim': '20/12/2026',
        'local': 'Posto de Coleta Norte',
        'cidade': 'Teresina',
        'estado': 'PI',
        'tipo_prioritario': None,
        'vagas': 30,
        'status': 'ATIVA',
        'parceiro': None,
    },
    {
        'id': 3,
        'nome': 'Doe com um amigo',
        'descricao': 'Campanha fictícia de janeiro, aprovada e aguardando o início.',
        'data_inicio': '05/01/2027',
        'data_fim': '30/01/2027',
        'local': 'Hemocentro Central',
        'cidade': 'Teresina',
        'estado': 'PI',
        'tipo_prioritario': 'A-',
        'vagas': 40,
        'status': 'APROVADA',
        'parceiro': None,
    },
    {
        'id': 4,
        'nome': 'Junho Solidário',
        'descricao': 'Campanha fictícia já encerrada, mantida como exemplo de histórico.',
        'data_inicio': '01/06/2026',
        'data_fim': '30/06/2026',
        'local': 'Hemocentro Central',
        'cidade': 'Teresina',
        'estado': 'PI',
        'tipo_prioritario': None,
        'vagas': 60,
        'status': 'ENCERRADA',
        'parceiro': None,
    },
]

LOCAIS = [
    {
        'id': 1,
        'nome': 'Hemocentro Central',
        'endereco': 'Endereço fictício, 100',
        'cidade': 'Teresina',
        'estado': 'PI',
        'telefone': '(86) 3000-0000',
        'horario': 'Segunda a sexta, das 8h às 17h',
        'status': 'ATIVO',
    },
    {
        'id': 2,
        'nome': 'Posto de Coleta Norte',
        'endereco': 'Endereço fictício, 250',
        'cidade': 'Teresina',
        'estado': 'PI',
        'telefone': '(86) 3000-0001',
        'horario': 'Segunda a sábado, das 8h às 12h',
        'status': 'ATIVO',
    },
    {
        'id': 3,
        'nome': 'Posto de Coleta Leste',
        'endereco': 'Endereço fictício, 45',
        'cidade': 'Teresina',
        'estado': 'PI',
        'telefone': '(86) 3000-0002',
        'horario': 'Atendimento suspenso no momento',
        'status': 'INATIVO',
    },
]


def buscar_campanha(id_campanha):
    for campanha in CAMPANHAS:
        if campanha['id'] == id_campanha:
            return campanha
    return None


def buscar_local(id_local):
    for local in LOCAIS:
        if local['id'] == id_local:
            return local
    return None