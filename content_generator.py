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
        다음 정보를 사용하여 전문가 수준의 상세하고 신뢰도 높은 블로그 포스트를 작성해 주세요.

        **주제:** "{article_title}"
        **출처:** {article_publisher} ({article_url})
        **주요 키워드:** {main_keyword}
        **관련 키워드:** {{', '.join(related_keywords)}}
        **작성 언어:** {DEFAULT_LANGUAGE}

        **요구사항:**
        1.  **제목**: 주요 키워드와 관련 키워드를 자연스럽게 사용하여 SEO에 최적화된, 전문가의 시선이 드러나는 제목을 생성해 주세요.
        2.  **분량**: 본문은 최소 **2000자 이상**으로 작성하여 주제에 대해 깊이 있는 정보를 제공해 주세요.
        3.  **구조 및 가독성**:
            - 서론, 본론, 결론의 명확한 구조를 갖춰주세요.
            - 여러 개의 문단으로 내용을 논리적으로 구분해 주세요.
            - '###' 와 같은 마크다운 소제목을 사용하여 본문을 구조화하고, 필요한 경우 글머리 기호(bullet points)나 번호 매기기를 활용하여 가독성을 높여주세요.
        4.  **신뢰성 및 전문성**:
            - "{article_publisher}"에서 제공된 정보를 바탕으로, 해당 분야의 전문가가 작성한 것처럼 권위 있는 어조를 사용해 주세요.
            - 독자들에게 신뢰를 주기 위해, 본문 내용 중 적절한 부분에서 "{article_publisher}"와 같은 정보 출처를 자연스럽게 언급해 주세요.
        5.  **마무리**: 내용 요약과 함께 독자의 참여를 유도할 수 있는 질문으로 마무리해 주세요.
        6.  **형식**: 결과물은 "제목: [여기에 제목]"과 "내용: [여기에 내용]" 형식으로만 반환해 주세요. 내용은 마크다운 형식을 사용해야 합니다.
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
