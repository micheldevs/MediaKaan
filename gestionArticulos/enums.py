from enum import Enum

# Enumeraciones para algunos campos de los modelos

class AccionType(Enum):
    INTERCAMBIO="INTERCAMBIO"
    DONO="DONO"
    COMPARTO="COMPARTO"

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)

class CategoriaType(Enum):
    PELICULAS="Películas"
    SERIES="Series"
    VIDEOJUEGOS="Videojuegos"
    COMICS="Cómics"
    LIBROS="Libros"
    MUSICA="Música"

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)