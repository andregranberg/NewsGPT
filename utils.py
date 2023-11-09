import json
import requests


def fetch_first_article_url(keyword: str, RapidAPIKey: str) -> str | None:
    url = "https://bing-news-search1.p.rapidapi.com/news/search"
    querystring = {"q": keyword, "textFormat": "Raw", "safeSearch": "Off", "mkt":"en-US"}
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
    url = "https://open-ai21.p.rapidapi.com/conversationgpt35"
    payload = {
        "messages": [
            {
                "role": "user",
                "content": f"give me a short summary of this text in journalistic style: {news_article}"
            }
        ],
        "web_access": False,
        "system_prompt": "",
        "temperature": 0.9,
        "top_k": 10,
        "top_p": 0.9,
        "max_tokens": 256
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RapidAPIKey,  # Ensure you use the correct API key variable or config
        "X-RapidAPI-Host": "open-ai21.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if response_json.get('status') and 'result' in response_json:
        return response_json['result']
    else:
        return "Error: Could not summarize the article."

