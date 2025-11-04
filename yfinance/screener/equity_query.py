from yfinance.const import SECTOR_INDUSTRY_MAPPING

from ..utils import (
    dynamic_docstring,
    extract_values,
    generate_list_table_from_dict_simple,
)
from .peer_groups import PEER_GROUPS
from .query import Query
from .region_code_mapping import REGION_CODE_MAPPING
from .region_exchange_code_mapping import REGION_EXCHANGE_CODE_MAPPING

EQUITY_SCREENER_EQ_MAP = {
    "region": REGION_CODE_MAPPING,
    "exchange": REGION_EXCHANGE_CODE_MAPPING,
    "sector": SECTOR_INDUSTRY_MAPPING.keys(),
    "industry": SECTOR_INDUSTRY_MAPPING,
    "peer_group": PEER_GROUPS,
}

EQUITY_SCREENER_FIELDS = {
    "eq_fields": {"region", "sector", "peer_group", "industry", "exchange"},
    "price": {
        "eodprice",
        "intradaypricechange",
        "intradayprice",
        "lastclosemarketcap.lasttwelvemonths",
        "percentchange",
        "lastclose52weekhigh.lasttwelvemonths",
        "fiftytwowkpercentchange",
        "lastclose52weeklow.lasttwelvemonths",
        "intradaymarketcap",
    },
    "trading": {
        "beta",
        "avgdailyvol3m",
        "pctheldinsider",
        "pctheldinst",
        "dayvolume",
        "eodvolume",
    },
    "short_interest": {
        "short_percentage_of_shares_outstanding.value",
        "short_interest.value",
        "short_percentage_of_float.value",
        "days_to_cover_short.value",
        "short_interest_percentage_change.value",
    },
    "valuation": {
        "bookvalueshare.lasttwelvemonths",
        "lastclosemarketcaptotalrevenue.lasttwelvemonths",
        "lastclosetevtotalrevenue.lasttwelvemonths",
        "pricebookratio.quarterly",
        "peratio.lasttwelvemonths",
        "lastclosepricetangiblebookvalue.lasttwelvemonths",
        "lastclosepriceearnings.lasttwelvemonths",
        "pegratio_5y",
    },
    "profitability": {
        "consecutive_years_of_dividend_growth_count",
        "returnonassets.lasttwelvemonths",
        "returnonequity.lasttwelvemonths",
        "forward_dividend_per_share",
        "forward_dividend_yield",
        "returnontotalcapital.lasttwelvemonths",
    },
    "leverage": {
        "lastclosetevebit.lasttwelvemonths",
        "netdebtebitda.lasttwelvemonths",
        "totaldebtequity.lasttwelvemonths",
        "ltdebtequity.lasttwelvemonths",
        "ebitinterestexpense.lasttwelvemonths",
        "ebitdainterestexpense.lasttwelvemonths",
        "lastclosetevebitda.lasttwelvemonths",
        "totaldebtebitda.lasttwelvemonths",
    },
    "liquidity": {
        "quickratio.lasttwelvemonths",
        "altmanzscoreusingtheaveragestockinformationforaperiod.lasttwelvemonths",
        "currentratio.lasttwelvemonths",
        "operatingcashflowtocurrentliabilities.lasttwelvemonths",
    },
    "income_statement": {
        "totalrevenues.lasttwelvemonths",
        "netincomemargin.lasttwelvemonths",
        "grossprofit.lasttwelvemonths",
        "ebitda1yrgrowth.lasttwelvemonths",
        "dilutedepscontinuingoperations.lasttwelvemonths",
        "quarterlyrevenuegrowth.quarterly",
        "epsgrowth.lasttwelvemonths",
        "netincomeis.lasttwelvemonths",
        "ebitda.lasttwelvemonths",
        "dilutedeps1yrgrowth.lasttwelvemonths",
        "totalrevenues1yrgrowth.lasttwelvemonths",
        "operatingincome.lasttwelvemonths",
        "netincome1yrgrowth.lasttwelvemonths",
        "grossprofitmargin.lasttwelvemonths",
        "ebitdamargin.lasttwelvemonths",
        "ebit.lasttwelvemonths",
        "basicepscontinuingoperations.lasttwelvemonths",
        "netepsbasic.lasttwelvemonthsnetepsdiluted.lasttwelvemonths",
    },
    "balance_sheet": {
        "totalassets.lasttwelvemonths",
        "totalcommonsharesoutstanding.lasttwelvemonths",
        "totaldebt.lasttwelvemonths",
        "totalequity.lasttwelvemonths",
        "totalcurrentassets.lasttwelvemonths",
        "totalcashandshortterminvestments.lasttwelvemonths",
        "totalcommonequity.lasttwelvemonths",
        "totalcurrentliabilities.lasttwelvemonths",
        "totalsharesoutstanding",
    },
    "cash_flow": {
        "forward_dividend_yield",
        "leveredfreecashflow.lasttwelvemonths",
        "capitalexpenditure.lasttwelvemonths",
        "cashfromoperations.lasttwelvemonths",
        "leveredfreecashflow1yrgrowth.lasttwelvemonths",
        "unleveredfreecashflow.lasttwelvemonths",
        "cashfromoperations1yrgrowth.lasttwelvemonths",
    },
    "esg": {
        "esg_score",
        "environmental_score",
        "governance_score",
        "social_score",
        "highest_controversy",
    },
}


class EquityQuery(Query):
    """
    The `EquityQuery` class constructs filters for stocks based on
    specific criteria such as region, sector, exchange, and peer group.

    Start with value operations: `EQ` (equals), `IS-IN` (is in), `BTWN` (between),
    `GT` (greater than), `LT` (less than), `GTE` (greater or equal), `LTE` (less or equal).

    Combine them with logical operations: `AND`, `OR`.

    Example:
        Predefined Yahoo query `aggressive_small_caps`:

        .. code-block:: python

            from yfinance import EquityQuery

            EquityQuery('and', [
                EquityQuery('is-in', ['exchange', 'NMS', 'NYQ']),
                EquityQuery('lt', ["epsgrowth.lasttwelvemonths", 15])
            ])
    """

    @property
    def quote_type(self) -> str:
        return "EQUITY"

    @dynamic_docstring(
        {
            "valid_operand_fields_table": generate_list_table_from_dict_simple(
                EQUITY_SCREENER_FIELDS,
                title="Valid Operand Fields",
                columns=["Category", "Fields"],
            )
        }
    )
    @property
    def valid_fields(self) -> dict:
        """
        Valid operands, grouped by category.
        {valid_operand_fields_table}
        """
        return EQUITY_SCREENER_FIELDS

    @dynamic_docstring(
        {
            "valid_values_table": generate_list_table_from_dict_simple(
                EQUITY_SCREENER_EQ_MAP,
                title="Valid EQ/IS-IN Operand Values",
                columns=["Field", "Permitted Values"],
            )
        }
    )
    @property
    def valid_values(self) -> dict:
        """
        Most operands take number values, but some have a restricted set of valid values.
        {valid_values_table}
        """
        # Extract values from nested structures for validation
        return {
            field: extract_values(values)
            for field, values in EQUITY_SCREENER_EQ_MAP.items()
        }
