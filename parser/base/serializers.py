from abc import ABC

from parser.base.data_typing import Review


class SerializerInterface(ABC):

    def _serialize_single(self, data: dict) -> Review:
        raise NotImplementedError

    def _serialize_from_list(self, data: list) -> list[Review]:
        raise NotImplementedError

    def serialize(self, data: dict | list) -> Review | list[Review]:
        raise NotImplementedError
