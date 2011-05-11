from thegateway.authentication import authentication_factory
import re

def validate_signin_form(form):
    riverId = form.get('riverId')
    password = form.get('password')
    if not riverId or not password:
        return False, ['You must enter your RiverID and password']
    authenticationProvider = authentication_factory()
    return authenticationProvider.authenticate(riverId, password)

def validate_add_app_form(form, user):
    app_name = form.get('appName')
    if not app_name:
        return False, ['You need to choose a name for this app']
    app_template = form.get('appTemplate')
    if app_template == '0':
        return False, ['You need to select a template for this app']
    rule = re.compile(app_name, re.IGNORECASE)
    for app in user.apps:
        if bool(rule.match(app.name)):
            return False, ['You already have an app with that name, please choose another one']
    return True, []