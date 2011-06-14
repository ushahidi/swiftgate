from server import views
from server import mappers
from urllib2 import urlopen, HTTPError
from domain.utils import get_authenticated_user_by_riverid
from domain.utils import get_all_price_plans_for_app_template, create_new_subscription, con
import re
import time
import hashlib
import json
from domain.models import *

def run_swiftmeme_authentication_adapter(request, api_method_wrapper):
    """Used to register a new account or auth and existing account and create associated apps in the gateway"""
    mapper = getattr(mappers, api_method_wrapper.mapper)
    
    authorisation_request = mapper(request, api_method_wrapper.endpoint)
    
    view = getattr(views, api_method_wrapper.view)
    
    try:
        
        response = urlopen(authorisation_request)
        
        response_object = json.loads(response.read())
        
        if response_object['status'] == 'Succeeded':
            
            riverid = request.form['riverid']
            
            user = get_authenticated_user_by_riverid(riverid)
            
            ensure_swiftmeme_apps(user)
            
            formatted_memes = [{"name":app.name,"id":app.key,"secret":app.secret} for app in get_swiftmeme_apps(user)]
            
            return view(api_method_wrapper.method_identifier, 'success', {"memes":formatted_memes})
        
        else:
            
            return view(api_method_wrapper.method_identifier, 'failure', {"errors":response_object['errors']})
            
    except HTTPError, e:
        #TODO: This needs to be converted into a SwiftGateway error
        pass
     
def run_swiftmeme_memeoverview_adapter(request, api_method_wrapper):
    #TODO: this is just a mock up at the moment
    view = getattr(views, api_method_wrapper.view)
    
    response_data = {
        "name":"This would be the name of the meme",
        "stats":[
            {
                "name":"quickstats",
                "data":{
                    "posts":4374343,
                    "sources":767,
                    "keywords":67,
                    "channels":3
                }
            },
            {
                "name":"recentactivity",
                "data":[
                    {"date":"2011-06-01","count":50},
                    {"date":"2011-06-02","count":40},
                    {"date":"2011-06-03","count":30},
                    {"date":"2011-06-04","count":50},
                ] 
            }
        ]
    }
    
    return view('success', response_data)

def run_swiftmeme_analytics_adapter(request, api_method_wrapper):
    #TODO: this is just a mock up at the moment
    view = getattr(views, api_method_wrapper.view)
    
    response_data = {
        "topkeywords": [
            {
                "name": "nike",
                "count": 40
            },
            {
                "name": "fail",
                "count": 80
            }
        ],
        "topsources": [
            {
                "name": "@whiteafrican",
                "uri": "http://twitter.com/whiteafrican",
                "count": 20
            },
            {
                "name": "CNN Blogs",
                "uri": "http://blogs.cnn.com",
                "count": 30
            }
        ],
        "newkeywords": [
            {
                "name": "swiftriver",
                "count": 80
            },
            {
                "name": "blog",
                "count": 20
            }
        ],
        "toplocations": [
            {
                "name": "Nairobi, Kenya",
                "country": "ke",
                "count": 1234,
                "sentiment": ":)"
            },
            {
                "name": "Mombasa, Kenya",
                "country": "ke",
                "count": 234,
                "sentiment": ":|"
            },
            {
                "name": "Cape Town, South Africa",
                "country": "za",
                "count": 123,
                "sentiment": ":("
            }
        ],
        "channels": [
            {
                "name": "Twitter",
                "count": 3456
            },
            {
                "name": "RSS",
                "count": 1234
            }
        ]
    }
    
    return view('success', response_data)
    
def run_swiftmeme_content_adapter(request, api_method_wrapper):
    view = getattr(views, api_method_wrapper.view)
    
    response_data = {
        "totalcount":"16","contentitems":[
             {"id":"6878a0e01c516a6087d4dfeba30d1918","state":"new_content","text":[{"languageCode":"unknown","title":"","text":[""]}],"link":"http:\/\/news.google.com\/","date":1308046388,"tags":[],"source":{"id":"52ba0c5e7026b2896373b0e18418889c","date":1308046388,"score":100,"name":"Quiver","email":None,"link":"http:\/\/news.google.com\/","applicationIds":[],"applicationProfileImages":[],"parent":"Quiver","type":"Quiver","subType":"Quiver","gisData":[]},"difs":[],"gisData":[],"extensions":[]},
             {"id":"cb162214d61faceb91a8662cb9e07375","state":"new_content","text":[{"languageCode":"en","title":"[] Sinsai.info \u6025\u52df in reception reports - post \/ Confirmation (moderator) staff and volunteers - Volunteers - Volunteer] [developers] are looking for a translator. http:\/\/p.tl\/SKb2 # osm-ja","text":["[] Sinsai.info \u6025\u52df in reception reports - post \/ Confirmation (moderator) staff and volunteers - Volunteers - Volunteer] [developers] are looking for a translator. http:\/\/p.tl\/SKb2 # osm-ja"]},{"languageCode":"ja","title":"\u3010\u6025\u52df\u3011sinsai.info \u3067\u306f\u3001\u3010\u6295\u7a3f\u3055\u308c\u305f\u30ec\u30dd\u30fc\u30c8\u306e\u53d7\u4ed8\/\u5185\u5bb9\u78ba\u8a8d\uff08\u30e2\u30c7\u30ec\u30fc\u30bf\u30fc\uff09\u30dc\u30e9\u30f3\u30c6\u30a3\u30a2\u3011\u30b9\u30bf\u30c3\u30d5\u3084\u3010\u958b\u767a\u8005\u30dc\u30e9\u30f3\u30c6\u30a3\u30a2\u3011\u3010\u7ffb\u8a33\u8005\u30dc\u30e9\u30f3\u30c6\u30a3\u30a2\u3011\u3092\u52df\u96c6\u4e2d\u3067\u3059\u3002http:\/\/p.tl\/SKb2 #osm-ja","text":["\u3010\u6025\u52df\u3011sinsai.info \u3067\u306f\u3001\u3010\u6295\u7a3f\u3055\u308c\u305f\u30ec\u30dd\u30fc\u30c8\u306e\u53d7\u4ed8\/\u5185\u5bb9\u78ba\u8a8d\uff08\u30e2\u30c7\u30ec\u30fc\u30bf\u30fc\uff09\u30dc\u30e9\u30f3\u30c6\u30a3\u30a2\u3011\u30b9\u30bf\u30c3\u30d5\u3084\u3010\u958b\u767a\u8005\u30dc\u30e9\u30f3\u30c6\u30a3\u30a2\u3011\u3010\u7ffb\u8a33\u8005\u30dc\u30e9\u30f3\u30c6\u30a3\u30a2\u3011\u3092\u52df\u96c6\u4e2d\u3067\u3059\u3002http:\/\/p.tl\/SKb2 #osm-ja"]}],"link":"&lt;a href=&quot;http:\/\/twittbot.net\/&quot; rel=&quot;nofollow&quot;&gt;twittbot.net&lt;\/a&gt;","date":1308042299,"tags":[{"type":"General","text":"osm"},{"type":"General","text":"sinsai.info"},{"type":"General","text":"ja"}],"source":{"id":"6908872397a36f569b3815c1bca755a5","date":1308046376,"score":None,"name":"iwaki_sinsai","email":None,"link":"http:\/\/twitter.com\/iwaki_sinsai","applicationIds":{"twitter":302301811},"applicationProfileImages":{"twitter":"http:\/\/a0.twimg.com\/sticky\/default_profile_images\/default_profile_1_normal.png"},"parent":"b360d30c973125a734b9e227e4fe0ebd","type":"Twitter","subType":"Search","gisData":[]},"difs":[{"difs":[{"type":"Sanitized Tweet","value":""}],"name":"Sanitized Tweet"}],"gisData":[],"extensions":[]},
             {"id":"2274cce5b29074c69f002f1c9a8fa32c","state":"new_content","text":[{"languageCode":"en","title":"Ushahidi planning considerations in order to learn from service user participation: Column: Internet Business types: VentureNow (Now venture) http:\/\/htn.to\/D2dvwU","text":["Ushahidi planning considerations in order to learn from service user participation: Column: Internet Business types: VentureNow (Now venture) http:\/\/htn.to\/D2dvwU"]},{"languageCode":"ja","title":"Ushahidi \u304b\u3089\u5b66\u3076\u30e6\u30fc\u30b6\u53c2\u52a0\u578b\u30b5\u30fc\u30d3\u30b9\u3092\u4f01\u753b\u3059\u308b\u4e0a\u3067\u306e\u7559\u610f\u70b9 :\u30b3\u30e9\u30e0\uff1a\u30a4\u30f3\u30bf\u30fc\u30cd\u30c3\u30c8\u30d3\u30b8\u30cd\u30b9\u306e\u7a2e\uff1aVentureNow\uff08\u30d9\u30f3\u30c1\u30e3\u30fc\u30ca\u30a6\uff09 http:\/\/htn.to\/D2dvwU","text":["Ushahidi \u304b\u3089\u5b66\u3076\u30e6\u30fc\u30b6\u53c2\u52a0\u578b\u30b5\u30fc\u30d3\u30b9\u3092\u4f01\u753b\u3059\u308b\u4e0a\u3067\u306e\u7559\u610f\u70b9 :\u30b3\u30e9\u30e0\uff1a\u30a4\u30f3\u30bf\u30fc\u30cd\u30c3\u30c8\u30d3\u30b8\u30cd\u30b9\u306e\u7a2e\uff1aVentureNow\uff08\u30d9\u30f3\u30c1\u30e3\u30fc\u30ca\u30a6\uff09 http:\/\/htn.to\/D2dvwU"]}],"link":"&lt;a href=&quot;http:\/\/www.hatena.ne.jp\/guide\/twitter&quot; rel=&quot;nofollow&quot;&gt;Hatena&lt;\/a&gt;","date":1308039187,"tags":[{"type":"General","text":"ushahidi"},{"type":"General","text":"venturenow"}],"source":{"id":"2467c620441578484ba20a5f019ff3ad","date":1308046376,"score":None,"name":"dhalmel","email":None,"link":"http:\/\/twitter.com\/dhalmel","applicationIds":{"twitter":283465},"applicationProfileImages":{"twitter":"http:\/\/a0.twimg.com\/profile_images\/1270813872\/bbb53f3d-1634-461d-81a7-9610abe7732e_normal.png"},"parent":"b360d30c973125a734b9e227e4fe0ebd","type":"Twitter","subType":"Search","gisData":[]},"difs":[{"difs":[{"type":"Sanitized Tweet","value":"ushahidi "}],"name":"Sanitized Tweet"}],"gisData":[],"extensions":[]},
             {"id":"35cce9cf268d221767260cb8f0d6cf5b","state":"new_content","text":[{"languageCode":"en","title":"RT @whiteafrican: Ushahidi's @dkobia accepts the (RED) Webby Award saying, &quot;Our voices revolutionize the world&quot;.","text":["RT @whiteafrican: Ushahidi's @dkobia accepts the (RED) Webby Award saying, &quot;Our voices revolutionize the world&quot;."]}],"link":"&lt;a href=&quot;http:\/\/tapbots.com\/tweetbot&quot; rel=&quot;nofollow&quot;&gt;Tweetbot for iPhone&lt;\/a&gt;","date":1308033412,"tags":[{"type":"General","text":"ushahidis"},{"type":"General","text":"world"},{"type":"General","text":"award"},{"type":"General","text":"accepts"},{"type":"General","text":"voice"},{"type":"General","text":"red"},{"type":"General","text":"webby"}],"source":{"id":"9ddbd36d1d251875265e84460cc90074","date":1308046376,"score":None,"name":"opentechgirl","email":None,"link":"http:\/\/twitter.com\/opentechgirl","applicationIds":{"twitter":29696905},"applicationProfileImages":{"twitter":"http:\/\/a2.twimg.com\/profile_images\/324078528\/dar_normal.jpg"},"parent":"b360d30c973125a734b9e227e4fe0ebd","type":"Twitter","subType":"Search","gisData":[]},"difs":[{"difs":[{"type":"Sanitized Tweet","value":"ushahidi's accepts the (red) webby award voices revolutionize the "}],"name":"Sanitized Tweet"}],"gisData":[],"extensions":[]},
             {"id":"a86c0fb6045524beccbf4c2d1a2afd3e","state":"new_content","text":[{"languageCode":"en","title":"RT @whiteafrican: Ushahidi's @dkobia accepts (RED) Webby Award saying, &quot;Our voices revolutionize the world.&quot; &lt;-Good use of his 5 word limit","text":["RT @whiteafrican: Ushahidi's @dkobia accepts (RED) Webby Award saying, &quot;Our voices revolutionize the world.&quot; &lt;-Good use of his 5 word limit"]}],"link":"&lt;a href=&quot;http:\/\/www.hootsuite.com&quot; rel=&quot;nofollow&quot;&gt;HootSuite&lt;\/a&gt;","date":1308032814,"tags":[{"type":"General","text":"ushahidis"},{"type":"General","text":"good"},{"type":"General","text":"world"},{"type":"General","text":"award"},{"type":"General","text":"accepts"},{"type":"General","text":"limit"},{"type":"General","text":"voice"},{"type":"General","text":"red"},{"type":"General","text":"word"},{"type":"General","text":"lt"},{"type":"General","text":"webby"}],"source":{"id":"33f7f215f7d1508a48939923e812a454","date":1308046376,"score":None,"name":"liveunchained","email":None,"link":"http:\/\/twitter.com\/liveunchained","applicationIds":{"twitter":65258296},"applicationProfileImages":{"twitter":"http:\/\/a2.twimg.com\/profile_images\/424660212\/facebookad_normal.jpg"},"parent":"b360d30c973125a734b9e227e4fe0ebd","type":"Twitter","subType":"Search","gisData":[]},"difs":[{"difs":[{"type":"Sanitized Tweet","value":"ushahidi's accepts (red) webby award voices revolutionize the use of his 5 word limit "}],"name":"Sanitized Tweet"}],"gisData":[],"extensions":[]},
             {"id":"a1a4e7dc0da4dcb21da52854c384c9db","state":"new_content","text":[{"languageCode":"en","title":"RT @whiteafrican: Ushahidi's @dkobia accepts the (RED) Webby Award saying, &quot;Our voices revolutionize the world&quot;.","text":["RT @whiteafrican: Ushahidi's @dkobia accepts the (RED) Webby Award saying, &quot;Our voices revolutionize the world&quot;."]}],"link":"&lt;a href=&quot;http:\/\/www.hootsuite.com&quot; rel=&quot;nofollow&quot;&gt;HootSuite&lt;\/a&gt;","date":1308032759,"tags":[{"type":"General","text":"ushahidis"},{"type":"General","text":"world"},{"type":"General","text":"award"},{"type":"General","text":"accepts"},{"type":"General","text":"voice"},{"type":"General","text":"red"},{"type":"General","text":"webby"}],"source":{"id":"33f7f215f7d1508a48939923e812a454","date":1308046376,"score":None,"name":"liveunchained","email":None,"link":"http:\/\/twitter.com\/liveunchained","applicationIds":{"twitter":65258296},"applicationProfileImages":{"twitter":"http:\/\/a2.twimg.com\/profile_images\/424660212\/facebookad_normal.jpg"},"parent":"b360d30c973125a734b9e227e4fe0ebd","type":"Twitter","subType":"Search","gisData":[]},"difs":[{"difs":[{"type":"Sanitized Tweet","value":"ushahidi's accepts the (red) webby award voices revolutionize the "}],"name":"Sanitized Tweet"}],"gisData":[],"extensions":[]},{"id":"a1542858b6b89431b98c1c36f984cfdb","state":"new_content","text":[{"languageCode":"en","title":"@whiteafrican starts by paying tribute to ushahidi on their webby award #pivot25","text":["@whiteafrican starts by paying tribute to ushahidi on their webby award #pivot25"]}],"link":"&lt;a href=&quot;http:\/\/www.tweetdeck.com&quot; rel=&quot;nofollow&quot;&gt;TweetDeck&lt;\/a&gt;","date":1308032407,"tags":[{"type":"General","text":"paying"},{"type":"General","text":"award"},{"type":"General","text":"pivot25"},{"type":"General","text":"webby"},{"type":"General","text":"tribute"},{"type":"General","text":"start"}],"source":{"id":"becef846d75e7481b54441ac81d32b1e","date":1308046376,"score":None,"name":"OscarRombo","email":None,"link":"http:\/\/twitter.com\/OscarRombo","applicationIds":{"twitter":34988534},"applicationProfileImages":{"twitter":"http:\/\/a1.twimg.com\/profile_images\/89638222\/Image124_normal.jpg"},"parent":"b360d30c973125a734b9e227e4fe0ebd","type":"Twitter","subType":"Search","gisData":[]},"difs":[{"difs":[{"type":"Sanitized Tweet","value":"starts by paying tribute to ushahidi on their webby award "}],"name":"Sanitized Tweet"}],"gisData":[],"extensions":[]},
        ],
        "navigation":{
            "Tags":{
                "type":"list",
                "key":"tags",
                "selected":False,
                "facets":[
                    {"name":"award","id":"award","count":"7"},
                    {"name":"webby","id":"webby","count":"7"},
                    {"name":"world","id":"world","count":"6"},
                    {"name":"ushahidis","id":"ushahidis","count":"5"},
                    {"name":"voice","id":"voice","count":"5"},
                    {"name":"red","id":"red","count":"5"},
                    {"name":"accepts","id":"accepts","count":"4"},
                    {"name":"sinsai.info","id":"sinsai.info","count":"4"},
                    {"name":"ushahidi","id":"ushahidi","count":"3"},
                    {"name":"wordpressjp","id":"wordpressjp","count":"3"},
                    {"name":"sinsai","id":"sinsai","count":"3"},
                    {"name":"wordpress","id":"wordpress","count":"3"},
                    {"name":"api","id":"api","count":"3"},
                    {"name":"congrats","id":"congrats","count":"2"},
                    {"name":"venturenow","id":"venturenow","count":"1"},
                    {"name":"david","id":"david","count":"1"},
                    {"name":"juliana","id":"juliana","count":"1"},
                    {"name":"erik","id":"erik","count":"1"},
                    {"name":"presenting","id":"presenting","count":"1"},
                    {"name":"thanks","id":"thanks","count":"1"},
                    {"name":"team","id":"team","count":"1"},
                    {"name":"university","id":"university","count":"1"},
                    {"name":"tool","id":"tool","count":"1"},
                    {"name":"peacebuilding","id":"peacebuilding","count":"1"},
                    {"name":"mapping","id":"mapping","count":"1"},
                    {"name":"example","id":"example","count":"1"},
                    {"name":"platform","id":"platform","count":"1"},
                    {"name":"paying","id":"paying","count":"1"},
                    {"name":"pivot25","id":"pivot25","count":"1"},
                    {"name":"tribute","id":"tribute","count":"1"},
                    {"name":"start","id":"start","count":"1"},
                    {"name":"good","id":"good","count":"1"},
                    {"name":"limit","id":"limit","count":"1"},
                    {"name":"word","id":"word","count":"1"},
                    {"name":"lt","id":"lt","count":"1"},
                    {"name":"osm","id":"osm","count":"1"},
                    {"name":"ja","id":"ja","count":"1"},
                    {"name":"better","id":"better","count":"1"},
                    {"name":"innovation","id":"innovation","count":"1"},
                    {"name":"tech","id":"tech","count":"1"}
                ]
            },
            "Channels":{
                "type":"list",
                "key":"type",
                "selected":False,
                "facets":[
                          {"name":"Twitter","id":"Twitter","count":"15"},
                          {"name":"Quiver","id":"Quiver","count":"1"}
                ]
            }
        }
    }
    
    return view('sucess', response_data)

#######################################################################################
# Supporting functions
#######################################################################################


def ensure_swiftmeme_apps(user):
    existing_swiftmeme_apps = get_swiftmeme_apps(user)
            
    if len(existing_swiftmeme_apps) == 0:
        apps_to_create = [1, 2, 3]
    elif len(existing_swiftmeme_apps) < 3:
        apps_to_create = []
        if not [app for app in existing_swiftmeme_apps if app.name == 'SwiftMeme Meme 1']:
            apps_to_create.append(1)
        if not [app for app in existing_swiftmeme_apps if app.name == 'SwiftMeme Meme 2']:
            apps_to_create.append(2)
        if not [app for app in existing_swiftmeme_apps if app.name == 'SwiftMeme Meme 3']:
            apps_to_create.append(3)
    else:
        apps_to_create = []
        
    
    #Here we create the swiftemem app ids that are needed for SwiftMeme
    for x in apps_to_create:
        swiftmeme_price_plans = get_all_price_plans_for_app_template('swiftmeme/1', "admin")
        
        #TODO Here we need to add support for creating paid accounts too
        price_plan = [p for p in swiftmeme_price_plans if p.name == "A SwiftMeme Meme"][0]
        
        subscription_id = create_new_subscription(int(time.time()), 0, price_plan)
        
        user_app_name = 'SwiftMeme Meme %s' % x
        user_app_key = hashlib.sha224("%s %s" % (unicode(user._id), user_app_name)).hexdigest()
        user_app_secret_seed = "%s %s %s" % (unicode(user._id), user_app_name, time.time())
        user_app_secret = hashlib.sha224(user_app_secret_seed).hexdigest()
        user_app_template = unicode(con.AppTemplate.find_one({'name':'A SwiftMeme Meme'})._id)
        user_app = AuthenticatedUserApp({
            "name":user_app_name,
            "key":user_app_key,
            "secret":user_app_secret,
            "subscription_ids":[subscription_id],
            "template":user_app_template})

        user.apps.append(user_app)
        
    user.save()
        
def get_swiftmeme_apps(user):
    if not len(user.apps):
        return []
    subject_template = con.AppTemplate.find_one({'name':'A SwiftMeme Meme'})
    if not subject_template:
        return []
    subject_template_id = unicode(subject_template._id)
    return [app for app in user.apps if app.template == subject_template_id] 

def get_app_overview(apps):
    return {}