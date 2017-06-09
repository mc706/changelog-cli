import click

from changelog.utils import initialize_changelog_file, update_section, get_new_release_version, cut_release
from changelog.exceptions import ChangelogDoesNotExistError


@click.group()
def cli():
    pass


@cli.command(help="Create CHANGELOG.md")
def init():
    click.echo('Initializing Changelog')
    outcome = initialize_changelog_file()
    click.echo(outcome)


@cli.command(help="add a line to the NEW section")
@click.argument("message")
def new(message):
    try:
        update_section('new', message)
    except ChangelogDoesNotExistError:
        if click.confirm("No CHANGELOG.md Found, do you want to create one?"):
            initialize_changelog_file()
            update_section('new', message)


@cli.command(help="add a line to the CHANGES section")
@click.argument("message")
def change(message):
    try:
        update_section('change', message)
    except ChangelogDoesNotExistError:
        if click.confirm("No CHANGELOG.md Found, do you want to create one?"):
            initialize_changelog_file()
            update_section('change', message)


@cli.command(help="add a line to the Fixes section")
@click.argument("message")
def fix(message):
    try:
        update_section('fix', message)
    except ChangelogDoesNotExistError:
        if click.confirm("No CHANGELOG.md Found, do you want to create one?"):
            initialize_changelog_file()
            update_section('fix', message)


@cli.command(help="add a line to the Breaks section")
@click.argument("message")
def breaks(message):
    try:
        update_section('break', message)
    except ChangelogDoesNotExistError:
        if click.confirm("No CHANGELOG.md Found, do you want to create one?"):
            initialize_changelog_file()
            update_section('break', message)


@cli.command()
@click.option('--patch', 'release_type', flag_value='patch')
@click.option('--minor', 'release_type', flag_value='minor')
@click.option('--major', 'release_type', flag_value='major')
@click.option('--suggest', 'release_type', flag_value='suggest', default=True)
def release(release_type):
    try:
        new_version = get_new_release_version(release_type)
        if click.confirm("Planning on releasing version {}. Proceed?".format(new_version)):
            cut_release(release_type)
    except ChangelogDoesNotExistError:
        if click.confirm("No CHANGELOG.md Found, do you want to create one?"):
            initialize_changelog_file()
