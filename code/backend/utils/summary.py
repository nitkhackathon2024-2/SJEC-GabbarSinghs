# utils/summary.py

import logging
import json
import re
from clients import get_groq_client
from sentence_transformers import SentenceTransformer

# Configure logging for summary
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

groq_client = get_groq_client()

# utils/summary.py

def generate_summary_tree(documents, existing_graph):
    """
    Generate or update the knowledge graph using Groq LLM based on the combined content of documents.
    """
    try:
        combined_text = "\n".join(documents)
        logger.info("Processing combined text with Groq LLM to generate simplified knowledge graph...")

        system_prompt = (
            "You are an assistant that structures data into a hierarchical multilevel knowledge graph in JSON format. "
            "Only include main headings and subheadings. The output should be a JSON object following this format: "
            "{\"name\": \"Root\", \"children\": [...]}. Ensure that only 'name' and 'children' keys are used. "
            "Do not include any explanations, code snippets, or text outside the JSON. Provide only the JSON output."
        )

        if existing_graph:
            # Convert existing graph to text to include in the prompt
            existing_graph_text = json.dumps(existing_graph)
            user_prompt = f"Existing Knowledge Graph:\n{existing_graph_text}\n\nNew Content:\n{combined_text}"
        else:
            user_prompt = combined_text

        completion = groq_client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=8000,
            top_p=0.95,
            stream=False,
            stop=None,
        )

        if not completion.choices:
            logger.error("No choices returned by Groq LLM.")
            return None

        knowledge_graph_str = completion.choices[0].message.content.strip()
        logger.info("Knowledge graph generated successfully.")

        json_match = re.search(r'\{.*\}', knowledge_graph_str, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            try:
                knowledge_graph = json.loads(json_str)
                return json.dumps(knowledge_graph, indent=2)
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing knowledge graph JSON: {e}")
                return None
        else:
            logger.error("Could not find JSON object in the LLM output.")
            return None

    except Exception as e:
        logger.error(f"Error generating knowledge graph with Groq: {e}")
        return None
