from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, carnet, nombre):
        self._carnet = carnet
        self._nombre = nombre
       

    @property
    def carnet(self):
        return self._carnet
    @property
    def nombre(self):
        return self._nombre
    
class Estudiante(Usuario):
    def __init__(self, carnet, nombre):
        super().__init__(carnet, nombre)
        self._cursos_asignados = set()

    
    def asignacion(self, nombrecurso ):

        while True:
            if nombrecurso in self._cursos_asignados:
                print(f"El curso {nombrecurso} ya está asignado para el/ la estudiante  {self.nombre}.")
                nombrecurso = input("Ingrese un nuevo nombre de curso: ")
            else:
                self._cursos_asignados.add(nombrecurso)
                print(f"Curso {nombrecurso} asignado exitosamente al estudiante {self.nombre}.")
                break

class Catedratico(Usuario):
    def __init__(self, carnet, nombre):
        super().__init__(carnet, nombre)
        self.cursos = set()

    
    def asigancion_catedratico(self, nombrecurso ):

        while True:
            if nombrecurso in self.cursos :
                print(f"El curso {nombrecurso} ya está asignado para el/ la catedrático  {self.nombre}.")
                nombrecurso = input("Ingrese un nuevo nombre de curso: ")
            else:
                self.cursos.add(nombrecurso)
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
    def agregar_evaluacion(self, curso_evaluacion):
        if curso_evaluacion in self.evaluaciones:
            print(f"La evaluación {curso_evaluacion} ya se ha creado para el curso {self.nombre}.")
        else:
            self.evaluaciones[curso_evaluacion] = {}
            print(f"Evaluación {curso_evaluacion} agregada al curso {self.nombre}.")

class Evaluacion(ABC):
    def __init__(self, nombre_examen,tipo, puntaje):
        self.nombre_examen = nombre_examen
        self.tipo = tipo
        self.puntaje = puntaje
        self.calificaciones = {}

    @property
    def nombre_examen(self):
        return self._nombre_examen
    
    @abstractmethod
    def registrar_calificacion(self, carnet_estudiante, nota):
        if nota < 0 or nota > self.puntaje:
            raise ValueError(f"La calificación debe estar entre 0 y 100.")
        self.calificaciones[carnet_estudiante] = nota

    
    