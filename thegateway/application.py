from flask import Flask, render_template, request, redirect, current_app, url_for, session
from thegateway.utils import validate_signin_form, validate_add_app_form
from flaskext.principal import Principal, Permission, RoleNeed, Identity, identity_changed
from flaskext.principal import identity_loaded
from domain.utils import con, get_authenticated_user_by_riverid, get_authenticated_user_by_id, get_all_price_plans_for_app_template, create_new_subscription
from domain.models import *
import time
import hashlib

app = Flask(__name__)

principals = Principal(app)

userPermission = Permission(RoleNeed('user'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'signIn' in request.form:
            passed, errors = validate_signin_form(request.form)
            if not passed:
                return render_template('index.html', signInErrors=errors, riverId=request.form.get('riverId'))
            identity_changed.send(current_app._get_current_object(), identity=Identity(request.form.get('riverId')))
            return redirect(url_for('user_home'))
    return render_template('index.html')


@app.route('/yourgateway', methods=['GET', 'POST'])
@userPermission.require(http_exception=401)
def user_home():
    user = get_authenticated_user_by_id(session['user_id'])
    if request.method == 'GET':
        return render_template("account/home.html", user=user)
    else:
        if 'add-app' in request.form :
            passed, errors = validate_add_app_form(request.form, user)
            if not passed:
                return render_template("account/home.html", user=user, addAppErrors=errors, appName=request.form.get('appName'), appTemplate=request.form.get('appTemplate'), pricePlan=request.form.get('pricePlan'))
            price_plans = get_all_price_plans_for_app_template(request.form.get('appTemplate'))

            #TODO for now we know they have select the free one for now so just hard code it
            price_plan = price_plans[0]
            subscription_id = create_new_subscription(int(time.time()), 0, price_plan)

            user_app_name = request.form.get('appName')
            user_app_key = hashlib.sha224(user_app_name).hexdigest()
            user_app_secret_seed = "%s %s" % (user_app_name, time.time())
            user_app_secret = hashlib.sha224(user_app_secret_seed).hexdigest()
            user_app = AuthenticatedUserApp({
                "name":user_app_name,
                "key":user_app_key,
                "secret":user_app_secret,
                "subscription_ids":[subscription_id]})

            user = get_authenticated_user_by_id(session['user_id'])
            user.apps.append(user_app)
            user.save()
            return render_template("account/home.html", user=user)

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    user = get_authenticated_user_by_riverid(identity.name)
    session['user_id'] = unicode(user._id)
    identity.provides.add(RoleNeed('user'))


app.secret_key = 'Q\x08\x13l\x0b-\x01\xd0)\xfddrY*\x8b\x96A.\xd7+\x02\xb8\xd8['