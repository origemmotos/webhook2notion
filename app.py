
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

def getItemRelation(token, collectionURL, itemName):
    cv = client.get_collection_view(collectionURL)
    items = cv.collection.get_rows(search=itemName)
    # notion-py search/query is not working, searching for item within items list
    item = [i for i in items if i.Part == itemName]
    return item

def createNotionRecord(token, collectionURL, urlItems, content):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    # retrieve item from items collection
    item = getItemRelation(token, urlItems, content["item"])
    if (item == None):
	print("Item '{}' not found in related database".format(content["item"]))
	return -1
    row = cv.collection.add_row()
    row.nome = content["name"]
    row.action = content["action_type"]
    row.item = item
    row.pn = content["part_number"]
    row.quantidade = content["quantity"]
    row.reason = content["reason"]
    row.obs = content["ps"]
    row.ts = content["ts"]
    return 0

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
    urlItems = os.environ.get("URL_ITEMS")
    r = createNotionRecord(token_v2, url, urlItems, content)
    if (r == 0):
        return f'added {content} to Notion'
    else:
	return f'failed to add {content} to Notion'

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
