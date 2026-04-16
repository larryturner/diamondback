"""**Description**
    Nox defines sessions to support project administration.

**Environment**
    Environment variables may be electively defined to support access to
    non-public repositories on GitHub or GitHub Enterprise.

**Example**
    List sessions.

    .. code-block:: bash

        nox -l

    Run default sessions.

    .. code-block:: bash

        nox

    Run specific sessions.

    .. code-block:: bash

        nox -s typing lint dependencies build tests docs

**License**
    `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
    © 2018 - 2026 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

**Author**
    Larry Turner, Schneider Electric, AI Hub, 2020-10-12.
"""

import glob
import json
import os
import pathlib
import random
import shutil
import string
import urllib.request

import nox
from nox import Session

nox.options.sessions = [
    "build",
    "format",
    "typing",
    "lint",
    "dependencies",
    "tests",
    "docs",
]

PYTHON_LIST = nox.project.python_versions(nox.project.load_toml("pyproject.toml"))
PYTHON = PYTHON_LIST[-1]
REPOSITORY = pathlib.Path.cwd().name
SOURCE = REPOSITORY.split("-")[0]
if not pathlib.Path(SOURCE).is_dir():
    SOURCE = "."


@nox.session(python=PYTHON)
def build(session: Session) -> None:
    """Build."""

    session.run("uv", "sync", "--active", "--locked", "--group=build", external=True)
    shutil.rmtree("dist", ignore_errors=True)
    session.run("python", "-m", "build", "-s", "-w")
    shutil.rmtree("build", ignore_errors=True)


@nox.session(venv_backend="none")
def clean(session: Session) -> None:
    """Clean."""

    for x in (
        "__pycache__",
        ".mypy_cache",
        ".nox",
        ".pytest_cache",
        ".ruff_cache",
        "build",
        "dist",
    ):
        shutil.rmtree(x, ignore_errors=True)
    for x in [x for x in glob.glob("**/", recursive=True) if ("__pycache__" in x)]:
        shutil.rmtree(x, ignore_errors=True)


@nox.session(python=PYTHON)
def dependencies(session: Session) -> None:
    """Dependencies."""

    session.run("uv", "sync", "--active", "--locked", "--group=dependencies", external=True)
    (pathlib.Path.cwd() / "docs").mkdir(exist_ok=True)
    path = pathlib.Path.cwd() / "docs" / "dependencies"
    with path.with_suffix(".dot").open("w") as fout:
        session.run(
            "pydeps",
            SOURCE,
            "--cluster",
            "--max-bacon",
            "0",
            "--no-config",
            "--no-output",
            "--show-dot",
            stdout=fout,
        )
        with path.with_suffix(".dot").open("r") as fin:
            with path.with_suffix(".svg").open("w") as fout:
                x = fin.read().strip()
                if "digraph" not in x:
                    raise ValueError(f"X = {x}")
                encode = lambda x: "".join(random.choices(string.ascii_letters, k=len(x)))
                code = dict([(u, encode(u)) for u in {v.split()[0] for v in x.splitlines() if ("[fillcolor" in v)}])
                for u, v in code.items():
                    x = x.replace(u, v)
                response = urllib.request.urlopen(
                    urllib.request.Request(
                        url="https://quickchart.io/graphviz",
                        data=str(json.dumps(dict(format="svg", graph=x))).encode("utf-8"),
                        headers={"Content-Type": "application/json"},
                    )
                )
                x = response.read().decode("utf-8")
                for u, v in code.items():
                    x = x.replace(v, u)
                fout.write(x)


@nox.session(python=PYTHON)
def docs(session: Session) -> None:
    """Documentation."""

    session.run("uv", "sync", "--active", "--locked", "--group=docs", external=True)
    if pathlib.Path("templates").is_dir():
        (pathlib.Path.cwd() / "docs").mkdir(exist_ok=True)
        session.run(
            "sphinx-apidoc",
            "--force",
            "--output",
            str(pathlib.Path.cwd() / "templates"),
            ".",
            "tests",
        )
        for x in glob.glob(str(pathlib.Path.cwd() / "templates" / "*.rst")):
            with pathlib.Path(x).open("r") as fin:
                y = fin.read().replace("   :members:", "   :members:\n   :noindex:")
            with pathlib.Path(x).open("w") as fout:
                fout.write(y)
        for x in glob.glob(str(pathlib.Path.cwd() / "templates" / "modules.rst")):
            with pathlib.Path(x).open("r") as fin:
                y = fin.read().replace("noxfile", "").replace("setup", "")
            with pathlib.Path(x).open("w") as fout:
                fout.write(y)
        for x in ("noxfile.rst", "setup.rst"):
            if (pathlib.Path.cwd() / "templates" / x).is_file():
                os.remove(str(pathlib.Path.cwd() / "templates" / x))
        session.run(
            "sphinx-build",
            str(pathlib.Path.cwd() / "templates"),
            str(pathlib.Path.cwd() / "docs"),
        )


@nox.session(python=PYTHON)
def format(session: Session):
    """Format."""

    session.run("uv", "sync", "--active", "--locked", "--group=format", external=True)
    session.run("ruff", "check", ".", "--select", "I", "--fix")
    session.run("ruff", "format", ".", "--check")


@nox.session(python=PYTHON)
def lint(session: Session) -> None:
    """Lint."""

    session.run("uv", "sync", "--active", "--locked", "--group=lint", external=True)
    session.run("ruff", "check", SOURCE)


@nox.session(venv_backend="none")
def lock(session: Session) -> None:
    """Lock."""

    session.run("uv", "lock", "--upgrade", external=True)


@nox.session(python=PYTHON)
def notebook(session: Session) -> None:
    """Notebook."""

    session.run("uv", "sync", "--active", "--locked", "--group=notebook", external=True)
    if pathlib.Path("notebooks").is_dir():
        os.chdir("notebooks")
        value = [x for x in glob.glob("*.ipynb", recursive=True)]
        if value:
            session.run("jupyter", "notebook", value[0])


@nox.session(venv_backend="none")
def tag(session: Session) -> None:
    """Tag."""

    if pathlib.Path(".git").is_dir():
        session.run("git", "tag", "--list", external=True)
        value = input("[" + REPOSITORY + "] annotate : ")
        if value:
            session.run(
                "git",
                "tag",
                "--annotate",
                value,
                "--force",
                "--message",
                ".",
                external=True,
            )
            session.run("git", "push", "--force", "--tags", external=True)


@nox.session(python=PYTHON_LIST)
def tests(session: Session) -> None:
    """Tests."""

    session.run("uv", "sync", "--active", "--locked", "--group=tests", external=True)
    if pathlib.Path("tests").is_dir():
        session.run(
            "coverage",
            "run",
            "--source=" + SOURCE,
            "-m",
            "pytest",
            "tests",
            "--verbose",
        )
        session.run("coverage", "report")


@nox.session(python=PYTHON)
def typing(session: Session) -> None:
    """Typing."""

    session.run("uv", "sync", "--active", "--locked", "--group=typing", external=True)
    session.run("mypy", SOURCE)
