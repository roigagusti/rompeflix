from flask import Flask, render_template, session, request, redirect, url_for
from classes.Airtable import Airtable
from classes.functions import dateToYear
from classes.private import atCredentials
from flask_login import UserMixin
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
def low(a):
    return a.lower()
def initials(a):
    x = a.split(' ')[0][0] + a.split(' ')[1][0]
    return x.upper()


### APP ###
#-- PROVES --#
@app.route("/history")
def history():
    if not session.get("user"):
        return redirect(url_for("login"))
    username = session["user"].get("name")
    return render_template('history.html',user=username,initials=initials(username))
@app.route("/my-list")
def myList():
    if not session.get("user"):
        return redirect(url_for("login"))
    username = session["user"].get("name")
    return render_template('my-list.html',user=username,initials=initials(username))

@app.route("/prova")
def prova():
    userExists = dbHas('rompeflix_users',where="miid='6610bd4a-bf42-4bbb-ba1d-37ff91cba8f'")
    return render_template('prova.html',miid=userExists)

@app.route("/validar",methods=['POST'])
def validar():
    rtid = request.form['id']
    name = request.form['name']
    email = request.form['email']
    #dbprova = dbInsert('rompeflix_users','miid,name,email',"'"+rtid+"','"+name+"','"+email+"'")
    #dbprova = dbSelect('rompeflix_users','name,email',limit=2,offset=3)
    #dbprova = dbUpdate('rompeflix_users',"name='"+name+"',email='"+email+"'","miid='gsfdgdsg'")
    return redirect(url_for("prova"))


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