from domain.models import APIUsageWrapper, APIRateAbuse
from server.utils import is_oauth_request
from domain.utils import get_un_authenticated_user_by_host
from domain.utils import get_un_authenticated_rate_abuser_by_host
import time

class RequestUser(object):
    def __init__(self, request, api_wrapper):
        self._request = request
        self._api_wrapper = api_wrapper

    def record_api_access(self, api_method_wrapper):
        #If this is not an Oauth request then only free access avaliable
        if not is_oauth_request(self._request):
            return self._record_api_access_for_unauthenticated_user(api_method_wrapper)

    def _record_api_access_for_unauthenticated_user(self, api_method_wrapper):
        #get the service identifier
        service_identifier = self._api_wrapper.url_identifier

        #get the method identifier
        method_identifier = api_method_wrapper.method_identifier

        #get the time now
        request_time = time.time()

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
        user = get_un_authenticated_user_by_host(unicode(self._request.host))

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
                self._record_unauthenticated_rate_abuse(api_method_wrapper)

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

    def _record_unauthenticated_rate_abuse(self, api_method_wrapper):
        #get the service identifier
        service_identifier = self._api_wrapper.url_identifier

        #get the method identifier
        method_identifier = api_method_wrapper.method_identifier

        #get the time now
        request_time = time.time()

        #get the rate abuser object
        rate_abuser = get_un_authenticated_rate_abuser_by_host(self._request.host)

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


class RecordAPIAccessReturn:
    pass




