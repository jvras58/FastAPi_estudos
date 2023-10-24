from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#tipo usuario
from app.tipo_usuario.tipo_usuario_controller import router_tipo_usuario as user_tipo
#usuario
from app.usuario.usuario_controller import router_usuario as user_control
# reservas
from app.reserva.reserva_controller import router_reserva as reserva_control
# areas
from app.area.area_controller import router_area as area_control


# uvicorn app.main:app --reload  <-- inicia o servidor

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# ----------------------------------------- tipo_usuario -------------------------------------------------------#
app.include_router(user_tipo)

# ----------------------------------------- usuario -------------------------------------------------------#
app.include_router(user_control)

# ----------------------------------------- area -------------------------------------------------------#
app.include_router(area_control)

# ----------------------------------------- reserva -------------------------------------------------------#
app.include_router(reserva_control)