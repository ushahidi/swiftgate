__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"


from flask import Flask, render_template, request, redirect, current_app, url_for, session
from thegateway.utils import validate_signin_form, validate_add_app_form
from thegateway.utils import build_app_stats_for_app_id
from thegateway.utils import validate_signup_form
from flaskext.principal import Principal, Permission, RoleNeed, Identity, identity_changed
from flaskext.principal import identity_loaded
from domain.utils import con
from domain.utils import get_authenticated_user_by_riverid
from domain.utils import get_authenticated_user_by_id
from domain.utils import get_all_price_plans_for_app_template
from domain.utils import create_new_subscription
from domain.utils import get_subscription_by_id
from domain.utils import get_api_wrapper_by_identifier
from domain.models import *
from thegateway.captchasdotnet import CaptchasDotNet
import time
import hashlib

app = Flask(__name__)

principals = Principal(app)

userPermission = Permission(RoleNeed('user'))

@app.route('/', methods=['GET', 'POST'])
def index():
    captchas = CaptchasDotNet(client='demo', secret='secret', alphabet='abcdefghkmnopqrstuvwxyz', letters=6, width=330, height=80)
    captchas_data = {
        'captchas_random':captchas.random(),
        'captchas_image':captchas.image(),
        'captchas_audio':captchas.audio_url()
    }
    if request.method == 'POST':
        if 'signIn' in request.form:
            passed, errors = validate_signin_form(request.form)
            if not passed:
                return render_template('index.html', signInErrors=errors, riverId=request.form.get('riverId'), captchas_data=captchas_data)
            identity_changed.send(current_app._get_current_object(), identity=Identity(request.form.get('riverId')))
            return redirect(url_for('user_home'))
        if 'signOut' in request.form:
            identity_changed.send(current_app._get_current_object(), identity=Identity('guest'))
        if 'signUp' in request.form:
            passed, errors = validate_signup_form(request.form, captchas)
            if not passed:
                return render_template('index.html', signUpErrors=errors, riverId=request.form.get('riverId'), emailaddress=request.form.get('emailaddress'), captchas_data=captchas_data)
            identity_changed.send(current_app._get_current_object(), identity=Identity(request.form.get('riverId')))
            return redirect(url_for('user_home'))
    return render_template('index.html', captchas_data=captchas_data)




@app.route('/yourgateway', methods=['GET', 'POST'])
@userPermission.require(http_exception=401)
def user_home():
    user = get_authenticated_user_by_id(session['user_id'])
    app_stats = {}
    for user_app in user.apps:
        app_id = unicode(user_app.key)
        app_stats[app_id] = build_app_stats_for_app_id(app_id)
    if request.method == 'GET':
        return render_template("account/home.html", user=user, app_stats=app_stats)
    else:
        if 'add-app' in request.form :
            passed, errors = validate_add_app_form(request.form, user)
            if not passed:
                return render_template("account/home.html", user=user, addAppErrors=errors, appName=request.form.get('appName'), appTemplate=request.form.get('appTemplate'), pricePlan=request.form.get('pricePlan'), app_stats=app_stats)
            price_plans = get_all_price_plans_for_app_template(request.form.get('appTemplate'))

            #TODO for now we know they have select the free one for now so just hard code it
            price_plan = price_plans[0]
            subscription_id = create_new_subscription(int(time.time()), 0, price_plan)

            user_app_name = request.form.get('appName')
            user_app_key = hashlib.sha224("%s %s" % (unicode(user._id), user_app_name)).hexdigest()
            user_app_secret_seed = "%s %s %s" % (unicode(user._id), user_app_name, time.time())
            user_app_secret = hashlib.sha224(user_app_secret_seed).hexdigest()
            user_app = AuthenticatedUserApp({
                "name":user_app_name,
                "key":user_app_key,
                "secret":user_app_secret,
                "subscription_ids":[subscription_id]})

            user = get_authenticated_user_by_id(session['user_id'])
            user.apps.append(user_app)
            user.save()
            return render_template("account/home.html", user=user, app_stats=app_stats)

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    if identity.name == 'guest':
        session.pop('user_id', None)
        identity.provides.clear()
    else:
        user = get_authenticated_user_by_riverid(identity.name)
        session['user_id'] = unicode(user._id)
        identity.provides.add(RoleNeed('user'))


app.secret_key = 'Q\x08\x13l\x0b-\x01\xd0)\xfddrY*\x8b\x96A.\xd7+\x02\xb8\xd8['