import warnings
from json import dumps
from typing import Any, Optional, Union

from requests import Session

from yfinance.const import _QUERY1_URL_
from yfinance.data import YfData

from ..utils import dynamic_docstring, generate_list_table_from_dict_universal
from .equity_query import EquityQuery
from .etf_query import ETFQuery
from .fund_query import FundQuery
from .index_query import IndexQuery
from .predifined_queries import PREDEFINED_SCREENER_QUERIES
from .query import Query

_SCREENER_URL_ = f"{_QUERY1_URL_}/v1/finance/screener"
_PREDEFINED_URL_ = f"{_SCREENER_URL_}/predefined/saved"

PREDEFINED_SCREENER_BODY_DEFAULTS = {
    "offset": 0, "count": 25, "userId": "", "userIdType": "guid"
}


@dynamic_docstring({"predefined_screeners": generate_list_table_from_dict_universal(PREDEFINED_SCREENER_QUERIES, bullets=True, title='Predefined queries (Dec-2024)')})
def screen(
    query: Union[str, EquityQuery, FundQuery, ETFQuery, IndexQuery],
    offset: Optional[int] = None,
    size: Optional[int] = None,
    count: Optional[int] = None,
    sortField: Optional[str] = None,
    sortAsc: Optional[bool] = None,
    userId: str = "",
    userIdType: str = "guid",
    session: Optional[Session] = None,
) -> dict:
    """
    Run a screen: predefined query, or custom query.

    :Parameters:
        * Defaults only apply if query = EquityQuery, FundQuery, ETFQuery or IndexQuery.
        query : str | Query:
            The query to execute, either name of predefined or custom query.
            For predefined list run yf.PREDEFINED_SCREENER_QUERIES.keys()
        offset : int
            The offset for the results. Default 0.
        size : int
            number of results to return. Default 100, maximum 250 (Yahoo)
            Use count instead for predefined queries.
        count : int
            number of results to return. Default 25, maximum 250 (Yahoo)
            Use size instead for custom queries.
        sortField : str
            field to sort by. Default "ticker"
        sortAsc : bool
            Sort ascending? Default False
        userId : str
            The user ID. Default empty.
        userIdType : str
            Type of user ID (e.g., "guid"). Default "guid".

    Example: predefined query
        .. code-block:: python

            import yfinance as yf
            response = yf.screen("aggressive_small_caps")

    Example: custom query
        .. code-block:: python

            import yfinance as yf
            from yfinance import EquityQuery
            q = EquityQuery('and', [
                   EquityQuery('gt', ['percentchange', 3]),
                   EquityQuery('eq', ['region', 'us'])
            ])
            response = yf.screen(q, sortField = 'percentchange', sortAsc = True)

    To access predefineds query code
        .. code-block:: python

            import yfinance as yf
            query = yf.PREDEFINED_SCREENER_QUERIES['aggressive_small_caps']

    {predefined_screeners}
    """

    if isinstance(query, Query):
        result = query.screen(
            offset=offset or 0,
            size=size or 25,
            sortField=sortField or "ticker",
            sortType="ASC" if sortAsc else "DESC",
            userId=userId,
            userIdType=userIdType,
            session=session,
        )
        return result

    if query not in PREDEFINED_SCREENER_QUERIES:
        raise ValueError(f"Unknown query: {query}")

    _data = YfData(session=session)

    if count is not None and count > 250:
        raise ValueError("Yahoo limits query count to 250, reduce count.")
    if size is not None:
        warnings.warn(
            "Screen 'size' argument is deprecated for predefined screens, set 'count' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
    if count is None and size is not None and size > 250:
        raise ValueError("Yahoo limits query size to 250, reduce size.")

    fields = PREDEFINED_SCREENER_QUERIES[query]
    params = {
        "corsDomain": "finance.yahoo.com",
        "formatted": "false",
        "lang": "en-US",
        "region": "US",
        "scrIds": fields["query"],
        "offset": offset or fields.get("offset", 0),
        "count": count or size or fields.get("count", 25),
        "userId": userId,
        "userIdType": userIdType,
        "sortField": sortField or fields.get("sortField", "ticker"),
    }
    if sortAsc is None:
        params["sortType"] = fields.get("sortType", "DESC")
    elif sortAsc:
        params["sortType"] = "ASC"
    else:
        params["sortType"] = "DESC"

    resp = _data.get(url=_PREDEFINED_URL_, params=params)
    resp.raise_for_status()
    return resp.json()["finance"]["result"][0]
