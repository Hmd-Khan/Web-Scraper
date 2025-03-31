This module integrates with a language model (via LangChain and OllamaLLM)
to parse and extract specific information from provided text content.
It defines the function parse_with_ollama which:
  1. Accepts chunks of DOM content and a extraction description.
  2. Constructs a prompt with instructions and feeds it to the language model.
  3. Collects and combines responses from individual chunks.

How It Works:
-------------
1. A template is defined with placeholders for the text content (dom_content)
   and the parsing instruction (parse_description).
2. The OllamaLLM language model (set to "wizardlm2") is instantiated.
3. parse_with_ollama() uses a loop to process each text chunk by:
   - Inserting the chunk and description into the prompt.
   - Invoking the chain (prompt | model) to obtain the response.
   - Storing the response in a list.
4. All results are joined to form the final parsed output.

Connection:
-------------
- main.py passes the cleaned and split text (DOM content) and a parsing description
  to parse_with_ollama(), which returns the data extracted by the language model.
