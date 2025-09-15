from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, carnet, nombre):
        self.carnet = carnet
        self.nombre = nombre
       

    @property
    def carnet(self):
        return self._carnet
    @property
    def nombre(self):
        return self._nombre
    
class Estudiante(Usuario):
    def __init__(self, carnet, nombre):
        super().__init__(carnet, nombre)
        self._cursos = set()

    
    def asigancion(self, nombrecurso ):

        while True:
            if nombrecurso in self._cursos:
                print(f"El curso {nombrecurso} ya está asignado para el/ la estudiante  {self.nombre}.")
                nombrecurso = input("Ingrese un nuevo nombre de curso: ")
            else:
                self._cursos.add(nombrecurso)
                print(f"Curso {nombrecurso} asignado exitosamente al estudiante {self.nombre}.")
                break

    