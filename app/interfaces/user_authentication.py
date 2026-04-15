from abc import ABC,abstractmethod

class UserAuthentication(ABC):
    @abstractmethod
    def registration(self,data:dict)-> dict:
        pass
    
    @abstractmethod
    def register_practice_identity(self,data:dict)-> dict:
        pass

    @abstractmethod
    def register_practice_details(self,data:dict)-> dict:
        pass

    @abstractmethod
    def compliance_agreement(self,data:dict)-> dict:
        pass