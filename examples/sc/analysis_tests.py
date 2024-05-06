import logging
from time import time

from tenable.sc import TenableSC

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s'
                    )

ACCESS_KEY = None
SECRET_KEY = None


def perform_analysis_test(age: int = 365,
                          page_size: int = 50,
                          timeout: int = 300
                          ):
    """
    Perform a simple test to record the amount of time it takes to return
    a single page of data from the SC Console given the specified attrs.
    """
    filters = (
          ('severity', '=', '3,4'),
          ('lastSeen', '=', f'0:{age}')
    )
    with TenableSC(access_key=ACCESS_KEY,
                   secret_key=SECRET_KEY,
                   timeout=timeout) as sc:
        start = time()
        vulns = sc.analysis.vulns(*filters, limit=page_size)
        _ = vulns.next()
        print(f'Requested page with a limit of {page_size}'
              f' took {int(time() - start)} seconds'
              )


for page_size in [50, 100, 500, 1000, 2000, 5000, 10000]:
    perform_analysis_test(page_size=page_size, timeout=999999)
