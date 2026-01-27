import numbers
from abc import ABC, abstractmethod
import logging

from collections.abc import Collection, Sequence
from json import dumps
from typing import Literal, Optional, Union

from requests import Session

from yfinance.const import _QUERY1_URL_
from yfinance.data import YfData
from yfinance.exceptions import YFNotImplementedError

# Operand = TypeVar("Operand", bound=Union["Query", str, numbers.Real])

logger = logging.getLogger(__name__)


class Query(ABC):
    _SCREENER_URL_ = f"{_QUERY1_URL_}/v1/finance/screener"

    def __init__(
        self,
        operator: str,
        operands: Sequence[Union["Query", str, int, float]],
        session: Optional[Session] = None,
    ):
        self._data = YfData(session=session)
        self.operator = operator.upper()
        self.operands = operands

        if not isinstance(operands, Sequence):
            raise TypeError("Invalid operand type")

        if self.operator == "IS-IN":
            self._validate_isin_operands()
        elif self.operator in {"OR", "AND"}:
            self._validate_or_and_operands()
        elif self.operator == "EQ":
            self._validate_eq_operands()
        elif self.operator == "BTWN":
            self._validate_btwn_operands()
        elif self.operator in {"GT", "LT", "GTE", "LTE"}:
            self._validate_gt_lt_operands()
        else:
            raise ValueError("Invalid Operator Value")

    @property
    @abstractmethod
    def quote_type(self) -> str:
        raise YFNotImplementedError("quote_type must be specified by child class")

    @property
    @abstractmethod
    def valid_fields(self) -> dict[str, Collection[str]]:
        raise YFNotImplementedError("valid_fields() needs to be implemented by child")

    @property
    @abstractmethod
    def valid_values(self) -> dict[str, Collection[str]]:
        raise YFNotImplementedError("valid_values() needs to be implemented by child")

    @property
    def numerical_fields(self) -> list[str]:
        return [
            field
            for category, fields in self.valid_fields.items()
            if category != "eq_fields"
            for field in fields
        ]

    def _validate_or_and_operands(self) -> None:
        if len(self.operands) <= 1:
            raise ValueError("Operands must have length longer than 1")
        # This validation prohibits things like EquityQuery('AND', [EquityQuery(...), FundQuery(...)])
        if not all(isinstance(e, type(self)) for e in self.operands):
            raise TypeError(
                f"Operands must be a sequence of objects of type {type(self)}"
            )

    def _validate_eq_operands(self) -> None:
        if len(self.operands) != 2:
            raise ValueError("Operands must have length 2 for EQ")
        # self._validate_categorical_operands()

    def _validate_btwn_operands(self) -> None:
        if len(self.operands) != 3:
            raise ValueError("Operands must have length 3 for BTWN")
        self._validate_numerical_operands()

    def _validate_gt_lt_operands(self) -> None:
        if len(self.operands) != 2:
            raise ValueError("Operands must have length 2 for GT/LT")
        self._validate_numerical_operands()

    def _validate_isin_operands(self) -> None:
        if len(self.operands) < 2:
            raise ValueError("Operands must be length 2+ for IS-IN")
        self._validate_categorical_operands()

    def _validate_numerical_operands(self) -> None:
        if self.operands[0] not in self.numerical_fields:
            raise ValueError(
                f'Invalid numerical field for {type(self)} "{self.operands[0]}"'
            )
        if not all(isinstance(operand, numbers.Real) for operand in self.operands[1:]):
            raise TypeError(
                f'Invalid numerical value in "{self.operands[1:]}" for field "{self.operands[0]}"'
            )

    def _validate_categorical_operands(self) -> None:
        if self.operands[0] not in self.valid_values:
            raise ValueError(
                f'Invalid categorical field for {type(self)} "{self.operands[0]}"'
            )
        if not all(
            operand in self.valid_values[self.operands[0]]
            for operand in self.operands[1:]
        ):
            raise ValueError(
                f'Invalid categorical value in "{self.operands[1:]}" for field "{self.operands[0]}"'
            )

    def to_dict(self) -> dict:
        operator = self.operator
        operands = self.operands
        if self.operator == "IS-IN":
            # Expand to OR of EQ queries
            operator = "OR"
            operands = [
                type(self)("EQ", [operands[0], operand]) for operand in operands[1:]
            ]
        return {
            "operator": operator,
            "operands": [
                operand.to_dict() if isinstance(operand, Query) else operand
                for operand in operands
            ],
        }

    def __repr__(self, indent=0) -> str:
        indent_str = "  " * indent
        class_name = self.__class__.__name__

        # For list operands, check if they contain any Query objects
        if any(isinstance(operand, Query) for operand in self.operands):
            # If there are nested queries, format them with newlines
            operands_str = ",\n".join(
                f"{indent_str}  {operand.__repr__(indent + 1) if isinstance(operand, Query) else repr(operand)}"
                for operand in self.operands
            )
            return f"{class_name}({self.operator}, [\n{operands_str}\n{indent_str}])"
        else:
            # For lists of simple types, keep them on one line
            return f"{class_name}({self.operator}, {repr(self.operands)})"

    def __str__(self) -> str:
        return self.__repr__()

    def screen(
        self,
        offset: int = 0,
        size: int = 25,
        sortField: str = "ticker",
        sortType: Literal["ASC", "DESC"] = "DESC",
        userId: str = "",
        userIdType: str = "guid",
        session: Optional[Session] = None,
    ) -> dict:
        
        if session:
            self._data = YfData(session=session)
            logger.warning(
                "Passing a session is deprecated and will be removed in future versions. "
                "Please pass the session when initializing the query."
            )
        
        if offset < 0:
            raise ValueError("The query offset must be a non-negative integer.")
        if size > 250 or size < 1:
            raise ValueError("The query size must be an integer between 1 and 250.")

        params = {
            "corsDomain": "finance.yahoo.com",
            "formatted": "false",
            "lang": "en-US",
            "region": "US",
        }
        body = {
            "quoteType": self.quote_type,
            "query": self.to_dict(),
            "offset": offset,
            "size": size,
            "sortField": sortField,
            "sortType": sortType,
            "userId": userId,
            "userIdType": userIdType,
        }
        data = dumps(body, separators=(",", ":"), ensure_ascii=False)
        response = self._data.post(self._SCREENER_URL_, data=data, params=params)
        response.raise_for_status()
        return response.json()["finance"]["result"][0]
