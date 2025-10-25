from abc import ABC, abstractmethod
from pydantic import BaseModel


class BaseNLP(ABC):

    @abstractmethod
    def chat(self, model_name: str, instructions: str, messages: list): ...

    @abstractmethod
    def struct_output(
        self, model_name: str, instructions: str, messages: list, structure: BaseModel
    ): ...

    @abstractmethod
    def func_call(self, model_name: str, messages: list, instructions: str, func): ...
