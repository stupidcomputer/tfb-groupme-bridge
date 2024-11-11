from flask import Flask, request, render_template, g, redirect
import requests
from .dbutils import get_and_init_db, get_db
from .groupme import group_sharing_url_to_id, get_oauth_auth_url, custom_get_oauth_auth
import json
import uuid

app = Flask(__name__)
app.config.from_mapping(
    DATABASE_LOCATION = "tfbbridge.sqlite3",
)
app.config.from_file("config.json", load=json.load)

@app.route("/groupme/oauth_callback")
def oauth_callback():
    token = request.args.get("access_token")
    r = requests.get("https://api.groupme.com/v3/groups?token={}".format(token))
    try:
        print(r.text)
        print(token)
        data = r.json()["response"]
    except KeyError:
        return "Couldn't find something", 500
    data = [
        {
            "group_id": i["group_id"],
            "name": i["name"],
        }
    for i in data]

    return render_template("what_group.html", groups=data, token=token)

@app.route("/groupme/add_group", methods=["POST"])
def add_group():
    token = request.form["token"]
    target_group = request.form["to_add"]

    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'token': token,
    }

    json_data = {
        'bot': {
            'name': 'tfbbot',
            'group_id': target_group,
        },
    }

    r = requests.post('https://api.groupme.com/v3/bots', params=params, headers=headers, json=json_data)

    payload = r.json()
    return payload
    bot_id = payload["response"]["bot"]["bot_id"]
    group_name = payload["response"]["bot"]["group_name"]
    group_id = payload["response"]["bot"]["group_id"]

    db = get_db()
    try:
        db.execute(
            "INSERT INTO channels (group_name, group_id, bot_id, chan_type, organization)"
        )

    return r.text

@app.route("/groupme/authorize")
def authorize():
    return redirect(get_oauth_auth_url())

@app.route("/groupme/create_organization", methods=["GET", "POST"])
def create_organization():
    if request.method == "GET":
        return render_template("new_org.html")
    elif request.method == "POST":
        name = request.form["orgname"]

        db = get_db()
        try:
            db.execute(
                "INSERT INTO organizations (org_name, admin_url, addition_url) VALUES (?, ?, ?)",
                (name, uuid.uuid4().hex, uuid.uuid4().hex,),
            )
            db.commit()

            return "testing"
        except db.IntegrityError:
            return "This group is already registered."

@app.route("/groupme/list_orgs")
def list_orgs():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM organizations')
    results = cursor.fetchall()
    results = [(i[0], i[1], i[2], i[3]) for i in results]
    print(results)
    return results

@app.route("/groupme/org_info/<org>")
def org_info(org):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, org_name FROM organizations WHERE admin_url=?', (org,))
    org_id, name = cursor.fetchone()

    cursor.execute('SELECT group_name, group_id, bot_id, chan_type FROM channels WHERE organization=?', (org_id,))
    results = cursor.fetchall()
    results = [
        {
            "name": i[0],
            "group_id": i[1],
            "bot_id": i[2],
            "chan_type": i[3],
        }
    for i in results]
    return results

@app.route("/groupme/add_chan_to_org/<org>")
def add_chan_to_org(org):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, org_name FROM organizations WHERE addition_url=?', (org,))
    org_id, name = cursor.fetchone()
    return redirect(
        "https://oauth.groupme.com/oauth/authorize?client_id=qAAAc8GSUlTA8C3Ypo9CMiFQwQCQnU8zPU5KGEtz3FYHDqP5&response_type=token"
    )