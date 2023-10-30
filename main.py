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
    # If keyword is provided as an argument, use that
    # Otherwise, use the default value of 'random'
    if args.keyword:
        keyword = args.keyword
    else:
        keyword = "chatGPT"

    conversation_history = []

    st.title("Keyword-based Article Summarizer Chatbot")

    keyword = st.text_input(
        "Enter a keyword or leave blank for 'random':", value=keyword
    )

    # If using 'random' keyword, pick a random one from the list
    if keyword == "random":
        keyword = random.choice(keywords)

    if keyword:
        user_message = f"You: {keyword}"
        conversation_history.append(user_message)
        summary_text = summarize_given_keyword(keyword, args.RapidAPIKey)

        # Remove quotes at the beginning and end
        if summary_text.startswith('"') and summary_text.endswith('"'):
            summary_text = summary_text[1:-1]

        # Replace escaped quotes with regular quotes
        summary_text = summary_text.replace('"', '"')

        # Replace \n with actual new line
        summary_text = summary_text.replace("\\n", "<br>")

        bot_message = (
            f"Chatbot: Summary based on keyword '{keyword}': <br><br>{summary_text}"
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

    # Start with an instruction if the conversation history is empty
    if not conversation_history:
        st.write("Enter a keyword to get a summary.")


if __name__ == "__main__":
    parser = jsonargparse.ArgumentParser(
        "Keyword-based Article Summarizer Chatbot", env_prefix="", default_env=True
    )
    parser.add_argument("--keyword", type=str, default="chatGPT")
    parser.add_argument(
        "--RapidAPIKey",
        type=str
        #default=RAPIDAPI_KEY,
    )
    args = parser.parse_args()

    main(args)
