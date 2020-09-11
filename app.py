
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

def createNotionTask_recebimento(token, collectionURL_recebimento, content_recebimento):
    # notion
    client_recebimento = NotionClient(token)
    cv_recebimento = client.get_collection_view(collectionURL_recebimento)
    row_recebimento = cv_recebimento.collection.add_row()
    row_recebimento.title = content_recebimento

@app.route('/create_todo_estoque', methods=['GET'])
def create_todo_estoque():

    todo = request.args.get('todo')
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createNotionTask(token_v2, url, todo)
    return f'added {todo} to Notion'

@app.route('/create_todo_recebimento', methods=['GET'])
def create_todo_recebimento():

    todo_recebimento = request.args.get('todo_recebimento')
    token_v2 = os.environ.get("TOKEN")
    url_recebimento = os.environ.get("url_recebimento")
    createNotionTask(token_v2, url_recebimento, todo_recebimento)
    return f'added {todo_recebimento} to Notion'

def getItemRelation(token, collectionURL, itemName):
    cv = client.get_collection_view(collectionURL)
    items = cv.collection.get_rows(search=itemName)
    # notion-py search/query is not working, searching for item within items list
    item = [i for i in items if i.Part == itemName]
    return item

def getnameRelation(token, collectionURL_recebimento, name):
    cv_recebimento = client_recebimento.get_collection_view(collectionURL_recebimento)
    names = cv_recebimento.collection.get_rows(search=name)
    # notion-py search/query is not working, searching for item within items list
    name = [i for i in items if i.Part == name]
    return name

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

def createNotionRecord_recebimento(token, collectionURL_recebimento, urlname, content_recebimento):
    # notion
    client_recebimento = NotionClient_recebimento(token)
    cv_recebimento = client_recebimento.get_collection_view(collectionURL_recebimento)
    # retrieve item from items collection
    name = getnameRelation(token, urlname, content["name"])
    if (name == None):
	print("Name '{}' not found in related database".format(content_recebimento["name"]))
	return -1
    row_recebimento = cv_recebimento.collection.add_row()
    row_recebimento.nome = content_recebimento["name"]
    row_recebimento.action = content_recebimento["action_type"]
    row_recebimento.item = item
    row.pn = content_recebimento["part_number"]
    row.quantidade = content_recebimento["quantity"]
    row.reason = content_recebimento["reason"]
    row.obs = content_recebimento["ps"]
    row.ts = content_recebimento["ts"]
    return 0

@app.route('/create_record_recebimento', methods=['GET'])
def create_record_recebimento():
    content_recebimento = {
        "name": request.args.get('name'),
        "action_type": request.args.get('action_type'),
        "item": request.args.get('item'),
        "part_number": request.args.get('part_number'),
        "quantity": request.args.get('quantity'),
        "reason": request.args.get('reason'),
        "ps": request.args.get('ps'),
        "ts": request.args.get('ts')
    }

    token_v2 = os.environ.get("token")
    url_recebimento = os.environ.get("url_recebimento")
    urlname = os.environ.get("url_name")
    r_recebimento = createNotionRecord(token_v2, url_recebimento, urlname, content_recebimento)
    if (r_recebimento == 0):
        return f'added {content_recebimento} to Notion'
    else:
	return f'failed to add {content_recebimento} to Notion'

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
