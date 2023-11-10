from fastapi import HTTPException, status


def credentials_exception():
    """
    Representa um erro de validação de credencial do usuário.
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
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


def user_not_found_exception():
    """
    Representa um erro de falta de usuario .
    """
    return HTTPException(status_code=404, detail='User not found')


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


def user_not_found1_exception():
    """
    Representa um erro de senha vazia .
    """
    return HTTPException(status_code=404, detail='Usuário não encontrado')


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
    return HTTPException(status_code=400, detail='Area não existe')


def area_not_found_exception():
    """
    Representa um erro de area não encontrada .
    """
    return HTTPException(status_code=404, detail='Area not found')


def area_existente_exception():
    """
    Representa um erro de area já existente .
    """
    return HTTPException(status_code=400, detail='Área já existe')


def reserva_nao_encontrada_exception():
    """
    Representa um erro de reserva não encontrada .
    """
    return HTTPException(status_code=404, detail='Reservation not found')


def reserva_choque_horario_exception():
    """
    Representa um erro de choque de hora para area escolhida .
    """
    return HTTPException(
        status_code=400, detail='Horário indiponível para essa Área'
    )
