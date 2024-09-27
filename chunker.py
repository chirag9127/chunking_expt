from dotenv import load_dotenv
import os
import json
import openai
import re

from chunking_evaluation import BaseChunker

load_dotenv()

class LLMChunker(BaseChunker):
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key

    def split_text(self, content, chunk_size=750):
        prompt = f"""
        Split the following article content into chunks of approximately {chunk_size} characters each. 
        Keep headers and paragraphs together, and don't break up bulleted lists mid-list. 
        It's okay if chunks are slightly longer to keep related content together. Don't change or format the text.

        Article content:
        {content}

        Output the chunks as a ONLY JSON array of strings.
        """

        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that chunks text content."},
                    {"role": "user", "content": prompt}
                ],
            )

            content = response.choices[0].message.content
            # Handle potential code block formatting
            content = re.sub(r'^\s*```\s*|\s*```\s*$', '', content)
            # Remove 'json' prefix if present
            content = re.sub(r'^\s*json\s*', '', content, flags=re.IGNORECASE).strip()
            chunks = json.loads(content)
            return chunks
        except Exception as e:
            print(f"Error in chunking content: {e}")
            return [content]  # Return the entire content as a single chunk if there's an error

    def process_articles(self, articles):
        for article in articles:
            article['chunks'] = self.split_text(article['content'])
        return articles

if __name__ == "__main__":
    # Example usage
    chunker = LLMChunker()
    sample_content = """
    # Header 1
    This is a paragraph under header 1. It contains some information about a topic.

    ## Subheader 1.1
    - Bullet point 1
    - Bullet point 2
    - Bullet point 3

    # Header 2
    Another paragraph with different content. This one is a bit longer to demonstrate how the chunking works.

    ## Subheader 2.1
    1. Numbered list item 1
    2. Numbered list item 2
    3. Numbered list item 3

    # Header 3
    Final paragraph with some concluding remarks.
    """

    sample_article = {'content': sample_content}
    processed_articles = chunker.process_articles([sample_article])
    
    for article in processed_articles:
        print(f"Number of chunks: {len(article['chunks'])}")
        for i, chunk in enumerate(article['chunks'], 1):
            print(f"Chunk {i}: {chunk[:50]}...")  # Print first 50 characters of each chunk
        print("\n")