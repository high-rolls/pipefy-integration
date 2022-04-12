from flask import Flask
from flask import request
import requests
import json
import re
import os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
  obj = request.get_json()
  print(json.dumps(obj, indent=4, ensure_ascii=False))
  ACCESS_TOKEN = os.getenv('PIPEFY_TOKEN')
  card_id = obj['data']['card']['id']
  query = f"""
query MyQuery {{
  card(id: {card_id}) {{
    id
    attachments {{
      createdAt
      path
      url
    }}
    fields {{
      filled_at
      name
      value
    }}
  }}
}}
  """
  url = "https://api.pipefy.com/graphql"
  payload = {"query": query}
  headers = {
    "Accept": "application/json",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyIjp7ImlkIjozMDIwMDU2MjYsImVtYWlsIjoiZGV2LnBpcGVmeUBncnVwb3phbm9uLmNvbS5iciIsImFwcGxpY2F0aW9uIjozMDAxNTQyMDZ9fQ.otUVR-VB9hZxHpbv12nc81Q7L4JQakxRKCL_17p_Ph1ZW6urOeOntadeg3fYq8qU8wUvITHm2FhDTFPVQqIa8g",
    "Content-Type": "application/json"
  }

  response = requests.post(url, json=payload, headers=headers)
  data = json.loads(response.text)
  if data:
      data = data["data"]
      for attachment in data["card"]["attachments"]:
        url = attachment["url"]
        path = attachment["path"]
        match = re.search(".*\/(.*)", path)
        if match:
          os.mkdir(f"{card_id}")
          file_name = match.group(1)
          data = requests.get(url)
          with open(file_name, 'wb') as file:
              file.write(data.content)

  return f"<h1>{response.text}</h1>"
