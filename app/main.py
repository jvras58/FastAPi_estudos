from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# areas
from app.area.area_controller import router_area as area_control

# reservas
from app.reserva.reserva_controller import router_reserva as reserva_control

# tipo usuario
from app.tipo_usuario.tipo_usuario_controller import (
    router_tipo_usuario as user_tipo,
)

# usuario
from app.usuario.usuario_controller import router_usuario as user_control

# uvicorn app.main:app --reload  <-- inicia o servidor

app = FastAPI(
    title='Reservations - API',
    description='Applicação backend de uma API para gerenciamento de reservas de áreas.',
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


@app.get('/')
def read_root():
    return {'Hello': 'World'}


# ----------------------------------------- tipo_usuario -------------------------------------------------------#
app.include_router(user_tipo, tags=['tipo_usuario'])

# ----------------------------------------- usuario -------------------------------------------------------#
app.include_router(user_control, tags=['Usuarios'])

# ----------------------------------------- area -------------------------------------------------------#
app.include_router(area_control, tags=['Areas'])

# ----------------------------------------- reserva -------------------------------------------------------#
app.include_router(reserva_control, tags=['Reservas'])
