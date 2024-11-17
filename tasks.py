from invoke import task


@task
def req_compile(c):
    c.run("pip-compile -v requirements/requirements.in")


@task
def req_upgrade(c):
    c.run("pip-compile -v -U requirements/requirements.in")


@task
def build(c):
    c.run("pip install -r requirements/requirements.txt")


@task
def rebuild(c):
    c.run("inv req_compile && inv build")


@task
def lint(c, path="src"):
    c.run(f"pylint --fail-under=9.0 --rcfile=.pylintrc {path}")
