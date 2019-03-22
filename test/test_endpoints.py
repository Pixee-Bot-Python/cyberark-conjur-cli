import unittest

from conjur_api_python3.endpoints import ConjurEndpoint

class EndpointsTest(unittest.TestCase):
    def test_http_verb_has_correct_authenticate_template_string(self):
        auth_endpoint = ConjurEndpoint.AUTHENTICATE.value.format(url='http://host',
                                                                 account='myacct',
                                                                 login='mylogin')
        self.assertEqual(auth_endpoint, 'http://host/authn/myacct/mylogin/authenticate')

    def test_http_verb_has_correct_login_template_string(self):
        auth_endpoint = ConjurEndpoint.LOGIN.value.format(url='http://host',
                                                          account='myacct')
        self.assertEqual(auth_endpoint, 'http://host/authn/myacct/login')

    def test_http_verb_has_correct_secrets_template_string(self):
        auth_endpoint = ConjurEndpoint.SECRETS.value.format(url='http://host',
                                                            account='myacct',
                                                            kind='varkind',
                                                            identifier='varid')
        self.assertEqual(auth_endpoint, 'http://host/secrets/myacct/varkind/varid')
