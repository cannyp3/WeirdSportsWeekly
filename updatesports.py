from openai import OpenAI
from datetime import datetime
import pytz
import os
import re

# Access the API key from environment variable
api_key = os.environ.get('PERPLEXITY_API_KEY')
if not api_key:
    raise ValueError("PERPLEXITY_API_KEY environment variable is not set")


# Initialize Perplexity client
client = OpenAI(
    api_key=api_key,
    base_url="https://api.perplexity.ai"
)

def clean_perplexity_response(text):
    # Remove bracketed references at the end of sentences
    pattern = r'\[\d+\]'
    cleaned_text = re.sub(pattern, '', text)
    # Fix extra space before periods
    cleaned_text = cleaned_text.replace(' .', '.')
    return cleaned_text

def get_sports_summary():
    messages = [
        {
            "role": "system",
            "content": "Search the web for three unusual, bizarre, or weird sports news stories from the past few years. Focus on odd events, strange coincidences, or peculiar incidents in sports. Provide a short paragraph summary for each story."
        },
        {
            "role": "user",
            "content": "What are three weird sports news stories from the past few years?"
        }
    ]
    
    response = client.chat.completions.create(
        model="llama-3.1-sonar-small-128k-online",
        messages=messages
    )

    # Clean the response before returning it
    raw_content = response.choices[0].message.content
    cleaned_content = clean_perplexity_response(raw_content)
    return cleaned_content


def update_html():
  
    summary = get_sports_summary()
    if not summary:
        raise ValueError("Failed to retrieve sports summary")
    timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S EST')
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Odd Sports Update</title>
        <link rel="stylesheet" href="styles.css">
        <script src="https://unpkg.com/showdown/dist/showdown.min.js"></script>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <h1>Odd Sports News Summary</h1>
        <p>Last updated: {timestamp}</p>
        <div id="content"></div>
        <script>
            const converter = new showdown.Converter();
            const markdown = `{summary}`;
            document.getElementById('content').innerHTML = converter.makeHtml(markdown);
        </script>
    </body>
    </html>
    """
    
    with open('index.html', 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    update_html()
