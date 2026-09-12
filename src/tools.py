from langchain_core.tools import tool


@tool
def get_stock_info(symbol: str) -> str:
    """
    Get basic information about a stock.

    Args:
        symbol: Stock ticker symbol.
    """

    return f"Stock information requested for {symbol.upper()}."


@tool
def calculate_percentage_change(
    old_price: float,
    new_price: float
) -> float:
    """
    Calculate percentage change between two prices.
    """

    if old_price == 0:
        return 0.0

    change = ((new_price - old_price) / old_price) * 100

    return round(change, 2)


# List of tools
tools = [
    get_stock_info,
    calculate_percentage_change
]