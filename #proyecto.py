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

class catedratico(Usuario):
    def __init__(self, carnet, nombre):
        super().__init__(carnet, nombre)
        self._cursos = set()

    
    def asigancion_catedratico(self, nombrecurso ):

        while True:
            if nombrecurso in self._cursos:
                print(f"El curso {nombrecurso} ya está asignado para el/ la catedrático  {self.nombre}.")
                nombrecurso = input("Ingrese un nuevo nombre de curso: ")
            else:
                self._cursos.add(nombrecurso)
                print(f"Curso {nombrecurso} asignado exitosamente al catedrático {self.nombre}.")
                break

class Curso:
    def __init__(self, nombre, nombre_catedratico):
        self.nombre = nombre
        self.nombre_catedratico = nombre_catedratico
        self._estudiantes = set()
        self.evaluaciones = {}


    def agregar_estudiante(self, carnet_estudiante):
       while True:
            if carnet_estudiante in self._estudiantes:
                print(f"El estudiante con carnet {carnet_estudiante} ya está inscrito en el curso {self.nombre}.")
                carnet_estudiante = input("Ingrese un nuevo carnet de estudiante: ")
            else:
                self._estudiantes.add(carnet_estudiante)
                print(f"Estudiante con carnet {carnet_estudiante} agregado al curso {self.nombre}.")
                break