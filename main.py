import random
import jsonargparse
import streamlit as st
from jsonargparse import Namespace
from utils import fetch_first_article_url, extract_article_text, summarize_article

keywords = [
    "humanoids",
    "robotics",
    "electric vehicles",
    "open source large language models",
]


def summarize_given_keyword(keyword: str, RapidAPIKey: str) -> str:
    first_article_url = fetch_first_article_url(keyword, RapidAPIKey)
    if first_article_url:
        article_text = extract_article_text(first_article_url, RapidAPIKey)
        summary = summarize_article(article_text, RapidAPIKey)
    else:
        summary = "No articles found"
    return summary


def main(args: Namespace) -> None:
    st.title("Keyword-based Article Summarizer Chatbot")
    
    # Instead of using a default value, we only use the value from the text input
    keyword = st.text_input("Enter a keyword to get a summary:")

    conversation_history = []

    if keyword:
        user_message = f"You: {keyword}"
        conversation_history.append(user_message)
        summary_text = summarize_given_keyword(keyword, args.RapidAPIKey)

        # Replace quotes, escaped characters, and newlines
        summary_text = summary_text.strip('"').replace('\\"', '"').replace("\\n", "<br>")

        bot_message = (
            f"BinGo: <br>{summary_text}"
        )
        conversation_history.append(bot_message)

    # Display conversation history
    for message in conversation_history:
        if "You:" in message:
            st.markdown(
                f"<div style='background-color: #E0F7FA; padding: 10px; border-radius: 5px;'>{message}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='background-color: #C8E6C9; padding: 10px; border-radius: 5px;'>{message}</div>",
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    parser = jsonargparse.ArgumentParser(
        "Keyword-based Article Summarizer Chatbot", env_prefix="", default_env=True
    )
    # The --keyword argument no longer has a default value
    parser.add_argument("--keyword", type=str, required=False)
    parser.add_argument(
        "--RapidAPIKey",
        type=str,
        required=True  # Ensure the RapidAPIKey is provided
    )
    args = parser.parse_args()

    main(args)
