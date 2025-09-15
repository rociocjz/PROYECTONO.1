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