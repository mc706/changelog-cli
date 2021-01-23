import click

from changelog.utils import ChangelogUtils
from changelog.exceptions import ChangelogDoesNotExistError
from changelog._version import __version__ as v


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(v)
    ctx.exit()


@click.group()
@click.option('-v', '--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def cli() -> None:
    pass


@cli.command(help="Create CHANGELOG.md with some basic documentation")
def init() -> None:
    click.echo('Initializing Changelog')
    CL = ChangelogUtils()
    outcome = CL.initialize_changelog_file()
    click.echo(outcome)


def bind_section_command(name):
    @click.argument("message")
    def section_command(message: str) -> None:
        CL = ChangelogUtils()
        try:
            CL.update_section(name, message)
        except ChangelogDoesNotExistError:
            if click.confirm("No CHANGELOG.md found, do you want to create one?"):
                CL.initialize_changelog_file()
                CL.update_section(name, message)

    section_command.__name__ = name
    return section_command


for change_type in ChangelogUtils.TYPES_OF_CHANGE:
    section_command_func = bind_section_command(change_type)
    cli.command(
        name=change_type,
        help=f"Add a line to the '{change_type.capitalize()}' section"
    )(section_command_func)


@cli.command(help="cut a release and update the changelog accordingly")
@click.option('--patch', 'release_type', flag_value='patch')
@click.option('--minor', 'release_type', flag_value='minor')
@click.option('--major', 'release_type', flag_value='major')
@click.option('--suggest', 'release_type', flag_value='suggest', default=True)
@click.option('--yes', 'auto_confirm', is_flag=True)
def release(release_type: str, auto_confirm: bool) -> None:
    CL = ChangelogUtils()
    try:
        new_version = CL.get_new_release_version(release_type)
        if auto_confirm:
            CL.cut_release()
        else:
            if click.confirm(f"Planning on releasing version {new_version}. Proceed?"):
                CL.cut_release(release_type)
    except ChangelogDoesNotExistError:
        if click.confirm("No CHANGELOG.md found, do you want to create one?"):
            CL.initialize_changelog_file()


@cli.command(help="returns the suggested next version based on the current logged changes")
@click.option('--type', "release_type", is_flag=True)
def suggest(release_type: str) -> None:
    CL = ChangelogUtils()
    try:
        if release_type:
            click.echo(CL.get_release_suggestion())
        else:
            new_version = CL.get_new_release_version('suggest')
            click.echo(new_version)
    except ChangelogDoesNotExistError:
        pass


@cli.command(help="returns the current application version based on the changelog")
def current() -> None:
    CL = ChangelogUtils()
    try:
        version = CL.get_current_version()
        click.echo(version)
    except ChangelogDoesNotExistError:
        pass


@cli.command(help="view the current and unreleased portion of the changelog")
def view() -> None:
    CL = ChangelogUtils()
    try:
        data = CL.get_changelog_data()
        first = False
        for line in data:
            if CL.match_version(line):
                if first:
                    break
                first = True
            click.echo(line.strip())

    except ChangelogDoesNotExistError:
        if click.confirm("No CHANGELOG.md found, do you want to create one?"):
            CL.initialize_changelog_file()
