import sys
import os
import markdown

# Add the parent directory to the Python path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from content_generator import generate_blog_post

def save_as_html(title: str, content_md: str, main_keyword: str):
    """
    Converts markdown content to HTML and saves it to a file.
    """
    html_content = markdown.markdown(content_md, extensions=['fenced_code', 'tables'])
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{ font-family: sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: auto; }}
            h1 {{ color: #333; }}
            pre {{ background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
            code {{ font-family: monospace; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        {html_content}
    </body>
    </html>
    """
    
    filename = f"{main_keyword.replace(' ', '_')}.html"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"\n✅ Successfully saved content to '{os.path.abspath(filename)}'")
    except Exception as e:
        print(f"❌ Failed to save HTML file: {e}")

def interactive_post_generator():
    """
    Interactively generates a blog post based on user input and saves it as an HTML file.
    """
    print("--- Interactive Blog Post Generator ---")

    try:
        # 1. Validate configuration for content generation
        print("\n[Step 1/3] Validating configuration...")
        from config import OPENROUTER_API_KEY # Import specifically for the check
        if not OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is not set in the .env file.")
        print("Configuration is valid for content generation.")
    except Exception as e:
        print(f"[ERROR] Configuration validation failed: {e}")
        print("Please ensure your .env file contains the OPENROUTER_API_KEY.")
        return

    # 2. Get input from user
    print("\n[Step 2/3] Please provide the following details:")
    topic_title = input("Enter the topic or article title: ")
    main_keyword = input("Enter the main keyword: ")
    related_keywords_str = input("Enter related keywords (comma-separated): ")
    related_keywords = [k.strip() for k in related_keywords_str.split(',')]

    # Create a mock article structure for the generator function
    topic_article = {
        'title': topic_title,
        'url': 'urn:local:user-input',
        'publisher': {'title': 'User Input'}
    }

    print(f"\n[Step 3/3] Generating content with the following details:")
    print(f"  - Main Keyword: {main_keyword}")
    print(f"  - Topic: '{topic_article['title']}'")
    print("-" * 20)

    # Call the function to be tested
    title, content = generate_blog_post(topic_article, main_keyword, related_keywords)

    print("\n--- Generation Results ---")
    if title and content:
        print(f"✅ Generation Successful!")
        # Save the result as an HTML file
        save_as_html(title, content, main_keyword)
    else:
        print(f"❌ Generation Failed.")
        print("Please check the console for error messages from the function.")

    print("\n--- Process Finished ---")

if __name__ == "__main__":
    interactive_post_generator()