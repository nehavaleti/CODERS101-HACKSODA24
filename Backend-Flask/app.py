from flask import Flask, request, jsonify
import os
from openai import OpenAI
import requests, justext

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"
model_name = "gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)


app = Flask(__name__)

# Load the summarization pipeline
#summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    url = data.get('policyURL', '').strip()
    
    if not url:
        return jsonify({"error": "Policy URL cannot be empty."}), 400
    policyText = ""
    # Extract the privacy policy text
    response = requests.get(url)
    paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            policyText += paragraph.text
    messages = []
    responseData = ""
    for i in range(0, len(policyText), 4096):
        messages = []
        messages.append(
            {
                "role": "user",
                "content": policyText[:4096],
            }
        )
        
        messages.append({
            "role": "user",
            "content": "summarize this and Point out and data privacy and data sharing policies using the above data in less than 100 words",
        })
        response = client.chat.completions.create(
            messages=messages,
            model=model_name,
        )

        responseData += response.choices[0].message.content

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": responseData,
            }
        ],
        model=model_name,
    )

    # Summarize the text
    # summary = summarizer(text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
    # print (response.choices[0].message.content)
    # return jsonify({"summary": policyText})
    return jsonify({"summary": response.choices[0].message.content})