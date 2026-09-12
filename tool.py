from langchain.tools import tool
import yfinance as yf
import json

@tool
def simple_screener(screen_type: str, offset: int) -> str:

    """Returns screened assets (stocks, funds, bonds) given popular criteria.

    Args:
        screen_type: One of a default set of stock screener queries from yahoo finance.
            aggressive_small_caps
            day_gainers
            day_losers
            growth_technology_stocks
            most_actives
            most_shorted_stocks
            small_cap_gainers
            undervalued_growth_stocks
            undervalued_large_caps
            conservative_foreign_funds
            high_yield_bond
            portfolio_anchors
            solid_large_growth_funds
            solid_midcap_growth_funds
            top_mutual_funds

    Returns:
        The a JSON output of assets that meet the criteria
    """

    query = yf.PREDEFINED_SCREENER_QUERIES[screen_type]['query']
    res = yf.screen(query, offset=offset, count=5)