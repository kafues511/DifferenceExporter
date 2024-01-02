from dataclasses import dataclass
from typing import Union, Iterator, Any
 
 
__all__ = [
    "GridUtil",
]


@dataclass
class GridUtil:
    __column:Union[int, Iterator[int]]
    __row:Union[int, Iterator[int]]
    __columnspan:Union[int, Iterator[int]]
    __padx:Union[int, tuple[int, int], Iterator[int], Iterator[tuple[int, int]]]
    __pady:Union[int, tuple[int, int], Iterator[int], Iterator[tuple[int, int]]]
    __sticky:Union[str, Iterator[str]]

    def __init__(
        self,
        column:Union[int, tuple[int, ...], list[int]] = 0,
        row:Union[int, tuple[int, ...], list[int]] = 0,
        columnspan:Union[int, tuple[int, ...], list[int]] = 1,
        padx:Union[int, tuple[int, ...], list[int], tuple[int, int], tuple[tuple[int, int], ...], list[tuple[int, int]]] = 0,
        pady:Union[int, tuple[int, ...], list[int], tuple[int, int], tuple[tuple[int, int], ...], list[tuple[int, int]]] = 0,
        sticky:Union[str, tuple[str, ...], list[str]] = "NSEW",
        *args,
        **kwargs,
    ) -> None:
        self.__column = iter(column) if self.is_vector(column) else column
        self.__row = iter(row) if self.is_vector(row) else row
        self.__columnspan = iter(columnspan) if self.is_vector(columnspan) else columnspan
        self.__padx = iter(padx) if self.is_vector(padx) else padx
        self.__pady = iter(pady) if self.is_vector(pady) else pady
        self.__sticky = iter(sticky) if self.is_vector(sticky) else sticky

    @staticmethod
    def is_tuple(value:Any) -> bool:
        return len(value) > 0 if isinstance(value, tuple) else False

    @staticmethod
    def is_list(value:Any) -> bool:
        return len(value) > 0 if isinstance(value, list) else False

    @staticmethod
    def is_vector(value:Any) -> bool:
        return GridUtil.is_tuple(value) or GridUtil.is_list(value)

    @property
    def column(self) -> int:
        return next(self.__column) if isinstance(self.__column, Iterator) else self.__column

    @property
    def row(self) -> int:
        return next(self.__row) if isinstance(self.__row, Iterator) else self.__row

    @property
    def columnspan(self) -> int:
        return next(self.__columnspan) if isinstance(self.__columnspan, Iterator) else self.__columnspan

    @property
    def padx(self) -> Union[int, tuple[int, int]]:
        return next(self.__padx) if isinstance(self.__padx, Iterator) else self.__padx

    @property
    def pady(self) -> Union[int, tuple[int, int]]:
        return next(self.__pady) if isinstance(self.__pady, Iterator) else self.__pady

    @property
    def sticky(self) -> str:
        return next(self.__sticky) if isinstance(self.__sticky, Iterator) else self.__sticky
