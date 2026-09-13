from langchain.tools import tool
import yfinance as yf
import json


@tool
def simple_screener(screen_type: str, offset: int | str = 0) -> str:
    """
    Returns screened assets (stocks, funds, bonds) using Yahoo Finance
    predefined screener queries.

    Args:
        screen_type: One of the following Yahoo Finance screeners:
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

        offset: Number of results to skip. Defaults to 0.

    Returns:
        JSON output containing the screened assets.
    """

    # --------------------------------------------------
    # Validate screen type
    # --------------------------------------------------

    if screen_type not in yf.PREDEFINED_SCREENER_QUERIES:
        return json.dumps({
            "error": f"Invalid screen_type: {screen_type}",
            "available_screeners": list(
                yf.PREDEFINED_SCREENER_QUERIES.keys()
            )
        }, indent=2)

    # --------------------------------------------------
    # Convert offset to integer
    # --------------------------------------------------

    if offset == "" or offset is None:
        offset = 0

    try:
        offset = int(offset)
    except (ValueError, TypeError):
        return json.dumps({
            "error": "offset must be a valid integer",
            "received": offset
        }, indent=2)

    # Prevent negative offset
    if offset < 0:
        offset = 0

    # --------------------------------------------------
    # Get Yahoo Finance query
    # --------------------------------------------------

    query = yf.PREDEFINED_SCREENER_QUERIES[screen_type]["query"]

    # --------------------------------------------------
    # Run screener
    # --------------------------------------------------

    try:
        res = yf.screen(
            query,
            offset=offset,
            count=5
        )
    except Exception as e:
        return json.dumps({
            "error": "Failed to fetch Yahoo Finance data",
            "details": str(e)
        }, indent=2)

    # --------------------------------------------------
    # Save complete Yahoo Finance response
    # --------------------------------------------------

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, default=str)

    # --------------------------------------------------
    # Select required fields
    # --------------------------------------------------

    fields = [
        "shortName",
        "bid",
        "ask",
        "exchange",
        "fiftyTwoWeekHigh",
        "fiftyTwoWeekLow",
        "averageAnalystRating",
        "dividendYield",
        "symbol"
    ]

    output_data = []

    for stock_detail in res.get("quotes", []):

        details = {}

        for key in fields:
            if key in stock_detail:
                details[key] = stock_detail[key]

        output_data.append(details)

    # --------------------------------------------------
    # Return proper JSON
    # --------------------------------------------------

    return json.dumps(output_data, indent=2, default=str)


# ------------------------------------------------------
# Test the tool directly
# ------------------------------------------------------

if __name__ == "__main__":

    result = simple_screener.invoke({
        "screen_type": "day_gainers",
        "offset": 0
    })

    print(result)