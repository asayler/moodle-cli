#!/usr/bin/env python

import pprint

import click

import moodle.ws

@click.group()
@click.option('--url', default=None, help="Moodle URL")
@click.option('--token', default=None, help="Moodle Token")
@click.option('--username', default=None, help="Moodle Username")
@click.option('--password', default=None, help="Moodle Password")
@click.option('--service', default=None, help="Moodle Web Service Name")
@click.pass_context
def cli(ctx, url, token, username, password, service):

    if not url:
        url = click.prompt("URL", type=str)

    ctx.obj = ws = moodle.ws.WS(url, token)
    if not ws.is_authenticated():
        if not username:
            username = click.prompt("username", type=str)
        if not password:
            password = click.prompt("password", type=str, hide_input=True)
        if not service:
            service = click.prompt("service", type=str)
        if not ws.authenticate(username, password, service):
            raise click.ClickException("Could not authenticate")

@click.command()
@click.option('--aid', default=None, type=int, help="Assignment ID")
@click.option('--cmid', default=None, type=int, help="Assignment Course Module ID")
@click.pass_obj
def assignment(ws, aid, cmid):

    if not aid:
        if not cmid:
            raise click.ClickException("Requires either aid or cmid")

    res = ws.mod_assign_get_assignments([])

    asn = None
    courses = res['courses']
    for course in courses:
        if not asn:
            asns = course['assignments']
            for a in asns:
                if aid:
                    if (a['id'] == aid):
                        asn = a
                        break
                elif cmid:
                    if (a['cmid'] == cmid):
                        asn = a
                        break
        else:
            break

    if asn:
        pp = pprint.PrettyPrinter()
        click.echo(pp.pformat(asn))
    else:
        raise click.ClickException("Assignment not found")

@click.command()
def user():
    click.echo('Not yet implemented')

cli.add_command(assignment)
cli.add_command(user)

if __name__ == '__main__':
    cli()
