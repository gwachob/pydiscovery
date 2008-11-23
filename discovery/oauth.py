import document

TYPE_REQUEST_TOKEN='http://oauth.net/core/1.0/endpoint/request'
TYPE_USER_AUTHORIZATION='http://oauth.net/core/1.0/endpoint/authorize'
TYPE_ACCESS_TOKEN='http://oauth.net/core/1.0/endpoint/access'
TYPE_PROTECTED_RESOURCE='http://oauth.net/core/1.0/endpoint/resource'

TYPE_STATIC_ALLOCATION='http://oauth.net/discovery/1.0/consumer-identity/static'
TYPE_OOB_ALLOCATION='http://oauth.net/discovery/1.0/consumer-identity/oob'

TYPE_AUTH_HEADER='http://oauth.net/core/1.0/parameters/auth-header'
TYPE_POST_BODY='http://oauth.net/core/1.0/parameters/post-body'
TYPE_URI_QUERY='http://oauth.net/core/1.0/parameters/uri-query'

TYPE_HMAC_SHA1='http://oauth.net/core/1.0/signature/HMAC-SHA1'
TYPE_RSA_SHA1='http://oauth.net/core/1.0/signature/RSA-SHA1'
TYPE_PLAINTEXT='http://oauth.net/core/1.0/signature/PLAINTEXT'


class OAuthDescriptor(object):

    def __init__(self, xrd):

    def getRequestTokens(self):
         

    def getUserAuthorization(self):
        pass

    def getAccesToken(self):
        pass

    def ProtectedResource(self):
        pass


