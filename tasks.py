import os
from invoke import task


DEFAULT_DOCKER_IMAGE_TAG = 'orbin/gramhopper'
DOCKER_IMAGE_TAG_ENV_VARIABLE = 'DOCKER_IMAGE_TAG'

@task
def build(c, package=True, docker_image=True, docker_image_tag=DEFAULT_DOCKER_IMAGE_TAG):
    if package:
        print('Building package...')
        c.run('python setup.py sdist bdist_wheel')

    if docker_image:
        print('Building docker image...')

        # If not specified the tag as a flag, the tag from the environment variable is preferred
        if docker_image_tag == DEFAULT_DOCKER_IMAGE_TAG and \
                DOCKER_IMAGE_TAG_ENV_VARIABLE in os.environ:
            docker_image_tag = os.environ[DOCKER_IMAGE_TAG_ENV_VARIABLE]

        c.run(f'docker build -t {docker_image_tag} .')
