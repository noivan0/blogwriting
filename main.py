import argparse
import sys
from config import validate_config, ConfigError
from news_fetcher import get_news
from trend_analyzer import select_hot_topic, get_related_keywords
from content_generator import generate_blog_post
from blogger_client import get_blogger_service, create_post

def main():
    """
    The main function to run the blog automation workflow.
    """
    parser = argparse.ArgumentParser(description="Automate blog posting with news, trends, and Gemini.")
    parser.add_argument("keyword", type=str, help="The main keyword (theme) for the blog post.")
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publish the post directly. If not set, the post will be saved as a draft.",
    )
    args = parser.parse_args()

    try:
        print("--- Starting Blog Post Automation ---")
        
        # 1. Validate configuration
        print("\n[Step 1/6] Validating configuration...")
        validate_config()

        # 2. Fetch news
        print(f"\n[Step 2/6] Fetching news for keyword: '{args.keyword}'")
        news_articles = get_news(args.keyword)
        if not news_articles:
            print("Could not fetch any news. Exiting.")
            sys.exit(1)

        # 3. Select topic
        print("\n[Step 3/6] Selecting a hot topic...")
        hot_topic = select_hot_topic(news_articles)
        if not hot_topic:
            print("Could not select a topic. Exiting.")
            sys.exit(1)

        # 4. Analyze trends and get related keywords
        print("\n[Step 4/6] Analyzing trends for related keywords...")
        related_keywords = get_related_keywords(args.keyword)
        # We add the main keyword to the list for the generator
        all_keywords = [args.keyword] + related_keywords

        # 5. Generate blog post content
        print("\n[Step 5/6] Generating blog post content with Gemini...")
        title, content = generate_blog_post(hot_topic, args.keyword, all_keywords)
        if not title or not content:
            print("Could not generate blog content. Exiting.")
            sys.exit(1)

        # 6. Authenticate and post to Blogger
        print("\n[Step 6/6] Posting to Blogger...")
        blogger_service = get_blogger_service()
        if not blogger_service:
            print("Could not authenticate with Blogger. Exiting.")
            sys.exit(1)

        is_draft = not args.publish
        create_post(blogger_service, title, content, is_draft=is_draft)

        print("\n--- Blog Post Automation Finished Successfully! ---")

    except ConfigError as e:
        print(f"\n[ERROR] Configuration Error: {e}")
        print("Please check your .env and client_secret.json files.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()