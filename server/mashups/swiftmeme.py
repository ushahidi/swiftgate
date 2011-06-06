from server import views
from server import mappers
from urllib2 import urlopen, HTTPError
import json
from domain.utils import get_authenticated_user_by_riverid,\
    get_all_price_plans_for_app_template, create_new_subscription, con
import re
import time
import hashlib
from domain.models import *

def run_swiftmeme_authentication_adapter(request, api_method_wrapper):
    """Used to register a new account or auth and existing account and create associated apps in the gateway"""
    mapper = getattr(mappers, api_method_wrapper.mapper)
    
    authorisation_request = mapper(request, api_method_wrapper.endpoint)
    
    try:
        
        response = urlopen(authorisation_request)
        
        response_object = json.loads(response.read())
        
        if response_object['status'] == 'Succeeded':
            
            riverid = request.form['riverid']
            
            user = get_authenticated_user_by_riverid(riverid)
            
            ensure_swiftmeme_apps(user)
            
            user.save()
            
            formatted_memes = [{"name":app.name,"id":app.key,"secret":app.secret} for app in get_swiftmeme_apps(user)]
            
            view = getattr(views, api_method_wrapper.view)
            
            return view('success', {"memes":formatted_memes})
        
        else:
            
            return view('failure', {"errors":response_object['errors']})
            
    except HTTPError, e:
        #TODO: This needs to be converted into a SwiftGateway error
        pass
     

def run_swiftmeme_memeoverview_adapter(request, api_method_wrapper):
    pass

#######################################################################################
# Supporting functions
#######################################################################################

def ensure_swiftmeme_apps(user):
    existing_swiftmeme_apps = get_swiftmeme_apps(user)
            
    #Here we create the swiftemem app ids that are needed for SwiftMeme
    for x in range(1, 3 - len(existing_swiftmeme_apps)):
        swiftmeme_price_plans = get_all_price_plans_for_app_template('SwiftMeme')
        
        #TODO Here we need to add support for creating paid accounts too
        price_plan = [p for p in swiftmeme_price_plans if bool(re.search(r'free', p.name, re.IGNORECASE))][0]
        
        subscription_id = create_new_subscription(int(time.time()), 0, price_plan)
        
        user_app_name = 'SwiftMeme Meme %s' % x
        user_app_key = hashlib.sha224("%s %s" % (unicode(user._id), user_app_name)).hexdigest()
        user_app_secret_seed = "%s %s %s" % (unicode(user._id), user_app_name, time.time())
        user_app_secret = hashlib.sha224(user_app_secret_seed).hexdigest()
        user_app = AuthenticatedUserApp({"name":user_app_name,"key":user_app_key,"secret":user_app_secret,"subscription_ids":[subscription_id]})

        user.apps.append(user_app)
        
def get_swiftmeme_apps(user):
    return [app for app in user.apps if app.template == unicode(con.AppTemplate.find_one({'name':'SwiftMeme'})._id)] 

def get_app_overview(apps):
    return {}