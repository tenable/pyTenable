'''
uploads
=======

The uploads methods are abstractions to make uploading an image into Container
Security easier for the user.

Methods available on ``cs.uploads``:

.. rst-class:: hide-signature
.. autoclass:: UploadAPI

    .. automethod:: docker_push
'''
from .base import CSEndpoint
from tenable.errors import PackageMissingError

class UploadAPI(CSEndpoint):
    def docker_push(self, name, tag=None, cs_name=None, cs_tag=None):
        '''
        Uploads an image into Tenable.io Container Security using docker.

        Args:
            name (str): The name of the local docker image.
            tag (str, optional):
                The tag for the local docker image. Default is `latest`.
            cs_name (str, optional):
                The repository and name for the image in Container Security.  If
                nothing is specified, the default is `library/{name}`
            cs_tag (str, optional):
                The tag to apply to the image in Container Security.  If nothing
                is specified, then we will use the current setting of the tag
                parameter instead.

        Return:
            str: The image identifier.
        '''
        # as we may not need to perform this action, we will import and initiate
        # the docker environment at the time of the push.
        try:
            import docker
        except ImportError:
            raise PackageMissingError(
                'The python package docker is required to use cs.uploads.docker_push')
        d = docker.from_env(version='auto')

        self._check('name', name, str)
        self._check('tag', tag, str)
        self._check('cs_name', cs_name, str)
        self._check('cs_tag', cs_tag, str)

        if not cs_name:
            cs_name = 'library/{}'.format(name)

        if not cs_tag:
            if not tag:
                cs_tag = tag
            else:
                cs_tag = 'latest'

        # get the image from the docker daemon.
        image = d.images.get('{}:{}'.format(name, tag) if tag else name)

        # build the remote tag
        remote = '{}/{}'.format(self._api._registry, cs_name)

        # upload the image to CS

        image.tag(remote, tag=cs_tag)
        d.images.push(remote, tag=cs_tag, auth_config={
            'username': self._api._access_key,
            'password': self._api._secret_key
        })
        d.images.remove('{}:{}'.format(remote, cs_tag))

        # return the image id
        return image.id.split(':')[1][:12]