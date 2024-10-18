# utils/formatting.py

import logging
from clients import get_groq_client

# Configure logging for formatting
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

groq_client = get_groq_client()

def reconstruct_formatting(raw_text):
    """
    Use Groq LLM to reconstruct the original formatting of the PDF text.
    """
    try:
        system_prompt = (
            "You are an assistant that reconstructs the original formatting of text extracted from a PDF. "
            "Preserve the structure, headings, bullet points, and other formatting elements without altering the content."
        )

        user_prompt = raw_text

        completion = groq_client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # Lower temperature for more deterministic output
            max_tokens=8000,
            top_p=0.95,
            stream=False,  # Synchronous processing
            stop=None,
        )

        # Access the first choice directly
        if not completion.choices:
            logger.error("No choices returned in the completion.")
            return None

        formatted_text = completion.choices[0].message.content.strip()
        logger.info("Reconstructed formatted text successfully.")
        return formatted_text

    except Exception as e:
        logger.error(f"Error reconstructing formatting with Groq: {e}")
        return None
