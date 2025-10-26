from abc import ABC, abstractmethod

class AbsEmailServerConfig(ABC):

    @property
    @abstractmethod 
    def mail_server(self):
        raise NotImplementedError
    @property
    @abstractmethod 
    def mail_port(self):
        raise NotImplementedError

    @property
    @abstractmethod 
    def mail_username(self):
        raise NotImplementedError
    
    @property
    @abstractmethod 
    def mail_password(self):
        raise NotImplementedError
    
    @property
    @abstractmethod 
    def mail_sender_address(self):
        raise NotImplementedError
    
    @property
    @abstractmethod 
    def name_sender(self):
        raise NotImplementedError
    
    @property
    @abstractmethod 
    def mail_sender_address(self):
        raise NotImplementedError
    
    @property
    @abstractmethod 
    def mail_use_tls(self):
        raise NotImplementedError
        