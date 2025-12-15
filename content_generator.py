from openai import OpenAI
from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_API_BASE,
    LLM_MODEL_NAME,
    DEFAULT_LANGUAGE,
    ConfigError
)

def generate_blog_post(topic_article: dict, main_keyword: str, related_keywords: list) -> tuple[str, str] | tuple[None, None]:
    """
    Generates an SEO-optimized blog post using an OpenRouter model.

    Args:
        topic_article (dict): The selected news article to write about.
        main_keyword (str): The main keyword for the post.
        related_keywords (list): A list of related keywords for SEO.

    Returns:
        A tuple containing (title, content). Returns (None, None) on failure.
    """
    try:
        if not OPENROUTER_API_KEY:
            raise ConfigError("OPENROUTER_API_KEY is not set. Please check your .env file.")

        client = OpenAI(
            base_url=OPENROUTER_API_BASE,
            api_key=OPENROUTER_API_KEY,
        )
        
        article_title = topic_article['title']
        article_url = topic_article['url']
        article_publisher = topic_article['publisher']['title']

        # Combine system and user prompts into a single user message
        system_prompt = "당신은 전문적인 블로거이자 SEO 전문가입니다. 주어진 정보를 바탕으로 SEO에 최적화된 매력적인 블로그 포스트를 작성합니다."
        
        user_prompt_details = f"""
        다음 정보를 사용하여 독자들이 흥미를 느끼고 검색 엔진에 최적화된 블로그 포스트를 작성해 주세요.

        **주제:** "{article_title}"
        **출처:** {article_publisher} ({article_url})
        **주요 키워드:** {main_keyword}
        **관련 키워드:** {', '.join(related_keywords)}
        **작성 언어:** {DEFAULT_LANGUAGE}

        **요구사항:**
        1.  주요 키워드와 관련 키워드를 자연스럽게 사용하여 SEO에 최적화된 제목을 생성해 주세요.
        2.  위 기사 내용을 바탕으로, 독자들이 쉽게 이해할 수 있도록 전문적인 블로그 포스트 형식으로 본문을 작성해 주세요.
        3.  서론, 본론, 결론의 구조를 갖추어 주세요.
        4.  독자의 흥미를 유발할 수 있는 어조를 사용해 주세요.
        5.  마지막에는 블로그 포스트 내용과 관련된 질문을 추가하여 독자의 참여를 유도해 주세요.
        6.  결과물은 "제목: [여기에 제목]"과 "내용: [여기에 내용]" 형식으로 반환해 주세요. 내용은 마크다운 형식을 사용해도 좋습니다.

        **예시:**
        제목: [여기에 생성된 제목]
        내용:
        ### [소제목 1]
        ... 본문 내용 ...

        ### [소제목 2]
        ... 본문 내용 ...
        """
        
        combined_prompt = f"{system_prompt}\n\n{user_prompt_details}"

        print(f"Generating blog post with model: {LLM_MODEL_NAME}...")
        
        response = client.chat.completions.create(
            model=LLM_MODEL_NAME,
            messages=[
                {"role": "user", "content": combined_prompt},
            ],
            temperature=0.7,
        )

        response_text = response.choices[0].message.content
        
        # Parse the response to extract title and content
        if "제목:" not in response_text or "내용:" not in response_text:
             print("Generated text is not in the expected '제목:... 내용:...' format.")
             # Fallback: use the whole text as content and generate a title
             title_part = f"{main_keyword}: {article_title}"
             content_part = response_text
        else:
            title_part = response_text.split("제목:")[1].split("내용:")[0].strip()
            content_part = response_text.split("내용:")[1].strip()

        print("Blog post generated successfully.")
        return title_part, content_part

    except Exception as e:
        print(f"An error occurred during content generation: {e}")
        return None, None
