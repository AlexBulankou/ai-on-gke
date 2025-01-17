import unittest
from tornado import httputil
from jupyterhub.handlers import BaseHandler

from gcpiapjwtauthenticator import GCPIAPAuthenticator

class TestAuthenticator(unittest.TestCase):
    def test_handler_get_wrong_header_no_content(self):
        auth = GCPIAPAuthenticator()
        auth.header_name = "X-Goog-IAP-JWT-Assertion"

        bh = BaseHandler
        bh.authenticator = auth
        hder = httputil.HTTPHeaders({"Content-Type": "Random-header"})
        bh.request = httputil.HTTPServerRequest(headers=hder)

        iaphandlerclass = auth.get_handlers("")[0][1]
        with self.assertRaises(Exception) as httpexception:
            iaphandlerclass.get(bh)

        self.assertTrue("Can not verify the IAP authentication content." in httpexception.exception.log_message)
        self.assertTrue(httpexception.exception.status_code == 400)

    def test_handler_get_unaccepted_header(self):
        auth = GCPIAPAuthenticator()
        auth.header_name = "Random-Header"

        bh = BaseHandler
        bh.authenticator = auth
        hder = httputil.HTTPHeaders({"Content-Type": "X-Goog-IAP-JWT-Assertion"})
        bh.request = httputil.HTTPServerRequest(headers=hder)

        iaphandlerclass = auth.get_handlers("")[0][1]
        with self.assertRaises(Exception) as httpexception:
            iaphandlerclass.get(bh)

        self.assertTrue("X-Goog-IAP-JWT-Assertion is the only accepted Header" in httpexception.exception.log_message)
        self.assertTrue(httpexception.exception.status_code == 400)

if __name__ == '__main__':
    unittest.main()