import os
import shutil
import sys
from invoke import task


DEFAULT_DOCKER_IMAGE = 'orbin/gramhopper'
DEFAULT_DOCKER_TAG = 'latest'
DOCKER_IMAGE_ENV_VARIABLE = 'DOCKER_IMAGE_TAG'
TASK_SUCCESS_CODE = 0
TASK_FAILURE_CODE = 1
SUCCESS_COLOR = '\033[92m'
FAILURE_COLOR = '\033[91m'
DEFAULT_COLOR = '\033[39m'


@task
def build(context, package=True, docker_image=True, docker_tag=DEFAULT_DOCKER_TAG, docs=False):
    if package:
        print('Building package...')
        context.run('python setup.py sdist bdist_wheel', echo=True)

    if docker_image:
        print('Building docker image...')

        # If not specified the tag as a flag, the tag from the environment variable is preferred
        if docker_tag == DEFAULT_DOCKER_TAG and \
                DOCKER_IMAGE_ENV_VARIABLE in os.environ:
            docker_tag = os.environ[DOCKER_IMAGE_ENV_VARIABLE]

        context.run(f'docker build -t {DEFAULT_DOCKER_IMAGE}:{docker_tag} .', echo=True)

    if docs:
        build_docs(context)


@task
def build_docs(context):
    print('Building docs...')
    with context.cd('docs'):
        context.run('make html', echo=True)


@task
def lint(context):
    source_code_dirs = './*.py ./gramhopper'
    test_code_dirs = './tests'
    exit_code = TASK_SUCCESS_CODE

    print('Running pylint on source code...')
    result = context.run(f'pylint {source_code_dirs}', warn=True, echo=True)
    if not result.exited == TASK_SUCCESS_CODE:
        exit_code = TASK_FAILURE_CODE

    print('Running pylint on test code...')
    result = context.run(f'pylint --rcfile=./tests/tests.pylintrc {test_code_dirs}',
                         warn=True,
                         echo=True)
    if not result.exited == TASK_SUCCESS_CODE:
        exit_code = TASK_FAILURE_CODE

    print('Running flake8...')
    result = context.run('flake8 --exclude=venv', warn=True, echo=True)
    if not result.exited == TASK_SUCCESS_CODE:
        exit_code = TASK_FAILURE_CODE

    print('Running pytype...')
    python_version = f'{sys.version_info.major}.{sys.version_info.minor}'
    cmd = f'pytype  --config ./setup.cfg -V {python_version} {source_code_dirs} {test_code_dirs}'
    result = context.run(cmd, warn=True, echo=True)
    if not result.exited == TASK_SUCCESS_CODE:
        exit_code = TASK_FAILURE_CODE

    message_color = SUCCESS_COLOR if exit_code == TASK_SUCCESS_CODE else FAILURE_COLOR
    status_string = 'successfully' if exit_code == TASK_SUCCESS_CODE else 'with errors'

    finished_string = f'{message_color}Lint task finished {status_string} {DEFAULT_COLOR}'
    print(finished_string)
    sys.exit(exit_code)


@task
def test(context):
    gramhopper_dir = os.path.join(os.path.expanduser('~'), '.gramhopper')
    gramhopper_backup_dir = os.path.join(os.path.expanduser('~'), '.gramhopper_bak')

    if os.path.exists(gramhopper_dir):
        print('Backing up configuration directory...')
        shutil.copytree(gramhopper_dir, gramhopper_backup_dir)

    print('Copying test assets...')
    shutil.rmtree(gramhopper_dir, ignore_errors=True)
    shutil.copytree('./tests/assets/.gramhopper', gramhopper_dir)

    print('Running tests...')
    context.run('pytest', echo=True)

    print('Removing test assets...')
    shutil.rmtree(gramhopper_dir)

    if os.path.exists(gramhopper_backup_dir):
        print('Restoring configuration directory...')
        shutil.copytree(gramhopper_backup_dir, gramhopper_dir)
        shutil.rmtree(gramhopper_backup_dir)


@task
def publish(context, docker_tag=None, docker_latest=False, production_pypi=False):
    pypi_type = 'production' if production_pypi else 'test'
    print(f'Uploading package to {pypi_type} PyPI...')
    repo_url_flag = '' if production_pypi else '--repository-url https://test.pypi.org/legacy/'
    context.run(f'twine upload {repo_url_flag} dist/*', echo=True)

    if docker_tag:
        publish_docker_image(context, f'{DEFAULT_DOCKER_IMAGE}:{docker_tag}')

    if docker_latest:
        publish_docker_image(context, f'{DEFAULT_DOCKER_IMAGE}:latest')


def publish_docker_image(context, full_image_name):
    print(f'Uploading docker image {full_image_name} to PyPI...')
    context.run(f'docker push {full_image_name}', echo=True)


@task
def clean(context,  # pylint: disable=too-many-arguments
          package=False,
          docker=False,
          docs=False,
          lint=False,  # pylint: disable=redefined-outer-name
          test=False,  # pylint: disable=redefined-outer-name
          all=False):  # pylint: disable=redefined-builtin

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
        clean_package()

    if docker:
        print('Removing docker images...')
        clean_docker(context)

    if docs:
        print('Removing docs build outputs...')
        shutil.rmtree('./docs/build', ignore_errors=True)

    if lint:
        print('Removing lint outputs and cache files...')
        shutil.rmtree('./pytype_output', ignore_errors=True)
        shutil.rmtree('./.pytype', ignore_errors=True)

    if test:
        print('Removing test outputs and cache files...')
        shutil.rmtree('./.pytest_cache', ignore_errors=True)
        shutil.rmtree('./gramhopper_test.egg-info', ignore_errors=True)


def clean_package():
    shutil.rmtree('./build', ignore_errors=True)
    shutil.rmtree('./dist', ignore_errors=True)
    shutil.rmtree('./gramhopper.egg-info', ignore_errors=True)


def clean_docker(context):
    docker_result = context.run('docker', hide='both')
    # If docker is installed, remove both the image with the default tag and
    # the image with the tag from the environment variable
    if docker_result.exited == TASK_SUCCESS_CODE:
        tags_to_remove = [DEFAULT_DOCKER_IMAGE]
        if DOCKER_IMAGE_ENV_VARIABLE in os.environ:
            tags_to_remove.append(os.environ[DOCKER_IMAGE_ENV_VARIABLE])

        hashes_to_remove = []
        for tag in tags_to_remove:
            hash_result = context.run(f'docker images -q {tag}', hide='out')
            image_hash = hash_result.stdout.split('\n')[0].strip()
            if image_hash:
                hashes_to_remove.append(image_hash)

        if hashes_to_remove:
            hashes_to_remove = ' '.join(set(hashes_to_remove))
            context.run(f'docker rmi -f {hashes_to_remove}', echo=True)
        else:
            print('No docker images to remove')
    else:
        print('Docker is not installed on this machine')
