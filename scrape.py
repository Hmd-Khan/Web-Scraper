import streamlit as st
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup

def scrape_website(website):
    # Notify the user via Streamlit that the browser is launching
    st.write("Launching chrome browser...")

    # Validate the URL scheme; if missing, prepend "https://"
    if not (website.startswith("http://") or website.startswith("https://")):
        website = "https://" + website

    # Specify the path to the ChromeDriver executable
    chrome_driver_path = "./chromedriver.exe"
    option = webdriver.ChromeOptions()
    
    # Add options to reduce SSL, GPU, and sandbox related errors
    option.add_argument("--ignore-certificate-errors")
    option.add_argument("--disable-gpu")
    option.add_argument("--no-sandbox")
    # Optionally run headless (without a visible browser window)
    # option.add_argument("--headless")

    # Instantiate a Chrome driver with the specified options
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=option)
    
    try:
        # Navigate to the target website
        driver.get(website)
        st.write("Page loaded...")
        # Get the page source (HTML content)
        html = driver.page_source
        # Pause to ensure content is fully loaded; adjust time as necessary
        time.sleep(10)
        return html
    finally:
        # Close the browser instance to free resources
        driver.quit()

def extract_body_content(html):
    """
    Extract the <body> element from the HTML.
    If no <body> is found, return full HTML.
    """
    soup = BeautifulSoup(html, "html.parser")
    return str(soup.body) if soup.body else html

def clean_body_content(body_content):
    """
    Remove script and style elements from the HTML.
    Returns a cleaned text version of the content.
    """
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    # Get text with newline-separated values; whitespace stripped
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, max_length=1000):
    """
    Split text into smaller chunks of at most max_length characters.
    This helps to avoid hitting input limits when processing lengthy texts.
    """
    return [
        dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)
    ]

def main():
    # Provide a minimal UI for standalone testing of web scraping functionality.
    st.title("AI Web Scraper")
    url = st.text_input("Enter the URL")
    
    if st.button("Scrape"):
        if url:
            html = scrape_website(url)
            cleaned_content = clean_body_content(html)
            st.text_area("Cleaned DOM Content", cleaned_content, height=300)
        else:
            st.error("Please input a URL.")

# If this module is run directly, execute main() for quick testing.
if __name__ == "__main__":
    main()
