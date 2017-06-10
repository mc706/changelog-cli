import click

from changelog.utils import ChangelogUtils
from changelog.exceptions import ChangelogDoesNotExistError


def print_version(ctx, _, value):
    from changelog._version import __version__ as v
    if not value or ctx.resilient_parsing:
        return
    click.echo(v)
    ctx.exit()


@click.group()
@click.option('-v', '--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def cli():
    pass


@cli.command(help="Create CHANGELOG.md with some basic documentation")
def init():
    click.echo('Initializing Changelog')
    CL = ChangelogUtils()
    outcome = CL.initialize_changelog_file()
    click.echo(outcome)


@cli.command(help="add a line to the NEW section")
@click.argument("message")
def new(message):
    CL = ChangelogUtils()
    try:
        CL.update_section('new', message)
    except ChangelogDoesNotExistError:
        if click.confirm("No CHANGELOG.md Found, do you want to create one?"):
            CL.initialize_changelog_file()
            CL.update_section('new', message)


@cli.command(help="add a line to the CHANGES section")
@click.argument("message")
def change(message):
    CL = ChangelogUtils()
    try:
        CL.update_section('change', message)
    except ChangelogDoesNotExistError:
        if click.confirm("No CHANGELOG.md Found, do you want to create one?"):
            CL.initialize_changelog_file()
            CL.update_section('change', message)


@cli.command(help="add a line to the FIXES section")
@click.argument("message")
def fix(message):
    CL = ChangelogUtils()
    try:
        CL.update_section('fix', message)
    except ChangelogDoesNotExistError:
        if click.confirm("No CHANGELOG.md Found, do you want to create one?"):
            CL.initialize_changelog_file()
            CL.update_section('fix', message)


@cli.command(help="add a line to the BREAKS section")
@click.argument("message")
def breaks(message):
    CL = ChangelogUtils()
    try:
        CL.update_section('break', message)
    except ChangelogDoesNotExistError:
        if click.confirm("No CHANGELOG.md Found, do you want to create one?"):
            CL.initialize_changelog_file()
            CL.update_section('break', message)


@cli.command(help="cut a release and update the changelog accordingly")
@click.option('--patch', 'release_type', flag_value='patch')
@click.option('--minor', 'release_type', flag_value='minor')
@click.option('--major', 'release_type', flag_value='major')
@click.option('--suggest', 'release_type', flag_value='suggest', default=True)
@click.option('--yes', 'auto_confirm', is_flag=True)
def release(release_type, auto_confirm):
    CL = ChangelogUtils()
    try:
        new_version = CL.get_new_release_version(release_type)
        if auto_confirm:
            CL.cut_release()
        else:
            if click.confirm("Planning on releasing version {}. Proceed?".format(new_version)):
                CL.cut_release(release_type)
    except ChangelogDoesNotExistError:
        if click.confirm("No CHANGELOG.md Found, do you want to create one?"):
            CL.initialize_changelog_file()


@cli.command(help="returns the suggested next version based on the current logged changes")
def suggest():
    CL = ChangelogUtils()
    try:
        new_version = CL.get_new_release_version('suggest')
        click.echo(new_version)
    except ChangelogDoesNotExistError:
        pass


@cli.command(help="returns the current application version based on the changelog")
def current():
    CL = ChangelogUtils()
    try:
        version = CL.get_current_version()
        click.echo(version)
    except ChangelogDoesNotExistError:
        pass
