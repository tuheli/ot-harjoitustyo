from invoke import task


@task
def start_game(ctx):
    ctx.run("python3 src/index_game.py", pty=True)


@task
def start_editor(ctx):
    ctx.run("python3 src/index_editor.py", pty=True)


@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src", pty=True)


@task
def test(ctx):
    ctx.run("pytest src", pty=True)


@task
def lint(ctx):
    ctx.run("pylint src", pty=True)


@task
def coverage_report(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)
    ctx.run("coverage html", pty=True)