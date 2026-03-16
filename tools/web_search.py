from ddgs import DDGS


def duckduckgo_search(query: str) -> list[dict]:
    """
    Perform a search using the updated ddgs library (2026 standard).
    """
    results = []
    try:
        # Initializing the new DDGS client
        with DDGS() as ddgs:
            # We use the .text() method.
            # 'max_results=5' gives the agent a few options to choose from.
            # 'region="wt-wt"' is global; 'timelimit="m"' gets the last month.
            search_gen = ddgs.text(query, max_results=5, timelimit="m")

            for r in search_gen:
                results.append(
                    {
                        "title": r.get("title"),
                        "url": r.get("href"),
                        "snippet": r.get("body"),
                    }
                )

    except Exception as e:
        return [{"error": f"Search failed: {e}"}]

    return (
        results
        if results
        else [{"message": "No specific news results found for this query."}]
    )
