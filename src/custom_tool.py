from langchain_core.tools import tool


@tool
def stock_screener(
    pe_ratio: float,
    roe: float,
    debt_to_equity: float
) -> str:
    """
    Perform a simple stock screening based on financial ratios.
    """

    conditions = []

    if pe_ratio < 25:
        conditions.append("PE ratio looks reasonable")
    else:
        conditions.append("PE ratio is relatively high")

    if roe > 15:
        conditions.append("ROE is strong")
    else:
        conditions.append("ROE is relatively weak")

    if debt_to_equity < 1:
        conditions.append("Debt-to-equity is under control")
    else:
        conditions.append("Debt-to-equity is relatively high")

    return "\n".join(
        f"- {condition}"
        for condition in conditions
    )


if __name__ == "__main__":

    result = stock_screener.invoke(
        {
            "pe_ratio": 22,
            "roe": 18,
            "debt_to_equity": 0.5
        }
    )

    print(result)