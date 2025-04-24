import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import os

def scrape_url_to_json(url, output_dir="prompts"):
    try:
        # Fetch the page
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)

        # Create output JSON structure
        domain = urlparse(url).netloc.replace(".", "_")
        data = {
            "source": url,
            "domain": domain,
            "content": text
        }

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{domain}.json"
        output_path = os.path.join(output_dir, filename)

        # Save to file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"[+] Scraped data saved to: {output_path}")
        return output_path

    except Exception as e:
        print(f"[Error] Failed to scrape {url}: {str(e)}")
        return None

# Example usage:
if __name__ == "__main__":
    test_url = input("Enter a URL to scrape: ")
    scrape_url_to_json(test_url)
