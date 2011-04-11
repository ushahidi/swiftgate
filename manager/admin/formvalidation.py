
def validate_search_for_service_form(form):
    search = form.get('search')
    if not search:
        return False, ['You forgot to enter anything in the search box!']
    return True, []

def validate_change_rate_limit(form):
    ratelimit = form.get('ratelimit')
    if not ratelimit.isdigit():
        return False, ['The rate limit must be a positive whole number!']
    return True
