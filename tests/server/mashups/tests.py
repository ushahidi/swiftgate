from domain.models import *
from domain.utils import *
from server.mashups.swiftmeme import ensure_swiftmeme_apps

user = get_authenticated_user_by_riverid(u'test1')
ensure_swiftmeme_apps(user)
