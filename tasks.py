import os
import sys
from invoke import task


DEFAULT_DOCKER_TAG = 'orbin/gramhopper'
DOCKER_TAG_ENV_VARIABLE = 'DOCKER_IMAGE_TAG'
TASK_SUCCEEDED_CODE = 0
TASK_FAILED_CODE = 1


@task
def build(context, package=True, docker_image=True, docker_tag=DEFAULT_DOCKER_TAG, docs=False):
    if package:
        print('Building package...')
        context.run('python setup.py sdist bdist_wheel')

    if docker_image:
        print('Building docker image...')

        # If not specified the tag as a flag, the tag from the environment variable is preferred
        if docker_tag == DEFAULT_DOCKER_TAG and \
                DOCKER_TAG_ENV_VARIABLE in os.environ:
            docker_tag = os.environ[DOCKER_TAG_ENV_VARIABLE]

        context.run(f'docker build -t {docker_tag} .')

    if docs:
        build_docs(context)


@task
def build_docs(context):
    print('Building docs...')
    with context.cd('docs'):
        context.run('make html')


@task
def lint(context):
    source_code_dirs = './*.py ./gramhopper'
    test_code_dirs = './tests'
    exit_code = TASK_SUCCEEDED_CODE

    print('Running pylint on source code...')
    result = context.run(f'pylint {source_code_dirs}', warn=True)
    if not result.exited == TASK_SUCCEEDED_CODE:
        exit_code = TASK_FAILED_CODE

    print('Running pylint on test code...')
    result = context.run(f'pylint --rcfile=./tests/tests.pylintrc {test_code_dirs}', warn=True)
    if not result.exited == TASK_SUCCEEDED_CODE:
        exit_code = TASK_FAILED_CODE

    print('Running flake8...')
    result = context.run('flake8 --exclude=venv', warn=True)
    if not result.exited == TASK_SUCCEEDED_CODE:
        exit_code = TASK_FAILED_CODE

    print('Running pytype...')

    python_version = '%d.%d' % (sys.version_info.major,  # pytype: disable=attribute-error
                                sys.version_info.minor)  # pytype: disable=attribute-error
    cmd = f'pytype  --config ./setup.cfg -V {python_version} {source_code_dirs} {test_code_dirs}'
    result = context.run(cmd, warn=True)
    if not result.exited == TASK_SUCCEEDED_CODE:
        exit_code = TASK_FAILED_CODE

    finished_string = 'Lint task finished ' + \
                      ('successfully' if exit_code == TASK_SUCCEEDED_CODE else 'with errors')
    print(finished_string)
    sys.exit(exit_code)


@task
def test(context):
    print('Copying test assets...')
    context.run('cp -R tests/assets/.gramhopper ~/.gramhopper')

    print('Running tests...')
    context.run('pytest')
