from typing import Protocol


class IDescriptable(Protocol):
    def get_description(self) -> str:
        pass


class IRandomCodable(Protocol):
    def get_random_code(self) -> int:
        pass
