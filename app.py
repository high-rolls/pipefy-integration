from flask import Flask
from flask import request
import requests
import json
import re
import os
import rd_station_robot
import shutil


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
			attachments {{
				path
				url
			}}
			fields {{
			field {{
				id
			}}
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
		files = []
		card = data["data"]["card"]
		for attachment in card["attachments"]:
			url = attachment["url"]
			path = attachment["path"]
			match = re.search(".*\/(.*)", path)
			if match:
				shutil.rmtree(f"{card_id}")
				os.mkdir(f"{card_id}")
				file_name = match.group(1)
				data = requests.get(url)
				file_path = f"{card_id}/{file_name}"
				with open(file_path, 'wb') as file:
					file.write(data.content)
					files.append(os.path.abspath(file_path))
					
		nome = None
		email = None
		for field in card["fields"]:
			field_id = field["field"]["id"]
			if field_id == "nome":
				nome = field["value"]
			elif field_id == "email":
				email = field["value"]
		deal_id = rd_station_robot.create_opportunity(nome, email)
		rd_station_robot.upload_deal_files(deal_id, files)

	return f"<h1>{response.text}</h1>"
