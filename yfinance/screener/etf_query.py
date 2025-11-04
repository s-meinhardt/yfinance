from collections.abc import Collection

from ..const import SECTOR_INDUSTRY_MAPPING
from ..utils import (
    dynamic_docstring,
    extract_values,
    generate_list_table_from_dict_simple,
    merge_two_level_dicts,
)
from .fund_categories import FUND_CATEGORIES
from .fund_companies import FUND_COMPANIES
from .query import Query
from .region_code_mapping import REGION_CODE_MAPPING
from .region_exchange_code_mapping import REGION_EXCHANGE_CODE_MAPPING

COMMON_SCREENER_FIELDS = {
    "eq_fields": {
        "categoryname",
        "fundfamilyname",
        "region",
        "exchange",
        "sector",
        "performanceratingoverall",
        "riskratingoverall",
    },
    "price": {
        "eodprice",
        "intradayprice",
        "intradaypricechange",
        "percentchange",
    },
    "Market Data": {
        "fundnetassets",
        "initialinvestment",
        "marketcapitalvaluelong",
    },
    "Performance": {
        "annualreturnnavy1",
        "annualreturnnavy3",
        "annualreturnnavy5",
        "annualreturnnavy1categoryrank",
        "fiftytwowkpercentchange",
        "quarterendtrailingreturnytd",
        "trailing_3m_return",
        "trailing_ytd_return",
    },
    "Ratios": {
        "annualreportgrossexpenseratio",
        "annualreportnetexpenseratio",
        "turnoverratio",
    },
    "Ratings": {"performanceratingoverall", "riskratingoverall"},
}

SCREENER_FIELDS = merge_two_level_dicts(
    COMMON_SCREENER_FIELDS,
    {
        "Market Data": {
            "dayvolume",
            "eodvolume",
            "avgdailyvol3m",
        },
    },
)

COMMON_SCREENER_EQ_MAP = {
    "performanceratingoverall": {1, 2, 3, 4, 5},
    "riskratingoverall": {1, 2, 3, 4, 5},
    "region": REGION_CODE_MAPPING,
    "sector": SECTOR_INDUSTRY_MAPPING.keys(),
    "exchange": REGION_EXCHANGE_CODE_MAPPING,
    "categoryname": FUND_CATEGORIES,
    "fundfamilyname": FUND_COMPANIES,
}


class ETFQuery(Query):
    """
    The `ETFQuery` class constructs filters for exchange-traded funds (ETFs) based on
     specific criteriasuch as region, sector, exchange, and volume.

    Start with value operations: `EQ` (equals), `IS-IN` (is in), `BTWN` (between),
    `GT` (greater than), `LT` (less than), `GTE` (greater or equal), `LTE` (less or equal).

    Combine them with logical operations: `AND`, `OR`.

    Example:
        Predefined Yahoo query `solid_large_growth_etfs`:

        .. code-block:: python

            from yfinance import ETFQuery

            ETFQuery('and', [
                ETFQuery('eq', ['categoryname', 'Large Growth']),
                ETFQuery('is-in', ['performanceratingoverall', 4, 5]),
                ETFQuery('lt', ['initialinvestment', 100001]),
                ETFQuery('lt', ['annualreturnnavy1categoryrank', 50]),
                ETFQuery('eq', ['exchange', 'NGM'])
            ])
    """

    @property
    def quote_type(self) -> str:
        return "ETF"

    @dynamic_docstring(
        {
            "valid_operand_fields_table": generate_list_table_from_dict_simple(
                SCREENER_FIELDS,
                title="Valid Operand Fields",
                columns=["Category", "Fields"],
                bullet_symbol="•",
            )
        }
    )
    @property
    def valid_fields(self) -> dict[str, Collection[str]]:
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
                bullet_symbol="•",
            )
        }
    )
    @property
    def valid_values(self) -> dict[str, Collection]:
        """
        Most operands take number values, but some have a restricted set of valid values.
        {valid_values_table}
        """
        return {
            field: extract_values(values)
            for field, values in COMMON_SCREENER_EQ_MAP.items()
        }
