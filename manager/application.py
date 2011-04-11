from flask import Flask, current_app, render_template, redirect, request, url_for
from flaskext.principal import Principal, Permission, RoleNeed, Identity, identity_changed
from flaskext.principal import identity_loaded
from admin.formvalidation import validate_search_for_service_form
from admin.formvalidation import validate_change_rate_limit
from domain.utils import get_api_wrapper_by_free_text_search
from domain.utils import get_api_wrapper_by_id
from domain.utils import get_api_usage_statistics_by_api_wrapper_id
from domain.models import *

app = Flask(__name__)

# load the extension
principals = Principal(app)

# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))

@app.route('/')
def index():
    return render_template("admin/index.html", name='matt', fun=0.5)

@app.route('/secure')
@admin_permission.require()
def secure():
    return "only if logged in"

@app.route('/login')
def login():
    identity_changed.send(current_app._get_current_object(), identity=Identity('username'))
    return "Logged in"

@app.route('/logout')
def logout():
    identity_changed.send(current_app._get_current_object(), identity=Identity('guest'))
    return "Logged out"


@app.route('/services', methods=['POST'])
def admin_services():
    if request.method == 'POST':
        if 'serviceid' in request.form :
            service_id = request.form.get('serviceid')
            service = get_api_wrapper_by_id(service_id)
            service_stats = get_api_usage_statistics_by_api_wrapper_id(service_id)

        if 'search-for-service' in request.form:
            passed, errors = validate_search_for_service_form(request.form)
            if not passed:
                return render_template(request.form.get('returnto'), service_search_errors=errors)
            search = request.form.get('search')
            services = get_api_wrapper_by_free_text_search(search)
            if not len(services):
                return render_template(request.form.get('returnto'), service_search_errors=["Sorry, we didn't find any services with names like '%s'" % search])
            return render_template("admin/servicelist.html", services=services)
        elif 'view-service' in request.form:
            return render_template('admin/service.html', service=service, service_stats=service_stats)
        elif 'change-open-access-rate-limit' in request.form :
            passed, errors = validate_change_rate_limit(request.form)
            if not passed:
                return render_template(
                    "admin/service.html",
                    change_open_access_rate_limit_errors={request.form['methodid']:errors},
                    service=service,
                    service_stats=service_stats,
                    ratelimit=request.form['ratelimit'])
            #TODO handel save service
            pass
    else:
        return "services"

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    if identity.name == 'guest':
        identity.provides.clear()
    else:
        identity.provides.add(RoleNeed('admin'))
    


app.secret_key = 'Q\x08\x13l\x0b-\x01\xd0)\xfddrY*\x8b\x96A.\xd7+\x02\xb8\xd8['





