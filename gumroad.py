import json
import os
import subprocess
import tempfile
from pathlib import Path

import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get Vercel and OpenAI API keys from environment variables
VERCEL_TOKEN = os.environ.get("VERCEL_TOKEN")
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Set the desired Vercel website name
vercel_website_name = "pesmasterplus"


def scrape_gumroad_data(url):
    # Send an HTTP request to the provided URL
    response = requests.get(url)
    # Parse the response HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract relevant data using CSS selectors (modify based on actual data)
    rich_text_elements = soup.select(".rich-text")
    all_elements = " ".join(
        [element.get_text(strip=True) for element in rich_text_elements]
    )

    return all_elements


def deploy_to_vercel(html_content: str, project_name: str, vercel_token: str):
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set the project directory
        project_dir = Path(temp_dir) / project_name
        os.makedirs(project_dir)

        # Write the HTML content to the index.html file
        with open(project_dir / "index.html", "w") as f:
            f.write(html_content)

        # Write the vercel.json configuration file
        vercel_config = {
            "name": project_name,
            "version": 2,
            "builds": [{"src": "index.html", "use": "@vercel/static"}],
        }

        with open(project_dir / "vercel.json", "w") as f:
            json.dump(vercel_config, f)

        # Deploy to Vercel using the CLI
        cmd = ["vercel", "--token", vercel_token, "-y", "--prod"]

        result = subprocess.run(cmd, cwd=project_dir, capture_output=True, text=True)

        if result.returncode == 0:
            print("Deployment successful!")
            print(f"Deployment URL: {result.stdout.strip()}")
        else:
            print("Deployment failed:")
            print(result.stderr)


def generate_website(gumroad_data):
    # Construct the prompt for the GPT model
    prompt = f"Generate an HTML that is colorful and well designed. Use gradient where it is reasonable. Make the website mobile friendly and SEO optimized. Include the following text: {gumroad_data}"  # noqa: E501

    # Call the OpenAI API for chat completion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a senior frontend designer. I need you to write the frontend code.",  # noqa: E501
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=1200,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Extract the generated HTML from the response
    reply = response["choices"][0]["message"]["content"]
    return reply


def main(project_name: str, vercel_token: str):
    # Read the HTML file
    gumroad_site = input("Enter the gumroad site: ")

    # Scrape the data from the Gumroad website
    scraped_data = scrape_gumroad_data(gumroad_site)
    print("\nGenerating the site for you now ser 🫡 \n")

    # Generate the HTML content using the GPT model
    html_content = generate_website(scraped_data)

    # Deploy the generated HTML to Vercel
    deploy_to_vercel(html_content, project_name, vercel_token)


# Run the main function with the provided website name and Vercel token
if __name__ == "__main__":
    main(vercel_website_name, str(VERCEL_TOKEN))
