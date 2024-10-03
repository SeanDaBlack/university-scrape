from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import unquote
import re

# Set up Chrome WebDriver
driver = webdriver.Chrome()

# Start URL
start_url = "https://president.columbia.edu/administration"

# List to store extracted emails
emails_list = []

# Set to keep track of visited URLs
visited_urls = set()
visited_urls.add("columbia.edu")


def extract_emails(url):
    try:
        # Check if URL has already been visited
        if url in visited_urls:
            return

        # Add URL to visited set
        visited_urls.add(url)

        driver.get(url)
        # Extract all anchor elements
        anchor_elements = driver.find_elements(By.TAG_NAME, "a")
        for anchor in anchor_elements:
            href = anchor.get_attribute("href")
            if href:
                # Check if href contains '@columbia.edu'
                if "@columbia.edu" in href:
                    email = re.findall(r"[\w\.-]+@[\w\.-]+", unquote(href))
                    if email:
                        emails_list.append({"email": email[0], "link": url})

        # Extract links
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")

            if href:
                if (
                    "blog" in href
                    or "calendar" in href
                    or "news" in href
                    or "files" in href
                ):
                    continue
                elif "president" not in href:
                    continue
                else:
                    extract_emails(href)
    except KeyboardInterrupt:
        return


# Start extraction
extract_emails(start_url)

# Close the WebDriver
driver.quit()

# Print the extracted emails
for email in emails_list:
    print(email)
