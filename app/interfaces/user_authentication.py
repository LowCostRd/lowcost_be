from abc import ABC,abstractmethod

class UserAuthentication(ABC):
    @abstractmethod
    def registration(self,data:dict)-> dict:
        pass