import os
import shutil
import sys
from invoke import task


DEFAULT_DOCKER_TAG = 'orbin/gramhopper'
DOCKER_TAG_ENV_VARIABLE = 'DOCKER_IMAGE_TAG'
TASK_SUCCESS_CODE = 0
TASK_FAILURE_CODE = 1


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
    exit_code = TASK_SUCCESS_CODE

    print('Running pylint on source code...')
    result = context.run(f'pylint {source_code_dirs}', warn=True)
    if not result.exited == TASK_SUCCESS_CODE:
        exit_code = TASK_FAILURE_CODE

    print('Running pylint on test code...')
    result = context.run(f'pylint --rcfile=./tests/tests.pylintrc {test_code_dirs}', warn=True)
    if not result.exited == TASK_SUCCESS_CODE:
        exit_code = TASK_FAILURE_CODE

    print('Running flake8...')
    result = context.run('flake8 --exclude=venv', warn=True)
    if not result.exited == TASK_SUCCESS_CODE:
        exit_code = TASK_FAILURE_CODE

    print('Running pytype...')

    python_version = '%d.%d' % (sys.version_info.major,  # pytype: disable=attribute-error
                                sys.version_info.minor)  # pytype: disable=attribute-error
    cmd = f'pytype  --config ./setup.cfg -V {python_version} {source_code_dirs} {test_code_dirs}'
    result = context.run(cmd, warn=True)
    if not result.exited == TASK_SUCCESS_CODE:
        exit_code = TASK_FAILURE_CODE

    finished_string = 'Lint task finished ' + \
                      ('successfully' if exit_code == TASK_SUCCESS_CODE else 'with errors')
    print(finished_string)
    sys.exit(exit_code)


@task
def test(context):
    print('Copying test assets...')
    # TODO backup and restore current ~/.gramhopper
    context.run('cp -R tests/assets/.gramhopper ~/.gramhopper')  # TODO change to python code

    print('Running tests...')
    context.run('pytest')

    # print('Removing test assets...')
    # context.run('rm ~/.gramhopper')  # TODO change to python code


@task
def clean(context, package=False, docker=False, docs=False, lint=False, test=False, all=False):

    if all:
        package = True
        docker = True
        docs = True
        lint = True
        test = True
    elif not any([package, docker, docs, lint, test]):
        # If no flag was specified, exit with an error
        print('Specified nothing to clean', file=sys.stderr)
        sys.exit(TASK_FAILURE_CODE)

    if package:
        print('Removing package build outputs...')
        shutil.rmtree('./build', ignore_errors=True)
        shutil.rmtree('./dist', ignore_errors=True)
        shutil.rmtree('./gramhopper.egg-info', ignore_errors=True)

    if docker:
        print('Removing docker images...')
        docker_result = context.run('docker', hide='both')
        # If docker is installed, remove both the image with the default tag and
        # the image with the tag from the environment variable
        if docker_result.exited == TASK_SUCCESS_CODE:
            tags_to_remove = [DEFAULT_DOCKER_TAG]
            if DOCKER_TAG_ENV_VARIABLE in os.environ:
                tags_to_remove.append(os.environ[DOCKER_TAG_ENV_VARIABLE])

            hashes_to_remove = []
            for tag in tags_to_remove:
                hash_result = context.run(f'docker images -q {tag}', hide='out')
                hash = hash_result.stdout.split('\n')[0].strip()
                if len(hash):
                    hashes_to_remove.append(hash)

            if len(hashes_to_remove):
                hashes_to_remove = ' '.join(set(hashes_to_remove))
                context.run(f'docker rmi -f {hashes_to_remove}')
            else:
                print('No docker images to remove')
        else:
            print('Docker is not installed on this machine')

    if docs:
        print('Removing docs build outputs...')
        shutil.rmtree('./docs/build', ignore_errors=True)

    if lint:
        print('Removing lint outputs and cache files...')
        shutil.rmtree('./pytype_output', ignore_errors=True)

    if test:
        print('Removing test outputs and cache files...')
        shutil.rmtree('./.pytest_cache', ignore_errors=True)
