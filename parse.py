from langchain_ollama import OllamaLLM  # Importing the OllamaLLM model for language processing
from langchain_core.prompts import ChatPromptTemplate  # Importing ChatPromptTemplate for prompt creation

# Template for the prompt used to extract specific information from text content
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Initializing the language model with a specific configuration
model = OllamaLLM(model="wizardlm2")


def parse_with_ollama(dom_chunks, parse_description):
    """
    Parses a list of DOM content chunks using the Ollama language model.

    Args:
        dom_chunks (list): A list of text chunks representing DOM content.
        parse_description (str): A description of the information to extract.

    Returns:
        str: A concatenated string of parsed results.
    """
    # Create a prompt chain using the template and the language model
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []  # List to store parsed results

    # Iterate over each chunk of DOM content
    for i, chunk in enumerate(dom_chunks, start=1):
        # Invoke the chain with the current chunk and parse description
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed batch: {i} of {len(dom_chunks)}")  # Log progress
        parsed_results.append(response)  # Append the response to results

    # Join all parsed results into a single string and return
    return "\n".join(parsed_results)