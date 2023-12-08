from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    """
    Representa um erro de validação de credencial do usuário.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Não foi possível validar as credenciais',
            headers={'WWW-Authenticate': 'Bearer'},
        )


class sem_permissao_exception(HTTPException):
    """
    Representa um erro de falta de permissão.
    """

    def __init__(self):
        super().__init__(
            status_code=403,
            detail='Usuário não tem permissão para realizar essa ação',
        )


class Permission_Exception(HTTPException):
    """
    Representa um erro de falta de permissão.
    """

    def __init__(self):
        super().__init__(
            status_code=403,
            detail='Usuário não tem permissão nenhuma',
        )


class IncorrectOldPasswordException(HTTPException):
    """
    Representa um erro de senha antiga incorreta.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Senha antiga incorreta',
        )


class EmptyPasswordException(HTTPException):
    """
    Representa um erro de senha vazia.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Nova senha não pode ser vazia',
        )


# TODO: provavelmente isso vai deve ser transformado em um exception que nem os outros
class UserNotFoundException(HTTPException):
    """
    Representa um erro de usuário não encontrado.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )


# TODO: provavelmente isso vai deve ser transformado em um exception que nem os outros
class EmailAlreadyRegistered(HTTPException):
    """
    Representa um erro de email já registrado.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='E-mail já registrado',
        )


class Incorrect_username_or_password(HTTPException):
    """
    Representa um erro de acesso ao token por Incorrect username ou password.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )


class ObjectAlreadyExistException(Exception):
    """
    Representa um erro quando se tentar cadastrar um usuário com o mesmo username.
    """

    def __init__(self, obj_type: str, obj_id: str):
        super().__init__(f'Object {obj_type} already exist with id [{obj_id}]')


class ObjectNotFoundException(Exception):
    """
    Representa um erro quando o usuário com determinado ID não é encontrado.
    """

    def __init__(self, obj_type: str, obj_id: str):
        super().__init__(f'{obj_type} with ID [{obj_id}] not found')


class ObjectConflitException(Exception):
    """
    Representa um erro quando um objeto entra em conflito com outro
    """

    def __init__(self, obj_type: str, obj_id: str):
        super().__init__(
            f'{obj_type} with ID [{obj_id}] conflict availability'
        )


class PermissionException(Exception):
    """
    Representa um erro quando uma permissão está ausente
    """

    def __init__(self, obj_type: str):
        super().__init__(f'{obj_type} conflict permission')
