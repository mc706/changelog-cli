"""
Run Test Suite
"""

from invoke import task


@task
def test(context):
    """
    Runs Test Suite
    """
    context.run('coverage run -m unittest discover')
