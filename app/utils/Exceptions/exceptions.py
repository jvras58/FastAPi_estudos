from fastapi import HTTPException, status


def credentials_exception():
    """
    Representa um erro de validação de credencial do usuário.
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possível validar as credenciais',
        headers={'WWW-Authenticate': 'Bearer'},
    )


def is_not_validation_adm_exception():
    """
    Representa um erro de validação de credencial do usuário adm .
    """
    return HTTPException(
        status_code=403,
        detail='Permissão negada. Somente administradores podem acessar esta rota.',
    )


def is_not_adm_exception():
    """
    Representa um erro de falta de privilegios do usuário adm .
    """
    return HTTPException(
        status_code=404,
        detail='Usuário com privilegios de adm não encontrado',
    )


def sem_permissao_exception():
    """
    Representa um erro de falta de permissão .
    """
    return HTTPException(
        status_code=403,
        detail='Usuário não tem permissão para realizar essa ação',
    )


def senha_antiga_incorreta_exception():
    """
    Representa um erro de senha antiga incorreta .
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Senha antiga incorreta',
    )


def senha_vazia_exception():
    """
    Representa um erro de senha vazia .
    """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Nova senha não pode ser vazia',
    )


def user_not_found_exception():
    """
    Representa um erro de não encontrado .
    """
    return HTTPException(status_code=404, detail='Usuário não encontrado')


def usertipo_not_found_exception():
    """
    Representa um erro de não encontrado .
    """
    return HTTPException(
        status_code=404, detail='tipo de usuario não encontrado'
    )


def email_ja_registrado_exception():
    """
    Representa um erro de email já registrado .
    """
    return HTTPException(status_code=400, detail='E-mail já registrado')


def usuario_nao_encontrado_ou_nao_autenticado_exception():
    """
    Representa um erro de user não autenticado ou não encontrado .
    """
    return HTTPException(
        status_code=400, detail='Usuário não encontrado ou não autenticado'
    )


def area_nao_encontrada_exception():
    """
    Representa um erro de area não encontrada .
    """
    return HTTPException(
        status_code=404, detail='Area não existe ou não encontrada'
    )


def area_existente_exception():
    """
    Representa um erro de area já existente .
    """
    return HTTPException(status_code=409, detail='Área já existe')


def reserva_nao_encontrada_exception():
    """
    Representa um erro de reserva não encontrada .
    """
    return HTTPException(
        status_code=404, detail='Reserva não existe ou encontrada'
    )


def reserva_choque_horario_exception():
    """
    Representa um erro de choque de hora para area escolhida .
    """
    return HTTPException(
        status_code=400, detail='Horário indiponível para essa Área'
    )


def Incorrect_username_or_password():
    """
    Representa um erro de acesso ao token por Incorrect username ou password .
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Usuário ou senha incorretos',
        headers={'WWW-Authenticate': 'Bearer'},
    )


def Unauthorized():
    """
    Representa um erro de acesso ao token por Incorrect username ou password .
    """
    return HTTPException(
        status_code=status.HTTP_STATUS.HTTP_401_UNAUTHORIZED,
        detail='Unauthorized',
    )


class ObjectNotFoundException(Exception):
    """
    Representa um erro quando o usuário com determinado ID não é encontrado.
    """

    def __init__(self, obj_type: str, obj_id: str):
        super().__init__(f'{obj_type} with ID [{obj_id}] not found')


class IntegrityValidationException(Exception):
    """
    Representa um erro de validação de integridade de dados.
    """

    def __init__(self, exc_msg: str):
        super().__init__(exc_msg)
