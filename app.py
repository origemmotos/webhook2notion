
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
    row.nome = content["name"]
    row.action = content["action_type"]
    row.item = content["item"]
    row.pn = content["part_number"]
    row.quantidade = content["quantity"]
    row.reason = content["reason"]
    row.obs = content["ps"]
    row.ts = content["ts"]

@app.route('/create_record', methods=['GET'])
def create_record():

    content = {
        "name": request.args.get('name'),
        "action_type": request.args.get('action_type'),
        "item": request.args.get('item'),
        "part_number": request.args.get('part_number'),
        "quantity": request.args.get('quantity'),
        "reason": request.args.get('reason'),
        "ps": request.args.get('ps'),
        "ts": request.args.get('ts')
    }
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createNotionRecord(token_v2, url, content)
    return f'added {content} to Notion'

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
