from typing import TypeVar, Type
from enum import Enum

E = TypeVar('E', bound=Enum)

def leer_texto(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print(">> Error: El campo no puede estar vacío.")

def leer_opcional_texto(prompt: str, valor_actual: str) -> str:
    val = input(f"{prompt} [{valor_actual}]: ").strip()
    return val if val else valor_actual

def leer_entero(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print(">> Error: Ingrese un número entero válido.")

def leer_opcional_entero(prompt: str, valor_actual: int) -> int:
    while True:
        val = input(f"{prompt} [{valor_actual}]: ").strip()
        if not val:
            return valor_actual
        try:
            return int(val)
        except ValueError:
            print(">> Error: Ingrese un número entero válido.")

def leer_flotante(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print(">> Error: Ingrese un número decimal válido.")

def leer_opcional_flotante(prompt: str, valor_actual: float) -> float:
    while True:
        val = input(f"{prompt} [{valor_actual:.2f}]: ").strip()
        if not val:
            return valor_actual
        try:
            return float(val)
        except ValueError:
            print(">> Error: Ingrese un número decimal válido.")

def leer_enum(enum_cls: Type[E], titulo: str) -> E:
    opciones = list(enum_cls)
    print(f"--- Seleccionar {titulo} ---")
    for idx, op in enumerate(opciones, start=1):
        print(f"{idx}. {op.name}")
    while True:
        eleccion = leer_entero("Seleccione una opción: ")
        if 1 <= eleccion <= len(opciones):
            return opciones[eleccion - 1]
        print(">> Opción fuera de rango.")

def confirmar_accion(prompt: str) -> bool:
    resp = input(f"{prompt} (S/N): ").strip().upper()
    return resp == 'S'