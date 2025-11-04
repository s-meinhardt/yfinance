from .equity_query import EquityQuery
from .fund_query import FundQuery

PREDEFINED_SCREENER_QUERIES = {
    "aggressive_small_caps": {
        "sortField": "eodvolume",
        "sortType": "DESC",
        "query": EquityQuery(
            "and",
            [
                EquityQuery("is-in", ["exchange", "NMS", "NYQ"]),
                EquityQuery("lt", ["epsgrowth.lasttwelvemonths", 15]),
            ],
        ),
    },
    "day_gainers": {
        "sortField": "percentchange",
        "sortType": "DESC",
        "query": EquityQuery(
            "and",
            [
                EquityQuery("gt", ["percentchange", 3]),
                EquityQuery("eq", ["region", "us"]),
                EquityQuery("gte", ["intradaymarketcap", 2000000000]),
                EquityQuery("gte", ["intradayprice", 5]),
                EquityQuery("gt", ["dayvolume", 15000]),
            ],
        ),
    },
    "day_losers": {
        "sortField": "percentchange",
        "sortType": "ASC",
        "query": EquityQuery(
            "and",
            [
                EquityQuery("lt", ["percentchange", -2.5]),
                EquityQuery("eq", ["region", "us"]),
                EquityQuery("gte", ["intradaymarketcap", 2000000000]),
                EquityQuery("gte", ["intradayprice", 5]),
                EquityQuery("gt", ["dayvolume", 20000]),
            ],
        ),
    },
    "growth_technology_stocks": {
        "sortField": "eodvolume",
        "sortType": "DESC",
        "query": EquityQuery(
            "and",
            [
                EquityQuery("gte", ["quarterlyrevenuegrowth.quarterly", 25]),
                EquityQuery("gte", ["epsgrowth.lasttwelvemonths", 25]),
                EquityQuery("eq", ["sector", "Technology"]),
                EquityQuery("is-in", ["exchange", "NMS", "NYQ"]),
            ],
        ),
    },
    "most_actives": {
        "sortField": "dayvolume",
        "sortType": "DESC",
        "query": EquityQuery(
            "and",
            [
                EquityQuery("eq", ["region", "us"]),
                EquityQuery("gte", ["intradaymarketcap", 2000000000]),
                EquityQuery("gt", ["dayvolume", 5000000]),
            ],
        ),
    },
    "most_shorted_stocks": {
        "count": 25,
        "offset": 0,
        "sortField": "short_percentage_of_shares_outstanding.value",
        "sortType": "DESC",
        "query": EquityQuery(
            "and",
            [
                EquityQuery("eq", ["region", "us"]),
                EquityQuery("gt", ["intradayprice", 1]),
                EquityQuery("gt", ["avgdailyvol3m", 200000]),
            ],
        ),
    },
    "small_cap_gainers": {
        "sortField": "eodvolume",
        "sortType": "DESC",
        "query": EquityQuery(
            "and",
            [
                EquityQuery("lt", ["intradaymarketcap", 2000000000]),
                EquityQuery("is-in", ["exchange", "NMS", "NYQ"]),
            ],
        ),
    },
    "undervalued_growth_stocks": {
        "sortType": "DESC",
        "sortField": "eodvolume",
        "query": EquityQuery(
            "and",
            [
                EquityQuery("btwn", ["peratio.lasttwelvemonths", 0, 20]),
                EquityQuery("lt", ["pegratio_5y", 1]),
                EquityQuery("gte", ["epsgrowth.lasttwelvemonths", 25]),
                EquityQuery("is-in", ["exchange", "NMS", "NYQ"]),
            ],
        ),
    },
    "undervalued_large_caps": {
        "sortField": "eodvolume",
        "sortType": "DESC",
        "query": EquityQuery(
            "and",
            [
                EquityQuery("btwn", ["peratio.lasttwelvemonths", 0, 20]),
                EquityQuery("lt", ["pegratio_5y", 1]),
                EquityQuery("btwn", ["intradaymarketcap", 10000000000, 100000000000]),
                EquityQuery("is-in", ["exchange", "NMS", "NYQ"]),
            ],
        ),
    },
    "conservative_foreign_funds": {
        "sortType": "DESC",
        "sortField": "fundnetassets",
        "query": FundQuery(
            "and",
            [
                FundQuery(
                    "is-in",
                    [
                        "categoryname",
                        "Foreign Large Value",
                        "Foreign Large Blend",
                        "Foreign Large Growth",
                        "Foreign Small/Mid Growth",
                        "Foreign Small/Mid Blend",
                        "Foreign Small/Mid Value",
                    ],
                ),
                FundQuery("is-in", ["performanceratingoverall", 4, 5]),
                FundQuery("lt", ["initialinvestment", 100001]),
                FundQuery("lt", ["annualreturnnavy1categoryrank", 50]),
                FundQuery("is-in", ["riskratingoverall", 1, 2, 3]),
                FundQuery("eq", ["exchange", "NAS"]),
            ],
        ),
    },
    "high_yield_bond": {
        "sortType": "DESC",
        "sortField": "fundnetassets",
        "query": FundQuery(
            "and",
            [
                FundQuery("is-in", ["performanceratingoverall", 4, 5]),
                FundQuery("lt", ["initialinvestment", 100001]),
                FundQuery("lt", ["annualreturnnavy1categoryrank", 50]),
                FundQuery("is-in", ["riskratingoverall", 1, 2, 3]),
                FundQuery("eq", ["categoryname", "High Yield Bond"]),
                FundQuery("eq", ["exchange", "NAS"]),
            ],
        ),
    },
    "portfolio_anchors": {
        "sortType": "DESC",
        "sortField": "fundnetassets",
        "query": FundQuery(
            "and",
            [
                FundQuery("eq", ["categoryname", "Large Blend"]),
                FundQuery("is-in", ["performanceratingoverall", 4, 5]),
                FundQuery("lt", ["initialinvestment", 100001]),
                FundQuery("lt", ["annualreturnnavy1categoryrank", 50]),
                FundQuery("eq", ["exchange", "NAS"]),
            ],
        ),
    },
    "solid_large_growth_funds": {
        "sortType": "DESC",
        "sortField": "fundnetassets",
        "query": FundQuery(
            "and",
            [
                FundQuery("eq", ["categoryname", "Large Growth"]),
                FundQuery("is-in", ["performanceratingoverall", 4, 5]),
                FundQuery("lt", ["initialinvestment", 100001]),
                FundQuery("lt", ["annualreturnnavy1categoryrank", 50]),
                FundQuery("eq", ["exchange", "NAS"]),
            ],
        ),
    },
    "solid_midcap_growth_funds": {
        "sortType": "DESC",
        "sortField": "fundnetassets",
        "query": FundQuery(
            "and",
            [
                FundQuery("eq", ["categoryname", "Mid-Cap Growth"]),
                FundQuery("is-in", ["performanceratingoverall", 4, 5]),
                FundQuery("lt", ["initialinvestment", 100001]),
                FundQuery("lt", ["annualreturnnavy1categoryrank", 50]),
                FundQuery("eq", ["exchange", "NAS"]),
            ],
        ),
    },
    "top_mutual_funds": {
        "sortType": "DESC",
        "sortField": "percentchange",
        "query": FundQuery(
            "and",
            [
                FundQuery("gt", ["intradayprice", 15]),
                FundQuery("is-in", ["performanceratingoverall", 4, 5]),
                FundQuery("gt", ["initialinvestment", 1000]),
                FundQuery("eq", ["exchange", "NAS"]),
            ],
        ),
    },
}
