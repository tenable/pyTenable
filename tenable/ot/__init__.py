from tenable.base import APISession
from tenable.errors import *
import warnings, logging, semver


class TenableOT(APISession):
    _timeout = 300

    def __init__(self, host, token=None, port=443, ssl_verify=False, cert=None,
                 adapter=None, scheme='https', retries=None, backoff=None,
                 ua_identity=None, session=None, proxies=None, timeout=None,
                 vendor=None, product=None, build=None, base_path='v1'):
        # As we will always be passing a URL to the APISession class, we will
        # want to construct a URL that APISession (and further requests)
        # understands.
        base = '{}://{}:{}'.format(scheme, host, port)
        url = '{}/{}'.format(base, base_path)

        # We will need to store the API Token in order to use it as part of the
        # session builder.
        self._api_token = token

        # Setting the SSL Verification flag on the object itself so that it's
        # reusable if the user logs out and logs back in.
        self._ssl_verify = ssl_verify

        # Now lets pass the relevent parts off to the APISession's constructor
        # to make sure we have everything lined up as we expect.
        super(TenableOT, self).__init__(url,
            retries=retries,
            backoff=backoff,
            ua_identity=ua_identity,
            session=session,
            proxies=proxies,
            vendor=vendor,
            product=product,
            build=build,
            timeout=timeout
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def _build_session(self, session=None):
        super(TenableOT, self)._build_session(session)
        # As Tenable.sc is generally installed without a certificate chain that
        # we can validate, we will want to turn off verification and the
        # associated warnings unless told to otherwise:
        self._session.verify = self._ssl_verify
        if not self._ssl_verify:
            warnings.filterwarnings('ignore', 'Unverified HTTPS request')
        self._session.headers.update({
            'Authorization': 'Key {token}'.format(token=self._api_token)
        })