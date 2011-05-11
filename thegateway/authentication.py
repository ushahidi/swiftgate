def authentication_factory():
    return MockAuthenticationProvider()

class MockAuthenticationProvider(object):
    def authenticate(self, username, password):
        if not username == 'matt':
            return False, ['That RiverID was not found']
        if not password == 'password':
            return False, ['That password was wrong, sorry']
        return True, []


