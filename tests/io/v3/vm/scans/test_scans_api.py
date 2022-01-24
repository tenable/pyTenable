'''
Testing the Scans endpoints
'''

import os

import pytest
import responses
from requests import Response
from responses import matchers

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

dir_name = os.path.dirname(os.path.abspath(__file__))

IMG_ATTACHMENT_FILE = 'img_attachment_file.png'
TXT_ATTACHMENT_FILE = 'text_file.txt'

TXT_ATTACHMENT_FILE_PATH = os.path.join(dir_name, TXT_ATTACHMENT_FILE)


SCAN_BASE_URL = r'https://cloud.tenable.com/api/v3/scans'
BASE_URL = r'https://cloud.tenable.com'


@pytest.fixture
def text_contents():

    '''
    Fixture to read the contents of text file.
    '''

    with open(TXT_ATTACHMENT_FILE_PATH, 'rb') as txt_file:
        text_data = txt_file.read()

    return text_data


@responses.activate
def test_create(api):
    '''
    Test the create endpoint
    '''
    create_resp_data = {
        'tag_type': None,
        'container_id': 'cfdabb09-6aef-481d-b28f-aecb1c38f297',
        'owner_id': 'e9f23194-adb7-4c02-8632-615c694c787e',
        'id':
            'template-b4e5aea9-ab26-5cf3-3a76-98e216211cd390d1e4e488585988',
        'name': 'Example Embedded Cred Scan',
        'description': None,
        'policy_id': 109,
        'scanner_id':
            '00000000-0000-0000-0000-00000000000000000000000000001',
        'emails': None,
        'sms': '',
        'enabled': True,
        'include_aggregate': True,
        'scan_time_window': None,
        'custom_targets': '127.0.0.1',
        'target_network_uuid': None,
        'auto_routed': 0,
        'remediation': 0,
        'version': 1,
        'triggers': None,
        'agent_scan_launch_type': None,
        'starttime': None,
        'rrules': None,
        'timezone': None,
        'notification_filters': None,
        'shared': 0, 'user_permissions': 128,
        'default_permissions': 0,
        'owner': 'test@test.com',
        'last_modification_date': '2019-12-31T20:50:23.635Z',
        'creation_date': '2019-12-31T20:50:23.635Z',
        'type': 'public',
    }
    policy_template_res = [{
        'unsupported': False,
        'cloud_only': False,
        'desc': 'Remote and local checks for CVE-2017-5689.',
        'order': 8,
        'subscription_only': False,
        'is_was': 'None',
        'title': 'Intel AMT Security Bypass',
        'is_agent': 'None',
        'uuid': '3f514e0e-66e0-8ea2-b6e7-d2d86b526999a93a89944d19e1f1',
        'icon':
            'PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48c3ZnIHZlcnNpb249IjEuMSIgaWQ9ImJhc2ljV2ViQXBwU2NhbiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgeD0iMHB4IiB5PSIwcHgiIHZpZXdCb3g9IjAgMCAxNiAxNiIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgMTYgMTY7IiB4bWw6c3BhY2U9InByZXNlcnZlIj48c3R5bGUgdHlwZT0idGV4dC9jc3MiPi5zdDB7ZmlsbDojREJEOUQ2O30uc3Qxe2ZpbGw6I0FBQTlBQTt9LnN0MntmaWxsOiM3Nzg1OTI7fS5zdDN7ZmlsbDojNDM1MzYzO30uc3Q0e2ZpbGw6IzI2Mzc0NTt9LnN0NXtmaWxsOiNGMzZDM0U7fS5zdDZ7ZmlsbDojQUU0NTI1O30uc3Q3e2ZpbGw6I0RCRTBFMTt9LnN0OHtmaWxsOiNGRkZGRkY7fTwvc3R5bGU+PGcgaWQ9Im5vZGVzIj48ZyBpZD0ibm9kZSI+PHJlY3QgeD0iNCIgeT0iMSIgY2xhc3M9InN0MCIgd2lkdGg9IjEiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjQiIHk9IjIiIGNsYXNzPSJzdDEiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiLz48L2c+PGcgaWQ9Im5vZGVfMV8iPjxyZWN0IHg9IjUuNzUiIHk9IjEiIGNsYXNzPSJzdDAiIHdpZHRoPSIxIiBoZWlnaHQ9IjIiLz48cmVjdCB4PSI1Ljc1IiB5PSIyIiBjbGFzcz0ic3QxIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIi8+PC9nPjxnIGlkPSJub2RlXzNfIj48cmVjdCB4PSI5LjI1IiB5PSIxIiBjbGFzcz0ic3QwIiB3aWR0aD0iMSIgaGVpZ2h0PSIyIi8+PHJlY3QgeD0iOS4yNSIgeT0iMiIgY2xhc3M9InN0MSIgd2lkdGg9IjEiIGhlaWdodD0iMSIvPjwvZz48ZyBpZD0ibm9kZV81XyI+PHJlY3QgeD0iNy41IiB5PSIxIiBjbGFzcz0ic3QwIiB3aWR0aD0iMSIgaGVpZ2h0PSIyIi8+PHJlY3QgeD0iNy41IiB5PSIyIiBjbGFzcz0ic3QxIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIi8+PC9nPjxnIGlkPSJub2RlXzRfIj48cmVjdCB4PSIxMSIgeT0iMSIgY2xhc3M9InN0MCIgd2lkdGg9IjEiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjExIiB5PSIyIiBjbGFzcz0ic3QxIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIi8+PC9nPjwvZz48ZyBpZD0ibm9kZXNfMV8iPjxnIGlkPSJub2RlXzlfIj48cmVjdCB4PSIxMSIgeT0iMTMiIHRyYW5zZm9ybT0ibWF0cml4KC0xIC0xLjIyNDY0N2UtMTYgMS4yMjQ2NDdlLTE2IC0xIDIzIDI4KSIgY2xhc3M9InN0MCIgd2lkdGg9IjEiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjExIiB5PSIxMyIgdHJhbnNmb3JtPSJtYXRyaXgoLTEgLTEuMjI0NjQ3ZS0xNiAxLjIyNDY0N2UtMTYgLTEgMjMgMjcpIiBjbGFzcz0ic3QxIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIi8+PC9nPjxnIGlkPSJub2RlXzhfIj48cmVjdCB4PSI5LjI1IiB5PSIxMyIgdHJhbnNmb3JtPSJtYXRyaXgoLTEgLTEuMjI0NjQ3ZS0xNiAxLjIyNDY0N2UtMTYgLTEgMTkuNSAyOCkiIGNsYXNzPSJzdDAiIHdpZHRoPSIxIiBoZWlnaHQ9IjIiLz48cmVjdCB4PSI5LjI1IiB5PSIxMyIgdHJhbnNmb3JtPSJtYXRyaXgoLTEgLTEuMjI0NjQ3ZS0xNiAxLjIyNDY0N2UtMTYgLTEgMTkuNSAyNykiIGNsYXNzPSJzdDEiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiLz48L2c+PGcgaWQ9Im5vZGVfN18iPjxyZWN0IHg9IjUuNzUiIHk9IjEzIiB0cmFuc2Zvcm09Im1hdHJpeCgtMSAtMS4yMjQ2NDdlLTE2IDEuMjI0NjQ3ZS0xNiAtMSAxMi41IDI4KSIgY2xhc3M9InN0MCIgd2lkdGg9IjEiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjUuNzUiIHk9IjEzIiB0cmFuc2Zvcm09Im1hdHJpeCgtMSAtMS4yMjQ2NDdlLTE2IDEuMjI0NjQ3ZS0xNiAtMSAxMi41IDI3KSIgY2xhc3M9InN0MSIgd2lkdGg9IjEiIGhlaWdodD0iMSIvPjwvZz48ZyBpZD0ibm9kZV82XyI+PHJlY3QgeD0iNy41IiB5PSIxMyIgdHJhbnNmb3JtPSJtYXRyaXgoLTEgLTEuMjI0NjQ3ZS0xNiAxLjIyNDY0N2UtMTYgLTEgMTYgMjgpIiBjbGFzcz0ic3QwIiB3aWR0aD0iMSIgaGVpZ2h0PSIyIi8+PHJlY3QgeD0iNy41IiB5PSIxMyIgdHJhbnNmb3JtPSJtYXRyaXgoLTEgLTEuMjI0NjQ3ZS0xNiAxLjIyNDY0N2UtMTYgLTEgMTYgMjcpIiBjbGFzcz0ic3QxIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIi8+PC9nPjxnIGlkPSJub2RlXzJfIj48cmVjdCB4PSI0IiB5PSIxMyIgdHJhbnNmb3JtPSJtYXRyaXgoLTEgMS44MTg4NjdlLTEyIC0xLjgxODg2N2UtMTIgLTEgOSAyOCkiIGNsYXNzPSJzdDAiIHdpZHRoPSIxIiBoZWlnaHQ9IjIiLz48cmVjdCB4PSI0IiB5PSIxMyIgdHJhbnNmb3JtPSJtYXRyaXgoLTEgMS44MTg4NjdlLTEyIC0xLjgxODg2N2UtMTIgLTEgOSAyNykiIGNsYXNzPSJzdDEiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiLz48L2c+PC9nPjxnIGlkPSJub2Rlc18yXyI+PGcgaWQ9Im5vZGVfMTRfIj48cmVjdCB4PSIxMy41IiB5PSIzLjUiIHRyYW5zZm9ybT0ibWF0cml4KC0xLjgzNjk3MGUtMTYgMSAtMSAtMS44MzY5NzBlLTE2IDE4LjUgLTkuNSkiIGNsYXNzPSJzdDAiIHdpZHRoPSIxIiBoZWlnaHQ9IjIiLz48cmVjdCB4PSIxMyIgeT0iNCIgdHJhbnNmb3JtPSJtYXRyaXgoLTEuODM2OTcwZS0xNiAxIC0xIC0xLjgzNjk3MGUtMTYgMTggLTkpIiBjbGFzcz0ic3QxIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIi8+PC9nPjxnIGlkPSJub2RlXzEzXyI+PHJlY3QgeD0iMTMuNSIgeT0iNS4yNSIgdHJhbnNmb3JtPSJtYXRyaXgoLTEuODM2OTcwZS0xNiAxIC0xIC0xLjgzNjk3MGUtMTYgMjAuMjUgLTcuNzUpIiBjbGFzcz0ic3QwIiB3aWR0aD0iMSIgaGVpZ2h0PSIyIi8+PHJlY3QgeD0iMTMiIHk9IjUuNzUiIHRyYW5zZm9ybT0ibWF0cml4KC0xLjgzNjk3MGUtMTYgMSAtMSAtMS44MzY5NzBlLTE2IDE5Ljc1IC03LjI1KSIgY2xhc3M9InN0MSIgd2lkdGg9IjEiIGhlaWdodD0iMSIvPjwvZz48ZyBpZD0ibm9kZV8xMl8iPjxyZWN0IHg9IjEzLjUiIHk9IjguNzUiIHRyYW5zZm9ybT0ibWF0cml4KC0xLjgzNjk3MGUtMTYgMSAtMSAtMS44MzY5NzBlLTE2IDIzLjc1IC00LjI1KSIgY2xhc3M9InN0MCIgd2lkdGg9IjEiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjEzIiB5PSI5LjI1IiB0cmFuc2Zvcm09Im1hdHJpeCgtMS44MzY5NzBlLTE2IDEgLTEgLTEuODM2OTcwZS0xNiAyMy4yNSAtMy43NSkiIGNsYXNzPSJzdDEiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiLz48L2c+PGcgaWQ9Im5vZGVfMTFfIj48cmVjdCB4PSIxMy41IiB5PSI3IiB0cmFuc2Zvcm09Im1hdHJpeCgtMS44MzY5NzBlLTE2IDEgLTEgLTEuODM2OTcwZS0xNiAyMiAtNikiIGNsYXNzPSJzdDAiIHdpZHRoPSIxIiBoZWlnaHQ9IjIiLz48cmVjdCB4PSIxMyIgeT0iNy41IiB0cmFuc2Zvcm09Im1hdHJpeCgtMS44MzY5NzBlLTE2IDEgLTEgLTEuODM2OTcwZS0xNiAyMS41IC01LjUpIiBjbGFzcz0ic3QxIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIi8+PC9nPjxnIGlkPSJub2RlXzEwXyI+PHJlY3QgeD0iMTMuNSIgeT0iMTAuNSIgdHJhbnNmb3JtPSJtYXRyaXgoMS44MTg4MDZlLTEyIDEgLTEgMS44MTg4MDZlLTEyIDI1LjUgLTIuNSkiIGNsYXNzPSJzdDAiIHdpZHRoPSIxIiBoZWlnaHQ9IjIiLz48cmVjdCB4PSIxMyIgeT0iMTEiIHRyYW5zZm9ybT0ibWF0cml4KDEuODE4ODA2ZS0xMiAxIC0xIDEuODE4ODA2ZS0xMiAyNSAtMikiIGNsYXNzPSJzdDEiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiLz48L2c+PC9nPjxnIGlkPSJub2Rlc18zXyI+PGcgaWQ9Im5vZGVfMTlfIj48cmVjdCB4PSIxLjUiIHk9IjEwLjUiIHRyYW5zZm9ybT0ibWF0cml4KDYuMTIzMjM0ZS0xNyAtMSAxIDYuMTIzMjM0ZS0xNyAtOS41IDEzLjUpIiBjbGFzcz0ic3QwIiB3aWR0aD0iMSIgaGVpZ2h0PSIyIi8+PHJlY3QgeD0iMiIgeT0iMTEiIHRyYW5zZm9ybT0ibWF0cml4KDYuMTIzMjM0ZS0xNyAtMSAxIDYuMTIzMjM0ZS0xNyAtOSAxNCkiIGNsYXNzPSJzdDEiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiLz48L2c+PGcgaWQ9Im5vZGVfMThfIj48cmVjdCB4PSIxLjUiIHk9IjguNzUiIHRyYW5zZm9ybT0ibWF0cml4KDYuMTIzMjM0ZS0xNyAtMSAxIDYuMTIzMjM0ZS0xNyAtNy43NSAxMS43NSkiIGNsYXNzPSJzdDAiIHdpZHRoPSIxIiBoZWlnaHQ9IjIiLz48cmVjdCB4PSIyIiB5PSI5LjI1IiB0cmFuc2Zvcm09Im1hdHJpeCg2LjEyMzIzNGUtMTcgLTEgMSA2LjEyMzIzNGUtMTcgLTcuMjUgMTIuMjUpIiBjbGFzcz0ic3QxIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIi8+PC9nPjxnIGlkPSJub2RlXzE3XyI+PHJlY3QgeD0iMS41IiB5PSI1LjI1IiB0cmFuc2Zvcm09Im1hdHJpeCg2LjEyMzIzNGUtMTcgLTEgMSA2LjEyMzIzNGUtMTcgLTQuMjUgOC4yNSkiIGNsYXNzPSJzdDAiIHdpZHRoPSIxIiBoZWlnaHQ9IjIiLz48cmVjdCB4PSIyIiB5PSI1Ljc1IiB0cmFuc2Zvcm09Im1hdHJpeCg2LjEyMzIzNGUtMTcgLTEgMSA2LjEyMzIzNGUtMTcgLTMuNzUgOC43NSkiIGNsYXNzPSJzdDEiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiLz48L2c+PGcgaWQ9Im5vZGVfMTZfIj48cmVjdCB4PSIxLjUiIHk9IjciIHRyYW5zZm9ybT0ibWF0cml4KDYuMTIzMjM0ZS0xNyAtMSAxIDYuMTIzMjM0ZS0xNyAtNiAxMCkiIGNsYXNzPSJzdDAiIHdpZHRoPSIxIiBoZWlnaHQ9IjIiLz48cmVjdCB4PSIyIiB5PSI3LjUiIHRyYW5zZm9ybT0ibWF0cml4KDYuMTIzMjM0ZS0xNyAtMSAxIDYuMTIzMjM0ZS0xNyAtNS41IDEwLjUpIiBjbGFzcz0ic3QxIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIi8+PC9nPjxnIGlkPSJub2RlXzE1XyI+PHJlY3QgeD0iMS41IiB5PSIzLjUiIHRyYW5zZm9ybT0ibWF0cml4KC0xLjgxODkyOGUtMTIgLTEgMSAtMS44MTg5MjhlLTEyIC0yLjUgNi41KSIgY2xhc3M9InN0MCIgd2lkdGg9IjEiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjIiIHk9IjQiIHRyYW5zZm9ybT0ibWF0cml4KC0xLjgxODkyOGUtMTIgLTEgMSAtMS44MTg5MjhlLTEyIC0yIDcpIiBjbGFzcz0ic3QxIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIi8+PC9nPjwvZz48cGF0aCBjbGFzcz0ic3QyIiBkPSJNMTIuNzUsM2gtOS41QzMuMTExOTI5LDMsMywzLjExMTkyOSwzLDMuMjV2NC4xMjVsMS45NDE5ODEtMS45NDE5ODFjMC4wMzc2OS0wLjAzNzY5LDAuMTk3NTExLTAuMDk4Mzg1LDAuMjUwMjA1LTAuMTA2NDExbDEuNTQ4OTkxLTAuMjE2ODA0TDkuMzEyNSwxMC42MjVMNi45Mzc1LDEzSDEyLjc1YzAuMTM4MDcxLDAsMC4yNS0wLjExMTkyOSwwLjI1LTAuMjV2LTkuNUMxMywzLjExMTkyOSwxMi44ODgwNzEsMywxMi43NSwzeiIvPjxwYXRoIGNsYXNzPSJzdDMiIGQ9Ik00Ljk0MTk4MSw1LjQzMzAxOUwzLDcuMzc1djUuMzc1QzMsMTIuODg4MDcxLDMuMTExOTI5LDEzLDMuMjUsMTNoMy42ODc1bDIuMzc1LTIuMzc1TDYuNzQxMTc3LDUuMTA5ODA0TDUuMTkyMTg2LDUuMzI2NjA4QzUuMTM5NDkyLDUuMzM0NjM0LDQuOTc5NjcxLDUuMzk1MzI5LDQuOTQxOTgxLDUuNDMzMDE5eiIvPjxjaXJjbGUgY2xhc3M9InN0MyIgY3g9IjExLjUiIGN5PSI0LjUiIHI9IjAuNSIvPjxjaXJjbGUgY2xhc3M9InN0NCIgY3g9IjQuNSIgY3k9IjExLjUiIHI9IjAuNSIvPjxwYXRoIGNsYXNzPSJzdDUiIGQ9Ik04LDV2Ni40NTAwMTJjMi42NDU1MDktMC44ODE4MzYsMi45NTgxMTItNC45MzI1NDYsMi45OTUwNS01Ljg3NzUyN2MwLjAwNDY3MS0wLjExOTQ5NS0wLjA3MDg2OC0wLjIxODMyMS0wLjE4NzIzNy0wLjI0NTg3N0MxMC4zNzk4MzcsNS4yMjUyNjIsOS4yODQxNDQsNSw4LDV6Ii8+PHBhdGggY2xhc3M9InN0NiIgZD0iTTUuMDA0OTUsNS41NzI0ODVDNS4wNDE4ODgsNi41MTc0NjYsNS4zNTQ0OTEsMTAuNTY4MTc2LDgsMTEuNDUwMDEyVjkuNTMxMDh2LTEuMjAzMzRWNUM2LjcxNTg1Niw1LDUuNjIwMTYyLDUuMjI1MjYyLDUuMTkyMTg2LDUuMzI2NjA4QzUuMDc1ODE4LDUuMzU0MTY1LDUuMDAwMjc4LDUuNDUyOTksNS4wMDQ5NSw1LjU3MjQ4NXoiLz48cGF0aCBjbGFzcz0ic3Q3IiBkPSJNNS41MTYyMzUsNS43NjY3MjRDNi4wMTM2MTEsNS42NjEwMTEsNi45NDQ3NjMsNS41LDgsNS41VjVDNi43MTU4NTYsNSw1LjYyMDE2Miw1LjIyNTI2Miw1LjE5MjE4Niw1LjMyNjYwOEM1LjA3NTgxOCw1LjM1NDE2NSw1LjAwMDI3OCw1LjQ1Mjk5LDUuMDA0OTUsNS41NzI0ODVDNS4wNDE4ODgsNi41MTc0NjYsNS4zNTQ0OTEsMTAuNTY4MTc2LDgsMTEuNDUwMDEydi0wLjUzMjk1OUM1Ljk2ODAxOCwxMC4wODgxMzUsNS41ODczNDEsNi44ODk2NDgsNS41MTYyMzUsNS43NjY3MjR6Ii8+PHBhdGggY2xhc3M9InN0OCIgZD0iTTkuMzIxMzUsNS4wNzY3MjFjLTAuMzg0NzY2LTAuMDQyNDgtMC44MTEzNC0wLjA3MzA1OS0xLjI2NzU3OC0wLjA3NTMxN0M4LjAzNTQsNS4wMDEyODIsOC4wMTg0MzMsNSw4LDVMNy4yMTIxMiw2LjE3ODAxMkw4LjA0Njg3NSw2LjcxODc1TDcuMzI5MDYyLDcuNDU0NDE5TDcuOTg0Mzc1LDguMTU2MjVMNy40NDM3MjYsOS4wNTYyMTNsMS4wNzE4OTktMS4wNDA1ODhsLTAuNTQ2ODc1LTAuNTYyNWwwLjg3MTg0My0wLjg2MTQ2NEw4LDZsMC4zOTA2MjUtMC40ODQzNzVjMCwwLDAuNDc2MjE3LDAuMDE2NjY2LDAuNzY4OTgyLDAuMDQ5NzQ0czEuMDIzMjU0LDAuMTM3MzksMS4zMjQ2NDYsMC4yMDE0MTZjLTAuMDY5NjQxLDEuMTIyNDk4LTAuNDQ2Nzc3LDQuMzIwMTktMi40ODQxOTIsNS4xNTAzM0w4LDEwLjkxNzA1M3YwLjUzMjk1OWMyLjY0NDc5NC0wLjg4MTU5OCwyLjk1Nzk0My00LjkzMDM1NSwyLjk5NTAyLTUuODc2NzU5YzAuMDA0NzA0LTAuMTIwMDQ2LTAuMDY5OTU3LTAuMjE4NTQtMC4xODY5NC0wLjI0NTg5QzEwLjUzNzY4Niw1LjI2NDE0OCwxMC4wMDA4MDgsNS4xNTE3OTgsOS4zMjEzNSw1LjA3NjcyMXoiLz48L3N2Zz4=',  # noqa E501
        'manager_only': False,
        'name': 'intelamt'
    },
        {
            'unsupported': False,
            'cloud_only': False,
            'desc': 'A full system scan suitable for any host.',
            'order': 1,
            'subscription_only': False,
            'is_was': 'None',
            'title': 'Basic Network Scan',
            'is_agent': 'None',
            'uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
            'icon':
                'PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48IURPQ1RZUEUgc3ZnIFBVQkxJQyAiLS8vVzNDLy9EVEQgU1ZHIDEuMS8vRU4iICJodHRwOi8vd3d3LnczLm9yZy9HcmFwaGljcy9TVkcvMS4xL0RURC9zdmcxMS5kdGQiPjxzdmcgdmVyc2lvbj0iMS4xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHBhdGggZmlsbD0iIzZmYmY0YSIgZD0iTTcgMzcuOTQ0YzAgMC41NTItMC40NDggMS0xIDFzLTEtMC40NDgtMS0xYzAtMC41NTIgMC40NDgtMSAxLTFzMSAwLjQ0OCAxIDF6Ij48L3BhdGg+PHBhdGggZmlsbD0iIzZmYmY0YSIgZD0iTTExIDM3Ljk0NGMwIDAuNTUyLTAuNDQ4IDEtMSAxcy0xLTAuNDQ4LTEtMWMwLTAuNTUyIDAuNDQ4LTEgMS0xczEgMC40NDggMSAxeiI+PC9wYXRoPjxwYXRoIGZpbGw9IiM2ZmJmNGEiIGQ9Ik01NSAzNy45NDRjMCAwLjU1Mi0wLjQ0OCAxLTEgMXMtMS0wLjQ0OC0xLTFjMC0wLjU1MiAwLjQ0OC0xIDEtMXMxIDAuNDQ4IDEgMXoiPjwvcGF0aD48cGF0aCBmaWxsPSIjNmZiZjRhIiBkPSJNNTkgMzcuOTQ0YzAgMC41NTItMC40NDggMS0xIDFzLTEtMC40NDgtMS0xYzAtMC41NTIgMC40NDgtMSAxLTFzMSAwLjQ0OCAxIDF6Ij48L3BhdGg+PHBhdGggZmlsbD0iIzZmYmY0YSIgZD0iTTMyLjU3OCA2MC41NTFsLTcuNTA0LTQwLjg1OC0zLjYxOSAxOS4zMDdoLTcuNDU1Yy0wLjU1MyAwLTEtMC40NDktMS0xczAuNDQ3LTEgMS0xaDUuNzQ0bDUuMjYtMzMuNTkyIDcuNzM4IDQwLjY5MSA2LjY0NS0yOC4xNDggNS4wOTggMjEuMDQ5aDUuNTE2YzAuNTUxIDAgMSAwLjQ0OSAxIDFzLTAuNDQ5IDEtMSAxaC03LjA4NmwtMy4zMzItMTEuNDAyLTcuMDA0IDMyLjk1M3oiPjwvcGF0aD48L3N2Zz4=',  # noqa E501
            'manager_only': False,
            'name': 'basic'
        }]
    name = 'Example Managed Cred Scan'
    targets = ['127.0.0.1']
    scan_id = 'template-b4e5aea9-ab26-5cf3-3a76-98e216211cd390d1e4e488585988'

    responses.add(
        responses.POST,
        url=SCAN_BASE_URL,
        json={'scan': create_resp_data}
    )
    responses.add(
        responses.GET,
        url=f'{BASE_URL}/editor/policy/templates',
        json={'templates': policy_template_res}
    )

    resp = api.v3.vm.scans.create(name=name, targets=targets)
    assert isinstance(resp, dict)
    assert resp['id'] == scan_id


@responses.activate
def test_copy(api):
    '''
    Test the copy endpoint
    '''
    scan_id = 'fcb652c3-8567-4b3c-a8d1-1926196cbef415c4912d35e1c64c'
    copy_resp_data = {
        'timezone': 'US/Central',
        'enabled': False,
        'last_modification_date': '2019-12-31T20:50:23.635Z',
        'status': 'empty',
        'user_permissions': 128,
        'owner': 'user@example.com',
        'starttime': None,
        'control': True,
        'id': 'fcb652c3-8567-4b3c-a8d1-1926196cbef415c4912d35e1c64c',
        'rrules': None,
        'creation_date': '2019-12-31T20:50:23.635Z',
        'read': False,
        'shared': False,
        'name': 'Copy of Basic Network Scan - Daily'
    }

    responses.add(
        responses.POST,
        url=f'{SCAN_BASE_URL}/{scan_id}/copy',
        json=copy_resp_data
    )
    resp = api.v3.vm.scans.copy(scan_id)
    assert resp == copy_resp_data
    assert resp['id'] == scan_id


@responses.activate
def test_delete(api):
    '''
    Test the delete endpoint
    '''
    scan_id = 'fcb652c3-8567-4b3c-a8d1-1926196cbef415c4912d35e1c64c'
    responses.add(
        responses.DELETE,
        url=f'{SCAN_BASE_URL}/{scan_id}',
    )
    resp = api.v3.vm.scans.delete(scan_id)
    assert None is resp


@responses.activate
def test_delete_history(api):
    '''
    Test the delete history endpoint
    '''
    scan_id = 'fcb652c3-8567-4b3c-a8d1-1926196cbef415c4912d35e1c64c'
    history_id = 'v5g652c3-8567-4b3c-a8d1-1926196cbef415c4912d35e1c87e'
    responses.add(
        responses.DELETE,
        url=f'{SCAN_BASE_URL}/{scan_id}/history/{history_id}',
    )
    resp = api.v3.vm.scans.delete_history(scan_id, history_id)
    assert None is resp


def get_editor_details_data():
    '''
    Editor details object
    '''
    editor_resp_data = {
        'is_was': None,
        'user_permissions': 128,
        'owner': 'jyoti.patel@crestdatasys.com',
        'title': 'Basic Network Scan',
        'is_agent': None,
        'uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
        'filter_attributes': [
            {
                'operators': [
                    'eq',
                    'neq'
                ],
                'control': {
                    'type': 'dropdown',
                    'list': [
                        'True',
                        'False'
                    ]
                },
                'name': 'asset_inventory',
                'readable_name': 'Asset Inventory'
            },
            {
                'operators': [
                    'eq',
                    'neq'
                ],
                'control': {
                    'type': 'dropdown',
                    'list': [
                        'True',
                        'False'
                    ]
                },
                'name': 'exploit_framework_canvas',
                'readable_name': 'CANVAS Exploit Framework'
            }
        ],
        'settings': {
            'basic': {
                'inputs': [
                    {
                        'type': 'entry',
                        'name': 'Name',
                        'id': 'name',
                        'default': 'Example Embedded Cred Scan',
                        'required': True
                    }],
                'title': 'Basic',
                'groups': [
                    {
                        'title': 'Schedule',
                        'name': 'schedule',
                        'enabled': True,
                        'rrules': None,
                        'timezone': None,
                        'starttime': None
                    }
                ],
                'sections': []
            },
            'assessment': {
                'inputs': 'None',
                'modes': {
                    'id': 'assessment_mode',
                    'name': 'mode',
                    'type': 'ui_radio',
                    'default': 'Custom',
                    'options': [
                        {
                            'desc': '<ul><li>General Settings:<ul><li>Avoid potential False alarms</li><li>Disable CGI scanning</li></ul></li><li>Web Applications:<ul><li>Disable web application scanning</li></ul></li></ul>',  # noqa E501
                            'name': 'Default'
                        }
                    ]
                },
                'title': 'Assessment',
                'groups': [
                    {
                        'inputs': 'None',
                        'title': 'General',
                        'name': 'general',
                        'sections': [
                            {
                                'inputs': [
                                    {
                                        'type': 'radio-group',
                                        'id': 'report_paranoia',
                                        'label': 'Override normal accuracy',
                                        'default': 'Normal',
                                        'options': [
                                            'Normal',
                                            'Avoid False alarms',
                                            'Paranoid (more False alarms)'
                                        ],
                                        'optionsLabels': [
                                            '',
                                            'Avoid potential False alarms',
                                            'Show potential False alarms'
                                        ]
                                    },
                                    {
                                        'type': 'checkbox',
                                        'id': 'thorough_tests',
                                        'label': 'Perform thorough tests (may disrupt your network or impact scan speed)',  # noqa E501
                                        'default': 'no'
                                    }
                                ],
                                'title': 'Accuracy',
                                'name': 'accuracy'
                            }
                        ]
                    }
                ],
                'sections': []
            },
            'advanced': {
                'inputs': 'None',
                'modes': {
                    'id': 'advanced_mode',
                    'name': 'mode',
                    'type': 'ui_radio',
                    'default': 'Custom',
                    'options': []
                },
                'title': 'Advanced',
                'groups': [],
                'sections': [
                    {
                        'inputs': [],
                        'title': 'General Settings',
                        'name': 'advanced'
                    }
                ]
            },
            'discovery': [],
            'report': {}
        },
        'name': 'basic'
    }
    return editor_resp_data


@responses.activate
def test_details(api):
    '''
    Test the details endpoint
    '''
    scan_id = '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65'
    editor_resp_data = get_editor_details_data()

    details_resp = {
        'settings':
            {'name': 'Example Embedded Cred Scan',
             'report_paranoia': 'Normal',
             'thorough_tests': 'no',
             'enabled': True,
             'rrules': None,
             'timezone': None,
             'starttime': None
             },
        'uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65'
    }

    responses.add(
        responses.GET,
        url=f'{BASE_URL}/editor/scan/{scan_id}',
        json=editor_resp_data
    )
    resp = api.v3.vm.scans.details(scan_id)
    assert resp == details_resp
    assert resp['uuid'] == scan_id


@responses.activate
def test_results(api):
    '''
    Test the results endpoint
    '''
    scan_id = '6d69ccd6-3a59-4188-8246-861bda08e1a4'
    results_resp_data = {
        'info': {
            'owner': 'test@test.com',
            'name': 'Example Embedded Cred Scan',
            'no_target': False,
            'folder_id': 'None',
            'control': True,
            'user_permissions': 128,
            'schedule_id':
                'template-b4e5aea9-ab26-5cf3-3a76-98e21621cd390d1e4e488585988',
            'edit_allowed': False,
            'scanner_name': 'US Cloud Scanner',
            'policy': 'Basic Network Scan',
            'shared': 'None',
            'object_id': 111,
            'tag_targets': 'None',
            'acls': [],
            'hostcount': 0,
            'id': '6d69ccd6-3a59-4188-8246-861bda08e1a4',
            'status': 'running',
            'scan_type': 'ps',
            'targets': '127.0.0.1',
            'alt_targets_used': False,
            'pci-can-upload': False,
            'scan_start': '2019-12-31T20:50:23.635Z',
            'timestamp': '2019-12-31T20:50:23.635Z',
            'is_archived': False,
            'reindexing': False,
            'haskb': True,
            'hasaudittrail': True,
            'scanner_start': 'None'
        },
        'hosts': [],
        'vulnerabilities': [],
        'comphosts': [],
        'compliance': [],
        'filters': [],
        'history': [],
        'notes': [],
        'remediations': {
            'num_cves': 0,
            'num_hosts': 1,
            'num_remediated_cves': 0,
            'num_impacted_hosts': 0,
            'remediations': [

            ]
        }
    }
    responses.add(
        responses.GET,
        url=f'{SCAN_BASE_URL}/{scan_id}',
        json=results_resp_data
    )
    resp = api.v3.vm.scans.results(scan_id)
    assert resp == results_resp_data
    assert resp['info']['id'] == scan_id


@responses.activate
def test_host_details(api):
    '''
    Test the details endpoint
    '''
    scan_id = '6d69ccd6-3a59-4188-8246-861bda08e1a4'
    host_id = '7f69ccd6-3a59-4188-8246-861bda08e1a4'
    host_resp_data = {
        'info': {
            'mac-address': None,
            'host-fqdn': 'matrixcentos5_matrix',
            'host-ip': '192.0.2.57',
            'operating-system': [
                'Linux Kernel 2.6.18-274.el5PAE on CentOS release 5.7 (Final)'
            ],
            'host_end': '2019-12-31T20:50:23.635Z',
            'host_start': '2019-12-31T20:50:23.635Z'
        },
        'vulnerabilities': [
            {
                'count': 7,
                'host_id': '7f69ccd6-3a59-4188-8246-861bda08e1a4',
                'hostname': '192.0.2.57',
                'plugin_family': 'Port scanners',
                'plugin_id': 14272,
                'plugin_name': 'Netstat Portscanner (SSH)',
                'severity': 0,
                'severity_index': 0,
                'vuln_index': 0
            }
        ],
        'compliance': [
            {
                'count': 1,
                'host_id': '7f69ccd6-3a59-4188-8246-861bda08e1a4',
                'hostname': '192.0.2.57',
                'plugin_family': 'Unix Compliance Checks',
                'plugin_id': '0042cf05a8358f531c68c8bd249a4874',
                'plugin_name':
                    'BSI-100-2: S 4.105: Telnet should be replaced by SSH.',
                'severity': 1,
                'severity_index': 0
            }
        ]
    }
    responses.add(
        responses.GET,
        url=f'{SCAN_BASE_URL}/{scan_id}/hosts/{host_id}',
        json=host_resp_data
    )
    resp = api.v3.vm.scans.host_details(scan_id, host_id)
    assert resp == host_resp_data
    assert resp['vulnerabilities'][0]['host_id'] == host_id


@responses.activate
def test_launch(api):
    '''
    Test the launch endpoint
    '''
    scan_id = '44346bcb-4afc-4db0-b283-2dd823fa8579'
    launch_resp_data = {
        'scan_id': '44346bcb-4afc-4db0-b283-2dd823fa8579'
    }
    responses.add(
        responses.POST,
        url=f'{SCAN_BASE_URL}/{scan_id}/launch',
        json=launch_resp_data
    )

    resp = api.v3.vm.scans.launch(scan_id)
    assert resp == scan_id


@responses.activate
def test_pause(api):
    '''
    Test the pause endpoint
    '''
    scan_id = '44346bcb-4afc-4db0-b283-2dd823fa8579'
    responses.add(
        responses.POST,
        url=f'{SCAN_BASE_URL}/{scan_id}/pause'
    )

    resp = api.v3.vm.scans.pause(scan_id)
    assert None is resp


@responses.activate
def test_set_read_status(api):
    '''
    Test the set read status endpoint
    '''
    scan_id = '44346bcb-4afc-4db0-b283-2dd823fa8579'
    read_status = False
    responses.add(
        responses.PUT,
        url=f'{SCAN_BASE_URL}/{scan_id}/status',
        match=[matchers.json_params_matcher({'read_status': read_status})],
    )

    resp = api.v3.vm.scans.set_read_status(scan_id, read_status)
    assert None is resp


@responses.activate
def test_resume(api):
    '''
    Test the resume endpoint
    '''
    scan_id = '44346bcb-4afc-4db0-b283-2dd823fa8579'
    responses.add(
        responses.POST,
        url=f'{SCAN_BASE_URL}/{scan_id}/resume'
    )

    resp = api.v3.vm.scans.resume(scan_id)
    assert None is resp


@responses.activate
def test_stop(api):
    '''
    Test the stop endpoint
    '''
    scan_id = '44346bcb-4afc-4db0-b283-2dd823fa8579'
    responses.add(
        responses.POST,
        url=f'{SCAN_BASE_URL}/{scan_id}/stop'
    )

    resp = api.v3.vm.scans.stop(scan_id)
    assert None is resp


@responses.activate
def test_schedule(api):
    '''
    Test the schedule endpoint
    '''
    scan_id = '44346bcb-4afc-4db0-b283-2dd823fa8579'
    schedule_resp_data = {
        'control': True,
        'enabled': False,
        'rrules': 'FREQ=DAILY;INTERVAL=1',
        'timezone': 'US/Central',
        'starttime': '2019-12-31T20:50:23.635Z'
    }
    responses.add(
        responses.PUT,
        url=f'{SCAN_BASE_URL}/{scan_id}/schedule',
        json=schedule_resp_data
    )

    resp = api.v3.vm.scans.schedule(scan_id, False)
    assert resp == schedule_resp_data
    assert resp['starttime'] == '2019-12-31T20:50:23.635Z'


@responses.activate
def test_status(api):
    scan_id = '44346bcb-4afc-4db0-b283-2dd823fa8579'
    status_resp_data = {
        'status': 'imported'
    }
    responses.add(
        responses.GET,
        url=f'{SCAN_BASE_URL}/{scan_id}/latest-status',
        json=status_resp_data
    )

    resp = api.v3.vm.scans.status(scan_id)
    assert resp == 'imported'


@responses.activate
def test_timezones(api):
    '''
    Test the timezones endpoint
    '''
    timezones_resp_data = {
        'timezones': [
            {
                'name': 'Africa/Abidjan',
                'value': 'Africa/Abidjan'
            },
            {
                'name': 'Europe/Tiraspol',
                'value': 'Europe/Tiraspol'
            }
        ]
    }
    responses.add(
        responses.GET,
        url=f'{SCAN_BASE_URL}/timezones',
        json=timezones_resp_data
    )

    resp = api.v3.vm.scans.timezones()
    assert resp[0] == 'Africa/Abidjan'


@responses.activate
def test_info(api):
    '''
    Test the info endpoint
    '''
    scan_id = 'template-2abaec51-c243-444a-afe3-673af35b165ac98ab9a2d2e18e78'
    history_id = '63d15524-fce5-4555-bcd1-5b3172f41925'
    info_resp_data = {
        'schedule_id':
            'template-2abaec51-c243-444a-afe3-673af35b165ac98ab9a2d2e18e78',
        'status': 'aborted',
        'is_archived': True,
        'scan_start': '2019-12-31T20:50:23.635Z',
        'owner_id': '842f4ba8-1163-4ae4-85bf-c84eefa62cb6',
        'owner': 'user2@example.com',
        'targets': '',
        'object_id': 10509951,
        'id': '63d15524-fce5-4555-bcd1-5b3172f41925',
        'scan_end': None,
        'scan_type': 'remote',
        'name': 'Advanced Windows Servers Scan'
    }
    responses.add(
        responses.GET,
        url=f'{SCAN_BASE_URL}/{scan_id}/history/{history_id}',
        json=info_resp_data
    )
    resp = api.v3.vm.scans.info(scan_id, history_id)
    assert resp == info_resp_data
    assert resp['id'] == history_id


@responses.activate
def test_auto_targets(api):
    '''
    Test the auto-targets endpoint
    '''
    auto_targets_resp_data = {
        'missed_targets': [
            'example.com',
            'localhost'
        ],
        'total_missed_targets': 2,
        'matched_resource_ids': [
            '4d636d44-76ba-4f81-bfc6-6b9a0de66ee9'
        ],
        'total_matched_resource_ids': 1
    }
    responses.add(
        responses.POST,
        url=f'{SCAN_BASE_URL}/check-auto-targets',
        json=auto_targets_resp_data
    )
    resp = api.v3.vm.scans.check_auto_targets(5, 2)
    assert resp == auto_targets_resp_data
    assert resp['missed_targets'][0] == 'example.com'


@responses.activate
def test_export(api, text_contents):
    '''
    Test the export endpoint
    '''
    # todo => export depends on parse filter => fix it once parse filter is
    #  ready and merged into develop
    scan_id = 'template-2abaec51-c243-444a-afe3-673af35b165ac98ab9a2d2e18e78'
    file_id = 778874546
    scan_filters_resp_data = {'filters': [
        {
            'name': 'host.id',
            'readable_name': 'Asset ID',
            'control': {
                'type': 'entry',
                'regex': '[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}(,[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})*',  # noqa E501
                'readable_regex': '01234567-abcd-ef01-2345-6789abcdef01'
            },
            'operators': [
                'eq',
                'neq',
                'match',
                'nmatch'
            ],
            'group_name': 'None'
        },
        {
            'name': 'tracking.state',
            'readable_name': 'Vulnerability State',
            'control': {
                'type': 'dropdown',
                'list': [
                    'New',
                    'Fixed',
                    'Active',
                    'Resurfaced'
                ]
            },
            'operators': [
                'eq',
                'neq'
            ],
            'group_name': 'None'
        }
    ]}
    export_resp_data = {
        'file': 778874546,
        'temp_token':
            '995bdb656fc6dc5d76e18ccafe7fbd390618fcd0257e0e1aa121f4412a6f7ecc'
    }

    responses.add(
        responses.POST,
        url=f'{SCAN_BASE_URL}/{scan_id}/export',
        json=export_resp_data
    )
    responses.add(
        responses.GET,
        url=f'{BASE_URL}/scans/{scan_id}/export/{file_id}/status',
        json={'status': 'ready'}
    )
    responses.add(
        responses.GET,
        url=f'{SCAN_BASE_URL}/{scan_id}/export/{file_id}/download',
        body=text_contents
    )
    responses.add(
        responses.GET,
        url=f'{BASE_URL}/filters/scans/reports',
        json=scan_filters_resp_data
    )

    # dummy_file_path = os.path.join(
    #     os.path.dirname(os.path.abspath(__file__)), 'scans_export.txt'
    # )
    # with open(dummy_file_path, 'wb+') as fobj:
    #     api.v3.vm.scans.export(scan_id, fobj=fobj)

    # with open(dummy_file_path, 'rb') as txt_output:
    #     assert txt_output.read() == text_contents
    #
    # os.remove(dummy_file_path)


@responses.activate
def test_import(api):
    '''
    Test the import endpoint
    '''
    folder_id = '63d15524-fce5-4555-bcd1-5b3172f41925'
    file_upload_resp_data = {
        'fileuploaded': 'scan_targets.txt'
    }
    import_resp_data = {
        'scan': {
            'timezone': None,
            'last_modification_date': '2019-12-31T20:50:23.635Z',
            'status': 'imported',
            'user_permissions': 128,
            'folder_id': '63d15524-fce5-4555-bcd1-5b3172f41925',
            'owner': 'user2@example.com',
            'control': None,
            'starttime': None,
            'id': 'e192840b-e7cc-4586-a482-4495758ed8560e3fa8eea4c7cb27',
            'rrules': None,
            'creation_date': '2019-12-31T20:50:23.635Z',
            'read': False,
            'name': 'KitchenSinkScan',
            'shared': False
        }
    }
    responses.add(
        responses.POST,
        url=f'{SCAN_BASE_URL}/import',
        json=import_resp_data
    )
    responses.add(
        responses.POST,
        url=f'{BASE_URL}/file/upload',
        json=file_upload_resp_data
    )

    dummy_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'scans_targets.txt'
    )
    with open(dummy_file_path, 'wb+') as fobj:
        resp = api.v3.vm.scans.import_scan(fobj, folder_id=folder_id)
    assert resp == import_resp_data
    assert resp['scan']['folder_id'] == folder_id


@responses.activate
def test_attachment(api, text_contents):
    '''
    Test the attachment endpoint
    '''
    scan_id = '63d15524-fce5-4555-bcd1-5b3172f41925'
    attachment_id = '7dd15524-fce5-4555-bcd1-5b3172f41925'

    responses.add(
        responses.GET,
        url=f'{SCAN_BASE_URL}/{scan_id}/attachments/{attachment_id}',
        body=text_contents
    )

    dummy_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'scans_attachments.txt'
    )
    with open(dummy_file_path, 'wb+') as fobj:
        api.v3.vm.scans.attachment(fobj=fobj, attachment_id=attachment_id,
                                   key='test_1', scan_id=scan_id)

    with open(dummy_file_path, 'rb') as txt_output:
        assert txt_output.read() == text_contents

    os.remove(dummy_file_path)


@responses.activate
def test_create_scan_schedule(api):
    '''
    Test the create scan schedule endpoint
    '''
    validated_data = {
        'rrules': 'FREQ=ONETIME;INTERVAL=1',
        'enabled': True,
        'launch': 'ONETIME',
        'starttime': '2021-12-31T09:00:00+00:00',
        'timezone': 'Etc/UTC',
        'scheduleScan': 'yes'
    }
    timezones_resp_data = {
        'timezones': [
            {
                'name': 'Africa/Abidjan',
                'value': 'Africa/Abidjan'
            },
            {
                'name': 'Europe/Tiraspol',
                'value': 'Europe/Tiraspol'
            }
        ]
    }
    responses.add(
        responses.GET,
        url=f'{BASE_URL}/scans/timezones',
        json=timezones_resp_data
    )
    resp = api.v3.vm.scans.create_scan_schedule(enabled=True)
    assert resp['launch'] == validated_data['launch']


@responses.activate
def test_configure_scan_schedule(api):
    '''
    Test the configure scan schedule endpoint
    '''
    scan_id = '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65'
    editor_resp_data = get_editor_details_data()
    responses.add(
        responses.GET,
        url=f'{BASE_URL}/editor/scan/{scan_id}',
        json=editor_resp_data
    )
    timezones_resp_data = {
        'timezones': [
            {
                'name': 'Africa/Abidjan',
                'value': 'Africa/Abidjan'
            },
            {
                'name': 'Europe/Tiraspol',
                'value': 'Europe/Tiraspol'
            }
        ]
    }
    responses.add(
        responses.GET,
        url=f'{BASE_URL}/scans/timezones',
        json=timezones_resp_data
    )

    validated_data = {
        'rrules': 'FREQ=ONETIME;INTERVAL=2',
        'enabled': True,
        'launch': 'ONETIME',
        'starttime': '2021-12-31T08:30:00+00:00',
        'timezone': 'Etc/UTC',
        'scheduleScan': 'yes'
    }

    resp = api.v3.vm.scans.configure_scan_schedule(scan_id, enabled=True)
    assert resp['timezone'] == validated_data['timezone']


@responses.activate
def test_convert_credentials(api):
    '''
    Test the convert credentials endpoint
    '''

    details_resp_data = {
        'name': 'Windows devices (Headquarters)',
        'description':
            'Use for scans of Windows devices located at headquarters.',
        'category': {
            'id': 'Host',
            'name': 'Host',
        },
        'type': {
            'id': 'Windows',
            'name': 'Windows',
        },
        'ad_hoc': False,
        'user_permissions': 64,
        'settings': {
            'domain': "",
            'username': 'user@example.com',
            'auth_method': 'Password',
        },
        'permissions': [
            {
                'grantee_id': '59042c90-5379-43a2-8cf4-87d97f7cb68f',
                'type': 'user',
                'permissions': 64,
                'name': 'user1@tenable.com',
            }
        ],
    }
    updated_cred_id = 'aa57ae93-45e5-4316-8e16-501ebce4ecb7'
    cred_id = 'cdd60f2b-8108-49d5-89df-58add7fa1075'
    scan_id = '00000000-0000-0000-0000-000000000000'
    responses.add(
        responses.GET,
        url=f'{BASE_URL}/credentials/{cred_id}',
        json=details_resp_data
    )
    responses.add(
            responses.POST,
            url=f'{SCAN_BASE_URL}/{scan_id}/credentials/{cred_id}/upgrade',
            json={
                'id': updated_cred_id
            }
        )

    data = api.v3.vm.scans.convert_credentials(
        cred_id,
        scan_id
    )
    assert data == updated_cred_id


@responses.activate
def test_search(api):
    '''
    Test the search method
    '''
    fields = [
        'name',
        'type',
        'id'
    ]
    sort = [('creation_date', 'desc')]
    filters = ('status', 'eq', 'completed')

    payload = {
        'fields': fields,
        'limit': 200,
        'sort': [{'creation_date': 'desc'}],
        'filter': {
            'property': 'status',
            'operator': 'eq',
            'value': 'completed'
        }
    }

    api_response = {
        'scans': [
            {
                'legacy': False,
                'permissions': 128,
                'type': None,
                'read': True,
                'last_modification_date': '2021-12-31T09:00:00+00:00',
                'creation_date': '2021-12-31T09:00:00+00:00',
                'status': 'imported',
                'id': 'fd7d0d8e-c0e1-4439-97a5-d5c3a5c2d369ab8f7ecb158c480e',
                'shared': False,
                'user_permissions': 128,
                'owner': 'user2@example.com',
                'schedule_id':
                    'b0eeabbe-a612-429a-a60e-0f68eafb8c36f60557ee0e264228',
                'timezone': None,
                'rrules': None,
                'starttime': '2021-12-31T09:00:00+00:00',
                'enabled': False,
                'control': False,
                'name': 'KitchenSinkScan'
            }
        ],
        'pagination': {
            'total': 1,
            'next': 'nextToken'
        }
    }
    responses.add(
        responses.POST,
        f'{SCAN_BASE_URL}/search',
        match=[matchers.json_params_matcher(payload)],
        json=api_response
    )

    iterator = api.v3.vm.scans.search(
        fields=fields, limit=200, sort=sort, filter=filters
    )
    assert isinstance(iterator, SearchIterator)

    event_list = []
    for event in iterator:
        event_list.append(event)
    assert len(event_list) == api_response['pagination']['total']

    iterator = api.v3.vm.scans.search(
        fields=fields, return_csv=True, sort=sort, limit=200, filter=filters
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.vm.scans.search(
        fields=fields, return_resp=True, limit=200, sort=sort, filter=filters
    )
    assert isinstance(resp, Response)
