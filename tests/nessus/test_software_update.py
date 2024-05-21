import pytest
import responses


@responses.activate
def test_software_update_schedule(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/settings/software-update'
                  )
    nessus.software_update.update()


@responses.activate
def test_software_update_settings(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/settings/software-update'
                  )
    nessus.software_update.settings(update='all',
                                    auto_update_delay=1
                                    )