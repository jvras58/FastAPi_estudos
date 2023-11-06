class DadosTeste_usuario:
    @staticmethod
    def tipo_usuario_adm():
        return {
            'id': 1,
            'tipo': 'administrador',
        }

    @staticmethod
    def tipo_usuario_cliente():
        return {
            'id': 2,
            'tipo': 'cliente',
        }

    @staticmethod
    def usuario_adm():
        return {
            'nome': 'adm test',
            'tipo_id': 1,
            'email': 'adm.test@example.com',
            'senha': 'senhaadm',
        }

    @staticmethod
    def usuario_cliente():
        return {
            'nome': 'cliente test',
            'tipo_id': 2,
            'email': 'cliente.test@example.com',
            'senha': 'senhacliente',
        }

    @staticmethod
    def login_token_adm():
        return {'usarname': 'adm.test@example.com', 'password': 'senhaadm'}

    @staticmethod
    def login_token_cliente():
        return {
            'usarname': 'cliente.test@example.com',
            'password': 'senhacliente',
        }


class DadosTeste_area:
    @staticmethod
    def area_id_adm():
        return {
            'id': 5,
            'nome': 'Quadra de volei',
            'descricao': 'Uma quadra de volei espaçosa',
            'iluminacao': 'LED',
            'tipo_piso': 'Liso',
            'covered': 'Sim',
            'foto_url': 'https://example.com/quadra_volei.jpg',
            'usuario_id': 3,
        }

    @staticmethod
    def area_id_cliente():
        return {
            'id': 6,
            'nome': 'Quadra de volei2',
            'descricao': 'Uma quadra de volei espaçosa2',
            'iluminacao': 'LED1',
            'tipo_piso': 'Liso2',
            'covered': 'Sim',
            'foto_url': 'https://example.com/quadra_volei.jpg',
            'usuario_id': 4,
        }


class DadosTeste_reserva:
    @staticmethod
    def reserva_id_adm():
        return {
            'id': 7,
            'valor': 10,
            'reserva_data': '2023-10-23T12:00:00',
            'hora_inicio': '2023-10-23T15:00:00',
            'hora_fim': '2023-10-23T16:00:00',
            'justificacao': 'Jogo de Equipe',
            'reserva_tipo': 'Jogo',
            'status': 'Em análise',
            'area_id': 5,
            'usuario_id': 3,
        }

    @staticmethod
    def reserva_id_cliente():
        return {
            'id': 8,
            'valor': 10,
            'reserva_data': '2023-10-23T15:00:00',
            'hora_inicio': '2023-10-23T16:00:00',
            'hora_fim': '2023-10-23T17:00:00',
            'justificacao': 'Jogo de Equipe',
            'reserva_tipo': 'Jogo',
            'status': 'Em análise',
            'area_id': 5,
            'usuario_id': 4,
        }

    @staticmethod
    def reserva_id_cliente_cliente_tenta_criar_area():
        return {
            'id': 8,
            'valor': 10,
            'reserva_data': '2023-10-23T15:00:00',
            'hora_inicio': '2023-10-23T16:00:00',
            'hora_fim': '2023-10-23T17:00:00',
            'justificacao': 'Jogo de Equipe',
            'reserva_tipo': 'Jogo',
            'status': 'Em análise',
            'area_id': 6,
            'usuario_id': 4,
        }
