__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"


from flask import Flask, render_template, request, redirect, current_app, url_for, session
from themanager.utils import validate_signin_form
from themanager.utils import validate_edit_service_form
from themanager.utils import validate_edit_method_form
from themanager.utils import validate_edit_priceplan_form
from themanager.utils import validate_edit_rule_form
from themanager.utils import validate_save_template_form
from flaskext.principal import Principal, Permission, RoleNeed, Identity, identity_changed
from flaskext.principal import identity_loaded
from domain.utils import con
from domain.utils import get_authenticated_user_by_riverid
from domain.utils import get_api_wrapper_by_id
from domain.utils import get_priceplan_by_id
from domain.models import *
import server.handlers
import server.mappers
import server.views
import re

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
            return redirect(url_for('gatewaymanager'))
        if 'signOut' in request.form:
            identity_changed.send(current_app._get_current_object(), identity=Identity('guest'))
    return render_template('index.html')


@app.route('/gatewaymanager', methods=['GET', 'POST'])
@userPermission.require(http_exception=401)
def gatewaymanager():
    services = con.APIWrapper.find()
    priceplans = con.PricePlan.find()
    app_templates = [template for template in con.AppTemplate.find()]
    return render_template(
        'manager/home.html',
        services=services,
        priceplans=priceplans,
        app_templates=app_templates)

@app.route('/gatewaymanager/editservice', methods=['GET', 'POST'])
@userPermission.require(http_exception=401)
def service_edit():
    #Get the views etc by reflexion
    is_handler = re.compile(r'handler', re.IGNORECASE)
    handlers = [handler for handler in dir(server.handlers) if is_handler.search(handler)]
    is_mapper = re.compile(r'mapper', re.IGNORECASE)
    mappers = [mapper for mapper in dir(server.mappers) if is_mapper.search(mapper)]
    is_view = re.compile(r'view', re.IGNORECASE)
    views = [view for view in dir(server.views) if is_view.search(view)]

    page_errors = {}
    service = {}
    messages = {}
    id = None
    form = {}

    if request.method == 'GET':
        if 'id' in request.args:
            id = request.args['id']
            service = get_api_wrapper_by_id(id)
    else:
        if request.form['id']:
            id = request.form['id']
            service = get_api_wrapper_by_id(id)
        else:
            service = con.APIWrapper()
        if 'delete_service' in request.form:
            service.delete()
            return redirect(url_for('gatewaymanager'))
        elif 'save_service' in request.form:
            passed, errors = validate_edit_service_form(request.form)
            if passed:
                service.display_name = request.form['display_name']
                service.description = request.form['description']
                service.request_handler = request.form['request_handler']
                service.url_identifier = request.form['url_identifier']
                service.save()
                messages['service_messages'] = ['Service saved']
            else:
                page_errors['service_errors'] = errors
        elif 'save_new_method' in request.form:
            if not request.form['id']:
                page_errors['new_method_errors'] = ['You need to save the service before you can add methods']
            else:
                passed, errors = validate_edit_method_form(request.form)
                if passed:
                    new_method = APIMethodWrapper({
                        "method_identifier":request.form['method_identifier'],
                        "mapper":request.form['mapper'],
                        "accepted_http_methods":request.form['accepted_http_methods'],
                        "url_pattern":request.form['url_pattern'],
                        "endpoint":request.form['endpoint'],
                        "view":request.form['view'],
                        "open_access_calls_per_hour":int(request.form['open_access_calls_per_hour']),
                    })
                    service.api_methods.append(new_method)
                    service.save()
                    messages['method_messages'] = ['New method added']
                else:
                    page_errors['new_method_errors'] = errors
                    form = request.form
        else:
            methods = []
            for method in service.api_methods:
                method_id = method.method_identifier
                if 'delete_method_%s' % method_id in request.form:
                    for candidate_method in service.api_methods:
                        if not method_id == candidate_method.method_identifier:
                            methods.append(candidate_method)
                            messages['method_messages'] = ['Method deleted']
            if not methods:
                for method in service.api_methods:
                    method_id = method.method_identifier
                    if 'save_method_%s' % method_id in request.form:
                        for candidate_method in service.api_methods:
                            if not method_id == candidate_method.method_identifier:
                                methods.append(candidate_method)
                            else:
                                passed, errors = validate_edit_method_form(request.form, method_id)
                                if passed:
                                    changed_method = APIMethodWrapper({
                                        "method_identifier":request.form['method_identifier_%s' % method_id],
                                        "mapper":request.form['mapper_%s' % method_id],
                                        "accepted_http_methods":request.form['accepted_http_methods_%s' % method_id],
                                        "url_pattern":request.form['url_pattern_%s' % method_id],
                                        "endpoint":request.form['endpoint_%s' % method_id],
                                        "view":request.form['view_%s' % method_id],
                                        "open_access_calls_per_hour":int(request.form['open_access_calls_per_hour_%s' % method_id]),
                                    })
                                    methods.append(changed_method)
                                    messages['method_messages'] = ['Method saved']
                                else:
                                    page_errors['method_errors_%s' %  method_id] = errors
            if not page_errors:
                service.api_methods = methods
                service.save()
    return render_template(
        'manager/service_edit.html',
        service=service,
        handlers=handlers,
        mappers=mappers,
        views=views,
        errors=page_errors,
        messages=messages,
        form=form)

@app.route('/gatewaymanager/editpriceplan', methods=['GET', 'POST'])
@userPermission.require(http_exception=401)
def priceplan_edit():
    # Set up the drop down data sources
    services = {}
    for service in con.APIWrapper.find(): services[re.sub(r'/', r'_', service.url_identifier)] = service

    priceplan = {}
    return_form = {}
    page_errors = {}
    messages = {}

    if request.method == 'GET':
        if 'id' in request.args:
            id = request.args['id']
            priceplan = get_priceplan_by_id(id)
    else:
        if request.form['id']:
            priceplan_id = request.form['id']
            priceplan = get_priceplan_by_id(priceplan_id)
        else:
            priceplan = con.PricePlan()
        if 'delete_priceplan' in request.form:
            priceplan.delete()
            return redirect(url_for('gatewaymanager'))
        elif 'save_priceplan' in request.form:
            passed, errors = validate_edit_priceplan_form(request.form)
            if passed:
                priceplan.name = request.form.get('name')
                priceplan.active = False if request.form['active'] == 'false' else True
                priceplan.group = request.form['group']
                priceplan.price = eval(request.form['price'])
                priceplan.save()
                messages['priceplan_messages'] = ['Priceplan saved']
            else:
                page_errors['priceplan_errors'] = errors
        elif 'save_new_rule' in request.form:
            if not request.form['id']:
                page_errors['new_rule_errors'] = ['You need to save the priceplan before you can add rules']
            else:
                passed, errors = validate_edit_rule_form(request.form)
                if passed:
                    new_rule = PricePlanRule({
                        "service":re.sub(r'_', '/', request.form['service']),
                        "api_method":request.form['api_method'] if not request.form['api_method'] == 'all' else None,
                        "permitted_calls":float(request.form['permitted_calls']),
                        "per":86400
                    })
                    priceplan.rules.append(new_rule)
                    priceplan.save()
                    messages['rule_messages'] = ['New rule added']
                else:
                    page_errors['new_rule_errors'] = errors
                    return_form = request.form
        else:
            rules = []
            counter = -1
            for rule in priceplan.rules:
                counter = counter + 1
                if 'delete_rule_%s' % counter in request.form:
                    for candidate_rule in priceplan.rules:
                        if not candidate_rule.service == priceplan.rules[counter].service:
                            rules.append(candidate_rule)
                            messages['rule_messages'] = ['Rule deleted']

            if not rules:
                counter = -1
                for rule in priceplan.rules:
                    counter = counter + 1
                    if 'save_rule_%s' % counter in request.form:
                        for candidate_rule in priceplan.rules:
                            if not candidate_rule.service == priceplan.rules[counter].service:
                                methods.append(candidate_method)
                            else:
                                passed, errors = validate_edit_rule_form(request.form, counter)
                                if passed:
                                    changed_rule = PricePlanRule({
                                        "service":re.sub(r'_', '/', request.form['service_%s' % counter]),
                                        "api_method":request.form['api_method_%s' % counter] if not request.form['api_method_%s' % counter] == 'all' else None,
                                        "permitted_calls":int(request.form['permitted_calls_%s' % counter]),
                                        "per":86400
                                    })
                                    rules.append(changed_rule)
                                    messages['rule_messages'] = ['rule saved']
                                else:
                                    page_errors['rule_errors_%s' %  counter] = errors
            if not page_errors:
                priceplan.rules = rules
                priceplan.save()

    return render_template(
        'manager/priceplan_edit.html',
        priceplan=priceplan,
        form=return_form,
        errors=page_errors,
        messages=messages,
        services=services)

@app.route('/gatewaymanager/editapptemplate', methods=['GET', 'POST'])
@userPermission.require(http_exception=401)
def apptemplate_edit():
    all_priceplans = [priceplan for priceplan in con.PricePlan.find({'active':True})]
    selected_priceplans = []
    template = {}
    page_errors = []
    form = request.form

    if request.method == 'GET':
        if 'id' in request.args:
            id = request.args['id']
            template = con.AppTemplate.find_one({'_id':ObjectId(id)})
    else:
        if request.form['id']:
            id = request.form['id']
            template = con.AppTemplate.find_one({'_id':ObjectId(id)})
        else:
            template = con.AppTemplate()
        if 'delete_template' in request.form:
            template.delete()
            return redirect(url_for('gatewaymanager'))
        if 'save_template' in request.form:
            passed, errors = validate_save_template_form(request.form)
            if passed:
                template.name= request.form['name']
                template.description = request.form['description']
                template.active = True if request.form['active'] == 'true' else False
                template.group = request.form['group']
                template.price_plans = [priceplan for priceplan in all_priceplans if unicode(priceplan._id) in request.form]
                template.save()
            else:
                page_errors = errors
    selected_priceplans = [pp._id for pp in template.price_plans] if template else []
    return render_template(
        'manager/template_edit.html',
        template=template,
        form=form,
        all_priceplans=all_priceplans,
        selected_priceplans=selected_priceplans,
        errors=page_errors)


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