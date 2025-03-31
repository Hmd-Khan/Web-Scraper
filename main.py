import streamlit as st

# Import scraping-related functions from scrape.py
from scrape import (
    scrape_website,         # Launches Chrome via Selenium to fetch webpage HTML.
    clean_body_content,     # Cleans HTML content by removing scripts and styles.
    split_dom_content,      # Splits the cleaned content into smaller chunks.
    extract_body_content,   # Extracts only the <body> section from the HTML.
)

# Import parsing function from parse.py (uses LangChain & OllamaLLM)
from parse import parse_with_ollama

# -----------------------------------------------------------------------------
# User Interface (UI) and Application Logic:
# -----------------------------------------------------------------------------

# Set the title of the Streamlit page
st.title("AI Web Scraper")

# Input widget for the target URL
url = st.text_input("Enter the URL")

# When the "Scrape" button is clicked, perform the web scraping tasks
if st.button("Scrape"):
    st.write("Scraping...")
    # Get raw HTML content from the provided URL
    result = scrape_website(url)
    # Extract only the <body> tag from the HTML
    body_content = extract_body_content(result)
    # Clean the HTML content to remove scripts/styles etc.
    cleaned_content = clean_body_content(body_content)
    # Store the cleaned content into Streamlit session state for later use (e.g., parsing)
    st.session_state.dom_content = cleaned_content

    # Display the cleaned DOM content in an expandable section
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=250)

# If scraped content exists, allow the user to enter a parsing description and process it.
if "dom_content" in st.session_state:
    # Input widget for describing the extraction requirements for parsing.
    parse_description = st.text_area("Describe what u want to parse?")
    
    # When the "Parse Content" button is clicked, start parsing:
    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")
            # Split the cleaned DOM content into chunks for processing by the language model.
            dom_chunks = split_dom_content(st.session_state.dom_content)
            # Call parse_with_ollama from parse.py, passing the text chunks and parsing description.
            result = parse_with_ollama(dom_chunks, parse_description)
            # Display the parsed content in a text area.
            st.text_area("Parsed Content", result, height=250)
