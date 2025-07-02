from typing import Optional

from fastapi import FastAPI, Path, Query

base_de_datos = {
    "usuarios": {
        1: {
            "id": 1,
            "nombre": "María López",
            "email": "maria@example.com",
            "activo": True,
            "rol": "admin",
        },
        2: {
            "id": 2,
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "activo": True,
            "rol": "usuario",
        },
        3: {
            "id": 3,
            "nombre": "Ana García",
            "email": "ana@example.com",
            "activo": False,
            "rol": "usuario",
        },
        4: {
            "id": 4,
            "nombre": "Carlos Ruiz",
            "email": "carlos@example.com",
            "activo": True,
            "rol": "editor",
        },
    },
    "productos": {
        101: {
            "id": 101,
            "nombre": "Laptop",
            "categoria": "electrónica",
            "precio": 999.99,
            "stock": 15,
            "descuento": True,
        },
        102: {
            "id": 102,
            "nombre": "Libro Python",
            "categoria": "libros",
            "precio": 39.99,
            "stock": 42,
            "descuento": False,
        },
        103: {
            "id": 103,
            "nombre": "Smartphone",
            "categoria": "electrónica",
            "precio": 699.99,
            "stock": 8,
            "descuento": True,
        },
        104: {
            "id": 104,
            "nombre": "Monitor",
            "categoria": "electrónica",
            "precio": 249.99,
            "stock": 0,
            "descuento": False,
        },
    },
    "pedidos": {
        1001: {
            "id": 1001,
            "usuario_id": 2,
            "productos": [101, 102],
            "total": 1039.98,
            "estado": "completado",
        },
        1002: {
            "id": 1002,
            "usuario_id": 1,
            "productos": [103],
            "total": 699.99,
            "estado": "en_proceso",
        },
        1003: {
            "id": 1003,
            "usuario_id": 3,
            "productos": [101, 103, 104],
            "total": 1949.97,
            "estado": "cancelado",
        },
    },
}

app = FastAPI()

@app.get("/")
def read_root():
    return {"ok": True}

@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int = Path(..., title="ID del usuario", gt=0, example="1")):
    usuario = base_de_datos["usuarios"].get(usuario_id)
    if usuario == None:
        return {"error": "Usuario no encontrado"}
    return {"usuario": usuario}


@app.get("/productos/")
def buscar_productos(
    categoria: Optional[str] = Query(None, min_length=3),
    con_descuento: bool = Query(False),
    stock_minimo: int = Query(0, ge=0),
):
    resultados = []

    for producto in base_de_datos["productos"].values():
        if categoria and producto["categoria"] != categoria:
            continue
        if con_descuento and not producto["descuento"]:
            continue
        if producto["stock"] < stock_minimo:
            continue

        resultados.append(producto)
    
    return { "productos": resultados }

