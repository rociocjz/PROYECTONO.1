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
    def __init__(self, nombre, catedratico):
        self.nombre = nombre
        self.catedratico = catedratico
        self._estudiantes = set()
        self.evaluaciones = {}


    def agregar_estudiante(self, carnet_estudiante):
       if carnet_estudiante in self._estudiantes:
           raise Exception(f"El estudiante con carnet {carnet_estudiante} ya está inscrito en el curso {self.nombre}.")
       self._estudiantes.add(carnet_estudiante)
       
    def agregar_evaluacion(self, evaluacion):
         if evaluacion.nombre_examen in self.evaluaciones:
              raise Exception(f"La evaluación {evaluacion.nombre_examen} ya existe en el curso {self.nombre}.")
         self.evaluaciones[evaluacion.nombre_examen] = evaluacion
       
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
        pass

class Examen(Evaluacion):
    def __init__(self, nombre_examen, puntaje):
        super().__init__(nombre_examen, "Examen", puntaje)

    def registrar_calificacion(self, carnet_estudiante, nota):
        if nota < 0 or nota > self.puntaje:
            raise Exception(f"La nota deberia de ser entre 0 y {self.puntaje}.")
        self.calificaciones[carnet_estudiante] = nota
        print(f"Calificación {nota}, estudiante {carnet_estudiante}, examen {self.nombre_examen}.")

class Tarea(Evaluacion):
    def __init__(self, nombre_examen, puntaje):
        super().__init__(nombre_examen, "Tarea", puntaje)

    def registrar_calificacion(self, carnet_estudiante, nota):
        if nota < 0 or nota > self.puntaje:
            raise Exception(f"La nota debe de ser entre 0 y {self.nombre_examen}.")
        self.calificaciones[carnet_estudiante] = nota
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
        
        catedratico = self.usuarios[carnet_catedratico]
        nuevo_curso = Curso(nombre_curso, catedratico    )
        self.cursos[nombre_curso] = nuevo_curso
        
        catedratico.asigancion_catedratico(nombre_curso)    

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
        self.cursos[nombre_curso].agregar_evaluacion(evaluacion)
        
    def registrar_calificacion(self, nombre_curso, nombre_evaluacion, carnet_estudiante, nota):
        if nombre_curso not in self.cursos:
            raise Exception(f"No se encontró el curso.")
        curso = self.cursos[nombre_curso]
        if nombre_evaluacion not in curso.evaluaciones:
            raise Exception(f"No se encontró la evaluación {nombre_evaluacion} en el curso {nombre_curso}.")
        curso.evaluaciones[nombre_evaluacion].registrar_calificacion(carnet_estudiante, nota)

    def generar_reporte_curso(self, nombre_curso):
        
        if nombre_curso not in self.cursos:
            raise Exception(f"No se encontró el curso.")
        curso = self.cursos[nombre_curso]
        print(f"Reporte del curso: {nombre_curso}")
        for carnet in curso._estudiantes:
            estudiante = self.usuarios[carnet]
            notas = []
            for evaluacion in curso.evaluaciones.values():
                if carnet in evaluacion.calificaciones:
                    notas.append(evaluacion.calificaciones[carnet])
            if notas:
                promedio = sum(notas) / len(notas)
                estado = "REPORBADO, ESTUDIANTE CON PROMEDIO MUY BAJO" if promedio < 60 else "APROBADO"
                print(f"Estudiante: {estudiante.nombre} ({carnet}): Promedio = {promedio:.2f}-{estado}")
            else:
                print(f"Estudiante: {estudiante.nombre} ({carnet}): No tiene notas registradas.")
def menu():
    sistema = Sistema()
    while True:
        print("\n--- Menú del Sistema de Gestión Académica ---")
        print("1. Agregar Estudiante")
        print("2. Agregar Catedrático")
        print("3. Agregar Curso")
        print("4. Inscribir Estudiante en Curso")
        print("5. Agregar Evaluación a Curso")
        print("6. Registrar Calificación")
        print("7. Generar Reporte de Curso")
        print("8. Salir")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                carnet = input("Ingrese el carnet del estudiante: ")
                nombre = input("Ingrese el nombre del estudiante: ")
                sistema.agregar_usuario(Estudiante(carnet, nombre))
                print(f"Estudiante agregado exitosamente.")


            elif opcion == "2":
                carnet = input("Ingrese el carnet del catedrático: ")
                nombre = input("Ingrese el nombre del catedrático: ")
                sistema.agregar_usuario(Catedratico(carnet, nombre))
                print(f"Catedrático {nombre} agregado exitosamente.")   

            elif opcion == "3":
                nombre_curso = input("Ingrese el nombre del curso: ")
                carnet_catedratico = input("Ingrese el carnet del catedrático : ")
                sistema.agregar_curso(nombre_curso, carnet_catedratico)

            elif opcion == "4":
                carnet_estudiante = input("Ingrese el carnet del estudiante: ")
                nombre_curso = input("Ingrese el nombre del curso: ")
                sistema.inscribir_estudiante(carnet_estudiante, nombre_curso)
            
            elif opcion == "5":
                nombre_curso = input("Ingrese el nombre del curso: ")
                tipo = input("Ingrese el tipo de evaluación (Examen/Tarea): ")
                nombre_evaluacion = input("Ingrese el nombre de la evaluación: ")
                puntaje = float(input("Ingrese el puntaje máximo de la evaluación: "))
                sistema.agregar_evaluacion_a_curso(nombre_curso, tipo, nombre_evaluacion, puntaje)
                
            elif opcion == "6":
                nombre_curso = input("Ingrese el nombre del curso: ")
                nombre_evaluacion = input("Ingrese el nombre de la evaluación: ")
                carnet_estudiante = input("Ingrese el carnet del estudiante: ")
                nota = float(input("Ingrese la calificación: "))
                sistema.registrar_calificacion(nombre_curso, nombre_evaluacion, carnet_estudiante, nota)
            
            elif opcion == "7":
                nombre_curso = input("Ingrese el nombre del curso: ")
                sistema.generar_reporte_curso(nombre_curso)

            elif opcion == "8":
                print("Saliendo del sistema... nos vemos pronto! ")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

        
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    menu()