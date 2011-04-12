import oauth2
from domain.models import APIUsageWrapper, APIRateAbuse
from server.utils import is_oauth_request
from server.utils import extract_oauth_consumer_key_from_auth_header_string
from server.utils import build_oauth_request_from_request
from domain.utils import get_un_authenticated_user_by_host
from domain.utils import get_un_authenticated_rate_abuser_by_host
from domain.utils import get_api_usage_statistics_by_api_wrapper_id
from domain.utils import get_authenticated_user_app_by_key
import time

class RequestUser(object):
    def __init__(self, request, api_wrapper):
        self._request = request
        self._api_wrapper = api_wrapper

    def record_api_access(self, api_method_wrapper):
        #get the time now
        request_time = time.time()

        self._record_general_api_usage_stats(api_method_wrapper, request_time)

        #If this is not an Oauth request then only free access avaliable
        if not is_oauth_request(self._request):
            return self._record_api_access_for_unauthenticated_user(api_method_wrapper, request_time)
        else:
            #TODO Enable OAuth
            return_data = RecordAPIAccessReturn()
            return_data.access_status = 'denied'
            return_data.access_message = 'Sorry, we dont yet support OAuth authenticated access to our API - but we will soon'
            return return_data
            #return self._record_api_access_for_authenticated_user(api_method_wrapper, request_time)


    def _record_general_api_usage_stats(self, api_method_wrapper, request_time):

        request_time = time.localtime(request_time)

        year = unicode(request_time.tm_year)
        month = unicode(request_time.tm_mon)
        day = unicode(request_time.tm_mday)
        hour = unicode(request_time.tm_hour)
        minute = unicode(request_time.tm_min)
        seconds = unicode(request_time.tm_sec)

        #Keep a running record of the total number of api access
        stats = get_api_usage_statistics_by_api_wrapper_id(unicode(self._api_wrapper._id))
        
        if not api_method_wrapper.method_identifier in stats['methods'].keys():
            stats['methods'][api_method_wrapper.method_identifier] = \
                {"total" : 1, "years" : {} }
        else:
            stats['methods'][api_method_wrapper.method_identifier]['total'] = \
                stats['methods'][api_method_wrapper.method_identifier]['total'] + 1

        if not year in stats['methods'][api_method_wrapper.method_identifier]['years'].keys():
            stats['methods'][api_method_wrapper.method_identifier]['years'][year] = {"total" : 1, "months" : {}}
        else:
            stats['methods'][api_method_wrapper.method_identifier]['years'][year]['total'] = \
                stats['methods'][api_method_wrapper.method_identifier]['years'][year]['total'] + 1

        if not month in stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'].keys():
            stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month] = {"total" : 1, "days" : {}}
        else:
            stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['total'] = \
                stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['total'] + 1

        if not day in stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['days'].keys():
            stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['days'][day] = {"total" : 1, "hours" : {}}
        else:
            stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['days'][day]['total'] = \
                stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['days'][day]['total'] + 1

        if not hour in stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['days'][day]['hours'].keys():
            stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['days'][day]['hours'][hour] = {"total" : 1, "minutes" : {}}
        else:
            stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['days'][day]['hours'][hour]['total'] = \
                stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['days'][day]['hours'][hour]['total'] + 1

        if not minute in stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['days'][day]['hours'][hour]['minutes'].keys():
            stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['days'][day]['hours'][hour]['minutes'][minute] = {"total" : 1, "seconds" : {}}
        else:
            stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['days'][day]['hours'][hour]['minutes'][minute]['total'] = \
                stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['days'][day]['hours'][hour]['minutes'][minute]['total'] + 1

        if not seconds in stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['days'][day]['hours'][hour]['minutes'][minute]['seconds'].keys():
            stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['days'][day]['hours'][hour]['minutes'][minute]['seconds'][seconds] = {"total" : 1}
        else:
            stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['days'][day]['hours'][hour]['minutes'][minute]['seconds'][seconds]['total'] = \
                stats['methods'][api_method_wrapper.method_identifier]['years'][year]['months'][month]['days'][day]['hours'][hour]['minutes'][minute]['seconds'][seconds]['total'] + 1

        stats.save()

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

    def _record_api_access_for_authenticated_user(self, api_method_wrapper, request_time):

        oauth_server = oauth2.Server(signature_methods={'HMAC-SHA1': oauth2.SignatureMethod_HMAC_SHA1()})

        oauth_server.timestamp_threshold = 500000

        #Get the Authorization header
        auth_header = {'Authorization':self._request.headers['Authorization']}

        key = extract_oauth_consumer_key_from_auth_header_string(auth_header['Authorization'])

        if not key:
            return_data = RecordAPIAccessReturn()
            return_data.access_status = 'denied'
            return_data.access_message = "Sorry, we didn't find an oauth_consumer_key in the Authorization header of your request"
            return return_data

        req = build_oauth_request_from_request(
            self._request.method,
            self._request.url,
            auth_header)
        
        user = get_authenticated_user_app_by_key(key)

        if user is None:
            return_data = RecordAPIAccessReturn()
            return_data.access_status = 'denied'
            return_data.access_message = "Sorry, we didn't find a user account that matches the Oauth customer key %s, are you sure you have it correct?" % key
            return return_data

        app = filter(lambda x: x.key == key, user.apps)[0]

        try:
            oauth_server.verify_request(req, app, None)
            return_data = RecordAPIAccessReturn()
            return_data.access_status = 'accepted'
            return return_data
        except oauth2.Error, e:
            return_data = RecordAPIAccessReturn()
            return_data.access_status = 'denied'
            return_data.access_message = "%s" % e
            return return_data
        except AttributeError, e:
            return_data = RecordAPIAccessReturn()
            return_data.access_status = 'denied'
            return_data.access_message = "You failed to supply the necessary parameters (%s) to properly authenticate." % e
            return return_data


class RecordAPIAccessReturn:
    pass




