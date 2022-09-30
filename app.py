from flask import Flask, render_template, session, request, redirect, url_for
from classes.Airtable import Airtable
from classes.functions import dateToYear
from classes.private import atCredentials
from classes.db import dbInsert,dbSelect,dbUpdate,dbHas
#from sqlalchemy import Column, Integer, String, Float
from flask_login import UserMixin
import timeago, datetime
# PROVES
from classes.db import dbInsert,dbSelect,dbUpdate,dbHas
from sqlalchemy import Column, Integer, String, Float

# Importacions per LoginWithMicrosoft
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
import app_config
from classes.functionsMicrosoft import _load_cache, _save_cache, _build_msal_app, _build_auth_code_flow, _get_token_from_cache

# Iniciem la APP
app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

# Necessari per quan es treballa en localhost
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Iniciem la base de dades
token,base_id = atCredentials()
at = Airtable(token,base_id)



# CLASSES
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = '******'
        self.password = '******'

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

# FUNCTIONS
def low(str):
    return str.lower()
def initials(longName):
    arrayName = longName.split(' ')
    initial = arrayName[0][0] + arrayName[1][0]
    return initial.upper()


### APP ###
#-- PROVES --#
@app.route("/my-list")
def myList():
    favourite = dbSelect('rompeflix_favourites','media_id',"user_miid='1'",limit=10)
    demos = []
    for item in favourite:
        demoday = at.record(item[0])
        demos.append(demoday)
    if not session.get("user"):
        return redirect(url_for("login"))
    username = session["user"].get("name")
    return render_template('my-list.html',content=demos,user=username,initials=initials(username))

@app.route("/prova")
def prova():
    name = "Sandra Regué"
    a = initials(name)
    return render_template('prova.html',print=a)


#-- PRODUCCIÓ --#
@app.route("/",methods=['GET'])
def index():
    resposta = []
    sliderMain = at.list(4,'slider_main','Yes')
    lastestReleases = at.list(7,'last_release','Yes')
    demoday = at.list(50,'tag','Demoday')
    techdemo = at.list(50,'tag','Tech demo')
    components = at.list(50,'tag','Components demo')
    if request.args.get('q'):
        query = low(request.args.get('q'))
        find = at.list(500, 'status', 'active')
        for record in find:
            if query in low(record.title):
                resposta.append(record)
            elif query in low(record.squad):
                resposta.append(record)
    if not session.get("user"):
        return redirect(url_for("login"))
    username = session["user"].get("name")
    return render_template('home.html',user=username,initials=initials(username),sliderMain=sliderMain,lastestReleases=lastestReleases,demoday=demoday,techdemo=techdemo,components=components,resposta=resposta)

@app.route('/movie-details',methods=['GET'])
def movieDetails():
    atid = request.args.get('id')
    data = at.record(atid)
    year = dateToYear(data.release_date)
    if not session.get("user"):
        return redirect(url_for("login"))
    username = session["user"].get("name")
    history = dbInsert('rompeflix_history','user_miid,media_id',"'"+session["user"].get("oid")+"','"+atid+"'")
    return render_template('movie-details.html',user=username,initials=initials(username),data=data,year=year)

@app.route('/demodays',methods=['GET'])
def demoDays():
    sliderMain = at.list(4,'slider_main','Yes')
    demodays = at.list(500,'tag','Demoday')
    title = 'Demodays'
    if not session.get("user"):
        return redirect(url_for("login"))
    username = session["user"].get("name")
    return render_template('category.html',user=username,initials=initials(username),sliderMain=sliderMain,demodays=demodays,title=title)

@app.route('/tech-releases',methods=['GET'])
def techReleases():
    sliderMain = at.list(4,'slider_main','Yes')
    demodays = at.list(500,'tag','Tech demo')
    title = 'Tech releases'
    if not session.get("user"):
        return redirect(url_for("login"))
    username = session["user"].get("name")
    return render_template('category.html',user=username,initials=initials(username),sliderMain=sliderMain,demodays=demodays,title=title)

@app.route('/components',methods=['GET'])
def components():
    sliderMain = at.list(4,'slider_main','Yes')
    demodays = at.list(500,'tag','Components demo')
    title = 'Components'
    if not session.get("user"):
        return redirect(url_for("login"))
    username = session["user"].get("name")
    return render_template('category.html',user=username,initials=initials(username),sliderMain=sliderMain,demodays=demodays,title=title)

# User Stuff
@app.route("/history")
def history():
    if not session.get("user"):
        return redirect(url_for("login"))
    username = session["user"].get("name")
    initial = 0
    history = dbSelect('rompeflix_history','media_id,created',"user_miid='"+session["user"].get("oid")+"'",orderby='created DESC',limit=10)
    demos = []
    for item in history:
        time = timeago.format(item[1], datetime.datetime.now())
        demoday = at.record(item[0])
        historyDemo = [demoday,time]
        appendDemo = True
        for demo in demos:
            if demo[0].id == historyDemo[0].id:
                appendDemo = False
        if appendDemo:
            demos.append(historyDemo)
    if len(demos) == 0:
        initial = 1
    return render_template('history.html',initial=initial,content=demos,user=username,initials=initials(username))


# Login Stuff
@app.route("/login")
def login():
    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
    return render_template("landing.html", auth_url=session["flow"]["auth_uri"])

@app.route(app_config.REDIRECT_PATH)
def authorized():
    try:
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")

        userExists = dbHas('rompeflix_users',where="miid='"+session["user"].get("oid")+"'")
        if not userExists:
            dbInsert('rompeflix_users','miid,name,email',"'"+session["user"].get("oid")+"','"+session["user"].get("name")+"','"+session["user"].get("preferred_username")+"'")
        _save_cache(cache)
    except ValueError:
        pass
    return redirect(url_for("index"))

@app.route("/display")
def graphcall():
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    graph_data = requests.get(  # Use token to call downstream service
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()
    return render_template('display.html', result=graph_data)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))


app.jinja_env.globals.update(_build_auth_code_flow=_build_auth_code_flow)  # Used in template

if __name__ == "__main__":
    app.run()