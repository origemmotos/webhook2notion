
import os
from notion.client import NotionClient
from flask import Flask
from flask import request


app = Flask(__name__)

def createNotionTask(token, collectionURL, content):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.title = content

@app.route('/create_todo', methods=['GET'])
def create_todo():

    todo = request.args.get('todo')
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createNotionTask(token_v2, url, todo)
    return f'added {todo} to Notion'

def createNotionRecord(token, collectionURL, content):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.name = content["name"]
    row.field1 = content["field1"]

@app.route('/create_record', methods=['GET'])
def create_record():

    content = {
        "name": request.args.get('name'),
        "field1": request.args.get('field1')
    }
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createNotionRecord(token_v2, url, content)
    return f'added {content} to Notion'

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
