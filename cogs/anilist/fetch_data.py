import requests
from anilist_errors import GraphQLError

URL = "https://graphql.anilist.co"

FETCH_QUERY = """
query ($name: String, $page: Int) {
  Page(page: $page) {
    pageInfo {
      hasNextPage
    }
    media (search: $name) {
        id
        siteUrl
        title {
            english
            romaji
            native
        }
        type
    }
  }
}
"""


async def fetch_data(name: str, *, page: int = 1) -> str | list[str]:
    variables = {"name": name, "page": page}
    response = requests.post(URL, json={"query": FETCH_QUERY, "variables": variables})

    if response.status_code != 200:
        raise GraphQLError("An error occurred while fetching data.")

    data = response.json()

    if data.get("errors"):
        raise GraphQLError(data["errors"])
