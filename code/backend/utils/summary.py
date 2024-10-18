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

def generate_summary_tree(documents):
    """
    Generate a simplified knowledge graph using Groq LLM based on the combined content of documents.
    """
    try:
        # Combine all documents into one text
        combined_text = "\n".join(documents)
        logger.info("Processing combined text with Groq LLM to generate simplified knowledge graph...")

        # Use a system prompt that instructs the LLM to produce the desired structure
        system_prompt = (
            "You are an assistant that structures data into a hierarchical multilevel knowledge graph in JSON format. "
            "Only include main headings and subheadings. The output should be a JSON object following this format: "
            "{\"name\": \"Root\", \"children\": [...]}. Ensure that only 'name' and 'children' keys are used. "
            "Do not include any explanations, code snippets, or text outside the JSON. Provide only the JSON output."
        )

        completion = groq_client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": combined_text
                }
            ],
            temperature=0.3,  # Lower temperature for more deterministic output
            max_tokens=8000,  # Increased max_tokens to allow for larger output
            top_p=0.95,
            stream=False,
            stop=None,
        )

        if not completion.choices:
            logger.error("No choices returned by Groq LLM.")
            return None

        # Get the LLM's raw output
        knowledge_graph_str = completion.choices[0].message.content.strip()
        logger.info("Knowledge graph generated successfully.")

        # Log the raw output for debugging
        logger.debug(f"Raw LLM output:\n{knowledge_graph_str}")

        # Extract the JSON object using regex
        json_match = re.search(r'\{.*\}', knowledge_graph_str, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            try:
                knowledge_graph = json.loads(json_str)
                # Simplify the graph if needed
                def simplify_graph(node):
                    return {
                        "name": node.get("name", ""),
                        "children": [simplify_graph(child) for child in node.get("children", [])]
                    }
                simplified_graph = simplify_graph(knowledge_graph)

                # Set the root node's name if desired
                simplified_graph['name'] = "Your Topic Heading"  # Replace with the desired root name

                knowledge_graph_str = json.dumps(simplified_graph, indent=2)
                return knowledge_graph_str
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing knowledge graph JSON: {e}")
                logger.debug(f"JSON string that failed to parse:\n{json_str}")
                return None
        else:
            logger.error("Could not find JSON object in the LLM output.")
            logger.debug(f"LLM output:\n{knowledge_graph_str}")
            return None

    except Exception as e:
        logger.error(f"Error generating knowledge graph with Groq: {e}")
        return None
