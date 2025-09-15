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

       if nombrecurso in self._cursos_asignados :
           raise Exception(f"El curso {nombrecurso} ya está asignado para el estudiante {self.nombre}.")
       self._cursos_asignados.add(nombrecurso)
       print(f"Curso {nombrecurso} asignado exitosamente al estudiante {self.nombre}")

class Catedratico(Usuario):
    def __init__(self, carnet, nombre):
        super().__init__(carnet, nombre)
        self.cursos = set()

    
    def asigancion_catedratico(self, nombrecurso ):
       self.cursos.add(nombrecurso)
       print(f"Curso {nombrecurso} asignado exitosamente al catedrático {self.nombre}")
class Curso:
    def __init__(self, nombre, nombre_catedratico):
        self.nombre = nombre
        self.nombre_catedratico = nombre_catedratico
        self._estudiantes = set()
        self.evaluaciones = {}


    def agregar_estudiante(self, carnet_estudiante):
       if carnet_estudiante in self._estudiantes:
           raise Exception(f"El estudiante con carnet {carnet_estudiante} ya está inscrito en el curso {self.nombre}.")
       self._estudiantes.add(carnet_estudiante)
       
    def agregar_evaluacion(self, curso_evaluacion):
         if curso_evaluacion in self.evaluaciones:
              raise Exception(f"La evaluación {curso_evaluacion} ya existe en el curso {self.nombre}.")
         self.evaluaciones[curso_evaluacion] = None
       
class Evaluacion(ABC):
    def __init__(self, nombre_examen,tipo, puntaje):
        self._nombre_examen = nombre_examen
        self._tipo = tipo
        self._puntaje = puntaje
        self.calificaciones = {}

    @property
    def nombre_examen(self):
        return self._nombre_examen
    
    @property
    def tipo(self):
        return self._tipo
    
    @property
    def puntaje(self):
        return self._puntaje
    
    
    @abstractmethod
    def registrar_calificacion(self, carnet_estudiante, nota):
        if nota < 0 or nota > self.puntaje:
            raise ValueError(f"La calificación debe estar entre 0 y 100.")
        self.calificaciones[carnet_estudiante] = nota

class Examen(Evaluacion):
    def __init__(self, nombre_examen, puntaje):
        super().__init__(nombre_examen, "Examen", puntaje)

    def registrar_calificacion(self, carnet_estudiante, nota):
        super().registrar_calificacion(carnet_estudiante, nota)
        print(f"Calificación {nota}, estudiante {carnet_estudiante}, examen {self.nombre_examen}.")

class Tarea(Evaluacion):
    def __init__(self, nombre_examen, puntaje):
        super().__init__(nombre_examen, "Tarea", puntaje)

    def registrar_calificacion(self, carnet_estudiante, nota):
        super().registrar_calificacion(carnet_estudiante, nota)
        print(f"Calificación {nota}, estudiante {carnet_estudiante}, tarea {self.nombre_examen}.")

class Sistema:
    def __init__(self):
        self.usuarios = {}
        self.cursos = {}

    def agregar_usuario(self, usuario):
        if usuario.carnet in self.usuarios:
            raise Exception(f"El usuario con carnet {usuario.carnet} ya existe.")
        self.usuarios[usuario.carnet] = usuario
        
    def agregar_curso(self, nombre_curso, carnet_catedratico):
        if nombre_curso in self.cursos:
            raise Exception(f"El curso {nombre_curso} ya existe.")
        if carnet_catedratico not in self.usuarios or not isinstance(self.usuarios[carnet_catedratico], Catedratico):
            raise Exception(f"No se encontró un catedrático con carnet {carnet_catedratico}.")
        
       
        nuevo_curso = Curso(nombre_curso, carnet_catedratico    )
        self.cursos[nombre_curso] = nuevo_curso
        self.usuarios[carnet_catedratico].asigancion_catedratico(nombre_curso)
        print(f"Curso {nombre_curso} agregado exitosamente con catedrático {self.usuarios[carnet_catedratico].nombre}.")

    def inscribir_estudiante(self, carnet_estudiante, nombre_curso):
        if carnet_estudiante not in self.usuarios or not isinstance(self.usuarios[carnet_estudiante], Estudiante):
            raise Exception(f"No se encontró un estudiante con carnet {carnet_estudiante}.")
        if nombre_curso not in self.cursos:
            raise Exception(f"No se encontró el curso {nombre_curso}.")
        
        self.cursos[nombre_curso].agregar_estudiante(carnet_estudiante)
        self.usuarios[carnet_estudiante].asignacion(nombre_curso)
        print(f"Estudiante {self.usuarios[carnet_estudiante].nombre} inscrito exitosamente en el curso {nombre_curso}.")

      
    def agregar_evaluacion_a_curso(self, nombre_curso, tipo, *args, **kwargs ):
        if nombre_curso not in self.cursos:
            raise Exception(f"No se encontró el curso.")
        if tipo.lower() == "examen":
            evaluacion = Examen(*args, **kwargs)
        elif tipo.lower() == "tarea":
            evaluacion = Tarea(*args, **kwargs)
        else:
            raise Exception("Tipo de evaluación no válido. Use 'Examen' o 'Tarea'.")
        self.cursos[nombre_curso].evaluaciones[evaluacion.nombre_examen] = evaluacion
        
    def registrar_calificacion(self, nombre_curso, nombre_evaluacion, carnet_estudiante, nota):
        if nombre_curso not in self.cursos:
            raise Exception(f"No se encontró el curso.")
        curso = self.cursos[nombre_curso]
        if nombre_evaluacion not in curso.evaluaciones:
            raise Exception(f"No se encontró la evaluación {nombre_evaluacion} en el curso {nombre_curso}.")
        curso.evaluaciones[nombre_evaluacion].registrar_calificacion(carnet_estudiante, nota)

    def generar_reporte_curso(self, nombre_curso):
        print(f"Reporte del curso: {nombre_curso}")
        for curso in self.cursos.values():
            for estudiante in curso._estudiantes:
                notas = []
                for evaluacion in curso.evaluaciones.values():
                    if estudiante in evaluacion.calificaciones:
                        notas.append(evaluacion.calificaciones[estudiante])
                if notas:
                    promedio = sum(notas) / len(notas)
                    if promedio < 60:
                        print(f"Estudiante {estudiante} tiene un promedio de {promedio:.2f} - REPROBADO TIENE RENDIMIENTO MUY BAJO")
