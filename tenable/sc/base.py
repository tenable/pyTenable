from tenable.base import APIEndpoint, APIResultsIterator

class SCEndpoint(APIEndpoint):
    def _schedule_document_creator(self, kw):
        '''
        Handles creation of the schedule subdocument.
        '''
        if ('schedule_type' in kw and kw['schedule_type'] == 'ical'
            and 'schedule_start' in kw 
            and 'schedule_repeat' in kw):
            # effectively here we are flattening the schedule subdocument on the
            # developer end and reconstructing it for the SecurityCenter end.
            #
            # FR: eventually we should start checking the repeating rule and the
            #     datetime against the ical format.
            kw['schedule'] = {
                'type': 'ical',
                'start': self._check(
                    'schedule_start', kw['schedule_start'], str),
                'repeatRule': self._check(
                    'schedule_repeat', kw['schedule_repeat'], str),
            }
            del(kw['schedule_type'])
            del(kw['schedule_start'])
            del(kw['schedule_repeat'])

        elif 'schedule_type' in kw:
            # if the schedule type is not an ical repeating rule, then we will
            # populate a schedule document with just the type.
            kw['schedule'] = {'type': self._check('schedule_type', 
                kw['schedule_type'], str, choices=[
                    'dependent', 'never', 'rollover', 'template'])}
            del(kw['schedule_type'])
        return kw

class SCResultsIterator(APIResultsIterator):
    pass