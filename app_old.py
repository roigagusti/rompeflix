from flask import Flask, render_template, request, redirect, url_for
from classes.Airtable import Airtable
from classes.Rompetechos import Rompetechos
from classes.functions import dateToYear
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

at = Airtable()

# CLASSES
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = 'admin011h'
        self.password = '011habitant'

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

# FUNCTIONS
def low(a):
    return a.lower()



# APP
app = Flask(__name__)

# Configurar login
app.config.update(
    DEBUG = True,
    SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
)
# Flask login
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"

# Crear users
users = [User(1)]



# Inici de la APP
@app.route('/',methods=['GET'])
@login_required
def index(): # Home page
    resposta = []
    sliderMain = at.list(4,'slider_main','Yes')
    lastReleases = at.list(7,'last_release','Yes')
    demoday = at.list(50,'tag','Demoday')
    techdemo = at.list(50,'tag','Tech demo')
    components = at.list(50,'tag','Components demo')
    if request.args.get('q'):
        query = low(request.args.get('q'))
        find = at.list(500, 'status', 'active')
        for record in find:
            if query in low(record.title):
                resposta.append(record)
            elif query in low(record.main_style):
                resposta.append(record)
    return render_template('home.html',sliderMain=sliderMain,lastReleases=lastReleases,demoday=demoday,techdemo=techdemo,components=components,resposta=resposta)

@app.route('/movie-details',methods=['GET'])
@login_required
def movieDetails():
    atid = request.args.get('id')
    data = at.record(atid)
    year = dateToYear(data.release_date)
    return render_template('movie-details.html',data=data,year=year)

@app.route('/demodays',methods=['GET'])
@login_required
def demoDays():
    sliderMain = at.list(4,'slider_main','Yes')
    demodays = at.list(500,'tag','Demoday')
    title = 'Demodays'
    return render_template('category.html',sliderMain=sliderMain,demodays=demodays,title=title)

@app.route('/tech-releases',methods=['GET'])
@login_required
def techReleases():
    sliderMain = at.list(4,'slider_main','Yes')
    demodays = at.list(500,'tag','Tech demo')
    title = 'Tech releases'
    return render_template('category.html',sliderMain=sliderMain,demodays=demodays,title=title)

@app.route('/components',methods=['GET'])
@login_required
def components():
    sliderMain = at.list(4,'slider_main','Yes')
    demodays = at.list(500,'tag','Components demo')
    title = 'Components'
    return render_template('category.html',sliderMain=sliderMain,demodays=demodays,title=title)

# Gestió d'usuaris: Login i Logout
@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('landing.html')

@app.route('/validate', methods=['GET','POST'])
def validate():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        if username == 'admin011h' and password == '011habitant':
            user = User(1)
            login_user(user)
            return redirect('/')
        else:
            return redirect('/login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



# Load the user
@login_manager.user_loader
def load_user(userid):
    return User(userid)