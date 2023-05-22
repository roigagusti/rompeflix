from flask import Flask, render_template, session, request, redirect, url_for
from classes.functions import dateToYear
from classes.private import atCredentials
from classes.db import dbInsert,dbSelect,dbUpdate,dbHas,Rompetechos
import timeago, datetime
# PROVES

# Importacions per LoginWithMicrosoft
import requests
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
#at = Airtable(token,base_id)
rt = Rompetechos('rompeflix_media')



# CLASSES

# FUNCTIONS
def low(str):
    return str.lower()
def initials(longName):
    name = longName.replace("  "," ")
    arrayName = name.split(' ')
    initial = arrayName[0][0] + arrayName[1][0]
    return initial.upper()


### APP ###
#-- PROVES --#
@app.route("/my-list")
def myList():
    if not session.get("user"):
        return redirect(url_for("login"))
    favourite = dbSelect('rompeflix_favourites','media_id',"user_miid='1'",limit=10)
    demos = []
    for item in favourite:
        demoday = rt.record(item[0])
        demos.append(demoday)
    username = session["user"].get("name")
    return render_template('my-list.html',content=demos,user=username,initials=initials(username))


#-- PRODUCCIÓ --#
@app.route("/",methods=['GET'])
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    resposta = []
    sliderMain = rt.list(4,'slider_main','Yes')
    lastestReleases = rt.list(8)
    demoday = rt.list(50,'category','Demoday')
    tech = rt.list(50,'area','IT')
    buildingsystem = rt.list(50,'area','Building System')
    if request.args.get('q'):
        query = low(request.args.get('q'))
        find = rt.list(50, 'estat', 'active')
        for record in find:
            if query in low(record.title):
                resposta.append(record)
            elif query in low(record.area):
                resposta.append(record)
    username = session["user"].get("name")
    return render_template('home.html',user=username,initials=initials(username),sliderMain=sliderMain,lastestReleases=lastestReleases,demoday=demoday,tech=tech,buildingsystem=buildingsystem,resposta=resposta)

@app.route('/movie-details',methods=['GET'])
def movieDetails():
    atid = request.args.get('id')
    data = rt.record(atid)
    year = dateToYear(data.release_date)
    if not session.get("user"):
        return redirect(url_for("login"))
    username = session["user"].get("name")
    history = dbInsert('rompeflix_history','user_miid,media_id',"'"+session["user"].get("oid")+"','"+atid+"'")
    return render_template('movie-details.html',user=username,initials=initials(username),data=data,year=year)

# Demodays
@app.route('/demodays',methods=['GET'])
def demoDays():
    if not session.get("user"):
        return redirect(url_for("login"))
    demodays = rt.list(500,'category','Demoday')
    title = 'Demodays'
    initial = 0
    username = session["user"].get("name")
    return render_template('category.html',initial=initial,user=username,initials=initials(username),demodays=demodays,title=title)

# Area content
@app.route('/content-<area>',methods=['GET'])
def areaContent(area):
    if not session.get("user"):
        return redirect(url_for("login"))
    categoryArea = 'Content area-'+area
    content = rt.list(500,'categoryArea',categoryArea)
    title = 'Area content. '+ area
    initial = 0
    if len(content) == 0:
        initial = 1
    username = session["user"].get("name")
    return render_template('category.html',initial=initial,user=username,initials=initials(username),demodays=content,title=title)

# Company trainings
@app.route('/trainings',methods=['GET'])
def trainings():
    if not session.get("user"):
        return redirect(url_for("login"))
    # LPS
    area = 'LPS'
    categoryArea = 'Training-'+area
    lps = rt.list(500,'categoryArea',categoryArea)
    initial = 0
    username = session["user"].get("name")
    return render_template('training.html',initial=initial,user=username,initials=initials(username),lps=lps)


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
        demoday = rt.record(item[0])
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
    return render_template("login.html", auth_url=session["flow"]["auth_uri"])

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