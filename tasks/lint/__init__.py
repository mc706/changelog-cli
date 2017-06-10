"""
Code Linting
"""
from invoke import task


@task
def lint(context):
    """
    Runs quality checks through linter
    """
    context.run('prospector')
