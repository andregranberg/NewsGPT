import json
import requests


def fetch_first_article_url(keyword: str, RapidAPIKey: str) -> str | None:
    url = "https://bing-news-search1.p.rapidapi.com/news/search"
    querystring = {"q": keyword, "textFormat": "Raw", "safeSearch": "Off"}
    headers = {
        "X-BingApis-SDK": "true",
        "X-RapidAPI-Key": RapidAPIKey,
        "X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers, params=querystring)
    response_json = response.json()

    def is_from_msn(article):
        url = article.get("url", "")
        return "msn.com" in url

    if "value" in response_json and response_json["value"]:
        filtered_articles = [
            article for article in response_json["value"] if not is_from_msn(article)
        ]
        if filtered_articles:
            return filtered_articles[0].get("url")
    return None


def extract_article_text(article_url: str, RapidAPIKey: str) -> str:
    url = "https://lexper.p.rapidapi.com/v1.1/extract"
    querystring = {"url": article_url, "js_timeout": "30", "media": "true"}
    headers = {
        "X-RapidAPI-Key": RapidAPIKey,
        "X-RapidAPI-Host": "lexper.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers, params=querystring)
    response_json = response.json()
    if "article" in response_json and "text" in response_json["article"]:
        return response_json["article"]["text"]
    else:
        return "Error: Article text not found."


def summarize_article(news_article: str, RapidAPIKey: str) -> str:
    url = "https://open-ai21.p.rapidapi.com/conversationgpt"
    payload = {
        "messages": [
            {
                "role": "user",
                "content": f"rewrite this to remove repetetive stuff while keeping the key information: {news_article}",
            }
        ]
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RapidAPIKey,
        "X-RapidAPI-Host": "open-ai21.p.rapidapi.com",
    }
    response = requests.post(url, json=payload, headers=headers)
    gpt_response = response.json()["GPT"]
    parsed_gpt_response = json.loads(gpt_response)

    # Add this line to decode the JSON string again
    final_response = json.loads(parsed_gpt_response)

    return final_response
