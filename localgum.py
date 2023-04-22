import json
import os
from pathlib import Path

import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

catppuccin_mocha = """Labels 	Hex 	RGB 	HSL
	Rosewater 	#f5e0dc 	rgb(245, 224, 220) 	hsl(10, 56%, 91%)
	Flamingo 	#f2cdcd 	rgb(242, 205, 205) 	hsl(0, 59%, 88%)
	Pink 	#f5c2e7 	rgb(245, 194, 231) 	hsl(316, 72%, 86%)
	Mauve 	#cba6f7 	rgb(203, 166, 247) 	hsl(267, 84%, 81%)
	Red 	#f38ba8 	rgb(243, 139, 168) 	hsl(343, 81%, 75%)
	Maroon 	#eba0ac 	rgb(235, 160, 172) 	hsl(350, 65%, 77%)
	Peach 	#fab387 	rgb(250, 179, 135) 	hsl(23, 92%, 75%)
	Yellow 	#f9e2af 	rgb(249, 226, 175) 	hsl(41, 86%, 83%)
	Green 	#a6e3a1 	rgb(166, 227, 161) 	hsl(115, 54%, 76%)
	Teal 	#94e2d5 	rgb(148, 226, 213) 	hsl(170, 57%, 73%)
	Sky 	#89dceb 	rgb(137, 220, 235) 	hsl(189, 71%, 73%)
	Sapphire 	#74c7ec 	rgb(116, 199, 236) 	hsl(199, 76%, 69%)
	Blue 	#89b4fa 	rgb(137, 180, 250) 	hsl(217, 92%, 76%)
	Lavender 	#b4befe 	rgb(180, 190, 254) 	hsl(232, 97%, 85%)
	Text 	#cdd6f4 	rgb(205, 214, 244) 	hsl(226, 64%, 88%)
	Subtext1 	#bac2de 	rgb(186, 194, 222) 	hsl(227, 35%, 80%)
	Subtext0 	#a6adc8 	rgb(166, 173, 200) 	hsl(228, 24%, 72%)
	Overlay2 	#9399b2 	rgb(147, 153, 178) 	hsl(228, 17%, 64%)
	Overlay1 	#7f849c 	rgb(127, 132, 156) 	hsl(230, 13%, 55%)
	Overlay0 	#6c7086 	rgb(108, 112, 134) 	hsl(231, 11%, 47%)
	Surface2 	#585b70 	rgb(88, 91, 112) 	hsl(233, 12%, 39%)
	Surface1 	#45475a 	rgb(69, 71, 90) 	hsl(234, 13%, 31%)
	Surface0 	#313244 	rgb(49, 50, 68) 	hsl(237, 16%, 23%)
	Base 	#1e1e2e 	rgb(30, 30, 46) 	hsl(240, 21%, 15%)
	Mantle 	#181825 	rgb(24, 24, 37) 	hsl(240, 21%, 12%)
	Crust 	#11111b 	rgb(17, 17, 27) 	hsl(240, 23%, 9%)
"""  # noqa: E101


def scrape_gumroad_data(url):
    try:
        # Send an HTTP request to the provided URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the status code is not 2xx
    except requests.exceptions.RequestException as e:
        print("Failed to fetch the Gumroad site:")
        print(str(e))
        return None

    # Parse the response HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract relevant data using CSS selectors (modify based on actual data)
    rich_text_elements = soup.select(".rich-text")
    all_elements = " ".join(
        [element.get_text(strip=True) for element in rich_text_elements]
    )

    return all_elements


def generate_website(gumroad_data):
    # Construct the prompt for the GPT model
    prompt = f"Generate an HTML that is colorful and well designed. Use gradient where it is reasonable. Make the website mobile friendly and SEO optimized meta tags. Use this CSS template: {catppuccin_mocha}. Add a call to action button with the URL. Include the following text: {gumroad_data}"  # noqa: E501

    # Call the OpenAI API for chat completion
    response = openai.ChatCompletion.create(
        model="gpt-4",
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


def save_website(html_content: str, project_name: str):
    # Set the project directory
    project_dir = Path.cwd() / project_name
    os.makedirs(project_dir, exist_ok=True)

    # Write the HTML content to the index.html file
    with open(project_dir / "index.html", "w") as f:
        f.write(html_content)

    # Write the JSON configuration file
    config = {
        "name": project_name,
        "version": 2,
    }

    with open(project_dir / "config.json", "w") as f:
        json.dump(config, f)

    # Print the location of the generated files
    print(f"Site generated at {project_dir}")


def main(project_name: str):
    # Read the Gumroad website URL
    gumroad_site = input("Enter the Gumroad site: ")

    # Scrape the data from the Gumroad website
    scraped_data = scrape_gumroad_data(gumroad_site)
    print("\nGenerating the site...\n")

    # Generate the HTML content using the GPT model
    html_content = generate_website(scraped_data)

    # Save the generated HTML to local files
    save_website(html_content, project_name)


# Run the main function with the provided project name
if __name__ == "__main__":
    project_name = input("Enter the project name: ")
    main(project_name)
