__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"


import oauth2
from domain.models import APIUsageWrapper, APIRateAbuse
from server.utils import is_oauth_request
from server.utils import extract_oauth_consumer_key_from_auth_header_string
from server.utils import baselogger
from domain.utils import get_un_authenticated_user_by_host
from domain.utils import get_un_authenticated_rate_abuser_by_host
from domain.utils import get_authenticated_user_app_by_key
from domain.utils import get_subscription_by_id

class RequestUser(object):
    def __init__(self, request, api_wrapper):
        self._request = request
        self._api_wrapper = api_wrapper

    def record_api_access(self, api_method_wrapper, usage_statistics):
        #get the time now
        request_time = usage_statistics['start_time']

        #If this is not an Oauth request then only free access avaliable
        if not is_oauth_request(self._request):
            return self._record_api_access_for_unauthenticated_user(api_method_wrapper, request_time)
        else:
            return self._record_api_access_for_authenticated_user(api_method_wrapper, request_time, usage_statistics)

    def _record_api_access_for_unauthenticated_user(self, api_method_wrapper, request_time):
        #get the service identifier
        service_identifier = self._api_wrapper.url_identifier

        #get the method identifier
        method_identifier = api_method_wrapper.method_identifier

        #get the allowed free rate limit per hour
        rate_limit = api_method_wrapper.open_access_calls_per_hour
        if rate_limit is None:
            rate_limit = 0

        #If no free limit allowed then return denied with message
        if rate_limit is 0:
            return_data = RecordAPIAccessReturn()
            return_data.access_status = 'denied'
            return_data.access_message = 'Oh no! This method has no free acess allowance'
            return return_data

        #pull the un_authenticed_user from the datastore
        user = get_un_authenticated_user_by_host(unicode(self._request.remote_addr))

        #extract any existing user statistics for this service and method
        candidate_usage_statistics = filter(
            lambda x:
                x.service_identifier == service_identifier and
                x.method_identifier == method_identifier,
            user.api_usage)

        #If user does not have existing statistics for this service/method combo
        if len(candidate_usage_statistics) == 0:
            #Build up the data for a new APIUsageWrapper instance
            usage_statistics = APIUsageWrapper({
                "service_identifier": service_identifier,
                "method_identifier": method_identifier,
                "usage_calls" : 1,
                "usage_since" : request_time,
            })

            #Add the statistict to the user
            user.api_usage.append(usage_statistics)

            #save the user
            user.save()

            #return a accepted message
            return_data = RecordAPIAccessReturn()
            return_data.access_status = 'accepted'
            return return_data
        else:
            #extract the usage statistics for the service and method
            usage_statistics = candidate_usage_statistics[0]

            #get the difference in hours between now and when stats last reset
            usage_time_diff = (request_time - usage_statistics.usage_since)/(60.0*60)

            #If the diff is more than one hour then reset all the counts and time
            if usage_time_diff > 1:
                usage_statistics.usage_calls = 0
                usage_statistics.usage_since = request_time

            #If the rate limit has been reached then return denied
            if rate_limit > 0 and usage_statistics.usage_calls > rate_limit:
                #record the rate abuse
                self._record_unauthenticated_rate_abuse(api_method_wrapper, request_time)

                #build and return the message
                return_data = RecordAPIAccessReturn()
                minutes_till_reset = 60 - ((request_time - usage_statistics.usage_since)/60)
                return_data.access_status = 'denied'
                return_data.access_message = 'Oh no! You have exceeded your rate limit for this service. You have %0.1f minutes till your account is reset.' % minutes_till_reset
                return return_data

            #increment the usage data
            usage_statistics.usage_calls = usage_statistics.usage_calls + 1

            #identify the index of the current APIUsageWrapper elment in the list
            index = user.api_usage.index(usage_statistics)

            #replace the existing usage data with the new one
            user.api_usage[index] = usage_statistics

            #save the user
            user.save()

            #return a accepted message
            return_data = RecordAPIAccessReturn()
            return_data.access_status = 'accepted'
            return return_data

    def _record_unauthenticated_rate_abuse(self, api_method_wrapper, request_time):
        #get the service identifier
        service_identifier = self._api_wrapper.url_identifier

        #get the method identifier
        method_identifier = api_method_wrapper.method_identifier

        #get the rate abuser object
        rate_abuser = get_un_authenticated_rate_abuser_by_host(self._request.remote_addr)

        candidate_abuse_statistics = filter(
            lambda x:
                x.service_identifier == service_identifier and
                x.method_identifier == method_identifier,
            rate_abuser.api_rate_abuse)

        #if no statistics exist for this service method combo
        if len(candidate_abuse_statistics) == 0:
            #construct a new APIRateAbuse instance
            abuse_statistics = APIRateAbuse({
                "service_identifier": service_identifier,
                "method_identifier": method_identifier,
                "rate_abuses" : 1,
                "abuses_since" : request_time,
            })

            #Add the new record to the rate_abuser instance
            rate_abuser.api_rate_abuse.append(abuse_statistics)

            #save the rate abuser
            rate_abuser.save()

        else:
            #Get the statistics for this service method combo
            abuse_statistics = candidate_abuse_statistics[0]

            #increnet the instances of abuse
            abuse_statistics.rate_abuses = abuse_statistics.rate_abuses +1

            #get the index of this service method combo on the rate_abuser instance
            index = rate_abuser.api_rate_abuse.index(abuse_statistics)

            #Add back the statistics
            rate_abuser.api_rate_abuse[index] = abuse_statistics

            #Save the rate abuser instance
            rate_abuser.save()

    def _record_api_access_for_authenticated_user(self, api_method_wrapper, request_time, usage_statistics):

        oauth_server = oauth2.Server(signature_methods={'HMAC-SHA1': oauth2.SignatureMethod_HMAC_SHA1()})

        #oauth_server.timestamp_threshold = 500000

        auth_header = {}
        key = None
        
        if 'Authorization' in self._request.headers:
            auth_header = {'Authorization':self._request.headers['Authorization']}
            key = extract_oauth_consumer_key_from_auth_header_string(auth_header['Authorization'])

        req = oauth2.Request.from_request(
            self._request.method,
            self._request.url.split('?')[0],
            headers=auth_header,
            parameters=dict([(k,v) for k,v in self._request.values.iteritems()]))

        #If key not present in the auth header try form the params
        if not key:
            key = self._request.values.get('oauth_consumer_key')

        #if still no key then quit
        if not key:
            return_data = RecordAPIAccessReturn()
            return_data.access_status = 'denied'
            return_data.access_message = "Sorry, we didn't find an oauth_consumer_key in the Authorization header of your request"
            return return_data

        user = get_authenticated_user_app_by_key(key)
        
        if user is None:
            return_data = RecordAPIAccessReturn()
            return_data.access_status = 'denied'
            return_data.access_message = "Sorry, we didn't find a user account that matches the Oauth customer key %s, are you sure you have it correct?" % key
            return return_data

        user_app = filter(lambda x: x.key == key, user.apps)[0]

        usage_statistics['app_id'] = user_app.key

        try:
            oauth_server.verify_request(req, user_app, None)
        except oauth2.Error, e:
            return_data = RecordAPIAccessReturn()
            return_data.access_status = 'denied'
            return_data.access_message = "%s" % e
            baselogger.error("OAUTH REQUEST DENIED, |%s|" % return_data.access_message)
            return return_data
        except KeyError, e:
            return_data = RecordAPIAccessReturn()
            return_data.access_status = 'denied'
            return_data.access_message = "You failed to supply the necessary parameters (%s) to properly authenticate." % e
            baselogger.error("OAUTH REQUEST DENIED, |%s|" % return_data.access_message)
            return return_data

        #get the service identifier for this request
        service_identifier = self._api_wrapper.url_identifier

        #get the method identifier
        method_identifier = api_method_wrapper.method_identifier

        #Set up the rate limit variables
        rate_limit = None
        rate_limit_per = None

        #Loop through the active
        for subscription_id in user_app.subscription_ids:
            subscription = get_subscription_by_id(subscription_id)
            #Validity period set to 0 for no-expire subscriptions
            if subscription.validity_period > 0:
                if subscription.start_date + subscription.validity_period > request_time:
                    #subscription has expired - break out of this and check anyother subscriptions
                    continue
            for rule in subscription.usage_plan.rules:
                if rule.service == service_identifier:
                    #rule.api_method set to none means all
                    if not rule.api_method or rule.api_method == method_identifier:
                        method = rule.api_method if rule.api_method else 'all'
                        #get the alloted permited calls from the rule
                        rate_limit = rule.permitted_calls
                        rate_limit_per = rule.per
                        #check if there is any current usage
                        if not service_identifier in subscription.usage:
                            subscription.usage[service_identifier] = {
                                method:{
                                    "calls":1,
                                    "since":request_time}}
                            subscription.save()
                        elif not method in subscription.usage[service_identifier]:
                            subscription.usage[service_identifier][method] = {
                                "calls":1,
                                "since":request_time
                            }
                            subscription.save()
                        else:
                            calls = subscription.usage[service_identifier][method]["calls"]
                            since = subscription.usage[service_identifier][method]["since"]
                            if request_time - since > rate_limit_per:
                                subscription.usage[service_identifier][method]["calls"] = 1
                                subscription.usage[service_identifier][method]["since"] = request_time
                                subscription.save()
                            elif calls > rate_limit:
                                #RATE ABUSE - record the abuse
                                if 'abuse' in subscription.usage[service_identifier][method]:
                                    subscription.usage[service_identifier][method]["abuse"].append(request_time)
                                else:
                                    subscription.usage[service_identifier][method]['abuse'] = [request_time]
                                subscription.save()
                                #build and return the message
                                return_data = RecordAPIAccessReturn()
                                minutes_till_reset = 60 - ((request_time - since)/60)
                                return_data.access_status = 'denied'
                                return_data.access_message = 'Oh no! You have exceeded your rate limit for this service. You have %0.1f minutes till your account is reset.' % minutes_till_reset
                                return return_data
                            else:
                                subscription.usage[service_identifier][method]["calls"] = calls + 1
                                subscription.save()

        return_data = RecordAPIAccessReturn()
        return_data.access_status = 'accepted'
        return return_data

class RecordAPIAccessReturn:
    pass




