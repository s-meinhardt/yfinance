from ..utils import (
    dynamic_docstring,
    extract_values,
    generate_list_table_from_dict_simple,
    merge_two_level_dicts,
)
from .etf_query import COMMON_SCREENER_EQ_MAP, COMMON_SCREENER_FIELDS
from .query import Query

SCREENER_FIELDS = merge_two_level_dicts(
    COMMON_SCREENER_FIELDS,
    {
        "Technicals": {
            "twohundreddaymovingavg",
            "fiftydaymovingavg",
        },
    },
)


class FundQuery(Query):
    """
    The `FundQuery` class constructs filters for mutual funds based on
    specific criteria such as region, sector, exchange, and peer group.

    Start with value operations: `EQ` (equals), `IS-IN` (is in), `BTWN` (between),
    `GT` (greater than), `LT` (less than), `GTE` (greater or equal), `LTE` (less or equal).

    Combine them with logical operations: `AND`, `OR`.

    Example:
        Predefined Yahoo query `solid_large_growth_funds`:

        .. code-block:: python

            from yfinance import FundQuery

            FundQuery('and', [
                FundQuery('eq', ['categoryname', 'Large Growth']),
                FundQuery('is-in', ['performanceratingoverall', 4, 5]),
                FundQuery('lt', ['initialinvestment', 100001]),
                FundQuery('lt', ['annualreturnnavy1categoryrank', 50]),
                FundQuery('eq', ['exchange', 'NAS'])
            ])
    """

    @property
    def quote_type(self) -> str:
        return "MUTUALFUND"

    @dynamic_docstring(
        {
            "valid_operand_fields_table": generate_list_table_from_dict_simple(
                SCREENER_FIELDS,
                title="Valid Operand Fields",
                columns=["Category", "Fields"],
                bullet_symbol="",
            )
        }
    )
    @property
    def valid_fields(self) -> dict:
        """
        Valid operands, grouped by category.
        {valid_operand_fields_table}
        """
        return SCREENER_FIELDS

    @dynamic_docstring(
        {
            "valid_values_table": generate_list_table_from_dict_simple(
                COMMON_SCREENER_EQ_MAP,
                title="Valid EQ/IS-IN Operand Values",
                columns=["Field", "Permitted Values"],
                bullet_symbol="",
            )
        }
    )
    @property
    def valid_values(self) -> dict:
        """
        Most operands take number values, but some have a restricted set of valid values.
        {valid_values_table}
        """
        return {
            field: extract_values(values)
            for field, values in COMMON_SCREENER_EQ_MAP.items()
        }
