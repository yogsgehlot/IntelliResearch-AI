from abc import ABC, abstractmethod

class BaseStorage:

    @abstractmethod
    def save(self, file, filename: str) -> str:
        pass

    @abstractmethod
    def delete(self, path: str):
        pass