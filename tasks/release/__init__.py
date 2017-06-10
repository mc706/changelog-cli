"""
Release Task
"""

from invoke import task


@task
def release(context):
    """
    Release a new version of changelog-cli
    """
    clean(context)
    bump_version(context)
    release_changelog(context)
    build(context)
    publish(context)


def clean(context):
    """
    Clean dist and build folders
    :param context:
    :return:
    """
    context.run("rm -rf dist")
    context.run("rm -rf build")


def bump_version(context):
    """

    :param context:
    :return:
    """
    version = context.run('changelog suggest')
    with open(context['VERSION_FILE'], 'w') as version_file:
        version_file.write('__version__ = "{0}" \n'.format(version.stdout.strip()))


def release_changelog(context):
    """
    Runs changelog command to update changelog
    """
    context.run('changelog release --yes')


def build(context):
    """
    Build the current python version
    """
    context.run("python setup.py sdist bdist_wheel")


def publish(context):
    """
    Publish the package on pypi
    """
    context.run("twine upload dist/*")