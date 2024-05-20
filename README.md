## Gumroad Scraper and Website Generator
This project is a Python script that scrapes data from a Gumroad site, generates a colorful and well-designed HTML page using OpenAI's GPT-4 model, and deploys the generated page to Vercel.

### Features
Scrape data from a Gumroad site using BeautifulSoup.
Generate a mobile-friendly and visually appealing HTML page with gradient design using OpenAI's GPT-4 model.
Deploy the generated HTML page to Vercel.
### Prerequisites
Before you begin, ensure you have met the following requirements:

You have a recent version of Python (3.7 or newer) installed.
You have a Vercel account and a Vercel API token.
You have OpenAI API access and an OpenAI API key.
You have installed the required Python packages:

login with the Vercel CLI 
```
openai, beautifulsoup4, requests, python-dotenv, vercel
```
### Setup
Clone this repository and navigate to its directory.

Create a .env file in the project directory and add your Vercel and OpenAI API keys:

```
VERCEL_TOKEN=<your_vercel_api_token>
OPENAI_API_KEY=<your_openai_api_key>
```

### Usage
To run the script, execute the following command in your terminal:

```
python gumroad.py
```
The script will prompt you to enter a Gumroad site URL. After providing the URL, it will scrape the data, generate an HTML page, and deploy it to Vercel.


## Sponsors

✨ Find profitable ideas faster: [Exploding Insights](https://explodinginsights.com/)
