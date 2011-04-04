
def validate_search_for_service_form(form):
    search = form.get('search')
    if not search:
        return False, ['You forgot to enter anything in the search box!']
    return True, []

