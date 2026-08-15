from src.tools.tools import web_search, scrape_url

results = scrape_url.invoke(
    "https://en.wikipedia.org/wiki/New_Delhi"
)

print(results)