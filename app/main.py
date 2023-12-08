# import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# areas
from app.api.area.area_router import router_area as area_control

# autenticação
from app.api.auth.auth_router import router_auth as auth_token

# reservas
from app.api.reserva.reserva_router import router_reserva as reserva_control

# tipo usuario
from app.api.tipo_usuario.tipo_usuario_router import (
    router_tipo_usuario as user_tipo,
)

# usuario
from app.api.usuario.usuario_router import router_usuario as user_control

# from app.init_db import init_db

# uvicorn app.main:app --reload  <-- inicia o servidor

app = FastAPI(
    title='Reservations - API',
    description='Aplicação backend de uma API para gerenciamento de reservas de áreas.',
    summary='Aplicação desenvolvida para estudos de backend com FastAPI.',
    version='0.0.0',
)


origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', tags=['Hello World'])
def read_root():
    return {'Hello': 'World'}


app.include_router(user_tipo, tags=['tipo_usuario'])

app.include_router(user_control, tags=['Usuarios'])

app.include_router(auth_token, tags=['Autenticação'])

app.include_router(area_control, tags=['Areas'])

app.include_router(reserva_control, tags=['Reservas'])


# @app.on_event('startup')
# async def startup_event():
#     try:
#         init_db()
#     except Exception as e:
#         logging.error(f'banco offline: {e}')
