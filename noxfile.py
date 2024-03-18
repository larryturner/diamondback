""" **Description**
        Nox project management.

    **Environment**
        Environment variables may be electively defined to support access to
        non-public repositories on GitHub or GitHub Enterprise.

        ``GITHUB_USER`` and ``GITHUB_TOKEN`` token define a GitHub user and token.

        pyproject.toml dependencies may include GitHub repositories, which
        are temporarily modified to embed GitHub credentials in build, as
        environment variable expressions are not directly supported.

        .. code-block:: bash

            '<package> @ git+https://[<GITHUB_USER>:<GITHUB_TOKEN>@]github.[<enterprise>.]com/<account>/<repository>@<tag>#egg=<package>'

    **Example**

        .. code-block:: bash

            nox -l
            nox -s build clean dependencies docs image notebook push status tag tests typing

    **License**
        © 2018 - 2024 Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2020-10-12.
"""

import glob
import nox
import os
import pathlib
import random
import requests
import shutil
import string
import time

nox.options.sessions = [ 'typing', 'dependencies', 'build', 'image', 'tests', 'docs' ]

REPOSITORY = pathlib.Path.cwd( ).name
x = REPOSITORY.split( '-' )
SOURCE = 'service' if ( pathlib.Path( 'service' ).is_dir( ) ) else x[ max( len( x ) - 2, 0 ) ]
if ( not pathlib.Path( SOURCE ).is_dir( ) ) :
    SOURCE = '.'

@nox.session( venv_backend = 'none' )
def build( session ) -> None :

    """ Build distribution.
    """

    if ( pathlib.Path( 'setup.py' ).is_file( ) ) :
        shutil.rmtree( 'dist', ignore_errors = True )
        x = None
        try :
            if ( pathlib.Path( 'pyproject.toml' ).is_file( ) ) :
                user, token = os.getenv( 'GITHUB_USER' ), os.getenv( 'GITHUB_TOKEN' )
                if ( user and token ) :
                    with open( 'pyproject.toml', 'r' ) as fin :
                        x = fin.read( )
                    u, v = 'git+https://github.', f'git+https://{user}:{token}@github.'
                    y = x.replace( u, v )
                    if ( x != y ) :
                        print( 'pyproject.toml : GitHub credentials found.' )
                        with open( 'pyproject.toml', 'w' ) as fout :
                            fout.write( y )
            session.run( 'python', '-m', 'build', '-s', '-w' )
        finally :
            if ( x ) :
                with open( 'pyproject.toml', 'w' ) as fout :
                    fout.write( x )
            shutil.rmtree( 'build', ignore_errors = True )

@nox.session( venv_backend = 'none' )
def clean( session ) -> None :

    """ Clean repository.
    """

    for x in ( '.mypy_cache', '.nox', '.pytest_cache', 'build', 'dist', 'docs' ) :
        shutil.rmtree( x, ignore_errors = True )
    for x in [ x for x in glob.glob( f'**{str( pathlib.Path( "/" ) )}', recursive = True ) if ( '__pycache__' in x ) ] :
        shutil.rmtree( x, ignore_errors = True )

def convert( x : str ) -> str :

    """Convert dot to svg format.

    Arguments :
        x : str - dot.

    Returns :
        y : str - svg.
    """

    if ( not x ) :
        raise ValueError( f'X = {x}' )
    x = x.strip( )
    if ( 'digraph' not in x ) :
        raise ValueError( f'X = {x}' )
    encode = lambda x : ''.join( random.choices( string.ascii_letters, k = len( x ) ) )
    code = dict( [ ( u, encode( u ) ) for u in {v.split( )[ 0 ] for v in x.splitlines( ) if ( '[fillcolor' in v )} ] )
    for u, v in code.items( ) :
        x = x.replace( u, v )
    y = requests.post( 'https://quickchart.io/graphviz', json = dict( format = 'svg', graph = x ) ).text
    for u, v in code.items( ) :
        y = y.replace( v, u )
    return y

@nox.session( venv_backend = 'none' )
def dependencies( session ) -> None :

    """ Dependency diagrams.
    """

    ( pathlib.Path.cwd( ) / 'docs' ).mkdir( exist_ok = True )
    path = str( pathlib.Path.cwd( ) / 'docs' / 'dependencies-partial' )
    with open( path + '.dot', 'w' ) as fout :
        session.run( 'pydeps', SOURCE, '--cluster', '--no-config', '--no-output', '--show-dot', stdout = fout )
        with open( path + '.dot', 'r' ) as fin :
            with open( path + '.svg', 'w' ) as fout :
                fout.write( convert( fin.read( ) ) )
    path = str( pathlib.Path.cwd( ) / 'docs' / 'dependencies-full' )
    with open( path + '.dot', 'w' ) as fout :
        session.run( 'pydeps', SOURCE, '--cluster', '--max-bacon', '0', '--no-config', '--no-output', '--show-dot', stdout = fout )
        with open( path + '.dot', 'r' ) as fin :
            with open( path + '.svg', 'w' ) as fout :
                fout.write( convert( fin.read( ) ) )

@nox.session( venv_backend = 'none' )
def docs( session ) -> None :

    """ Documentation.
    """

    if ( pathlib.Path( 'templates' ).is_dir( ) ) :
        ( pathlib.Path.cwd( ) / 'docs' ).mkdir( exist_ok = True )
        session.run( 'sphinx-apidoc', '--force', '--output', str( pathlib.Path.cwd( ) / 'templates' ), '.', 'tests' )
        for x in glob.glob( str( pathlib.Path.cwd( ) / 'templates' / '*.rst' ) ) :
            with open( x, 'r' ) as fin :
                y = fin.read( ).replace( '   :members:', '   :members:\n   :noindex:' )
            with open( x, 'w' ) as fout :
                fout.write( y )
        for x in glob.glob( str( pathlib.Path.cwd( ) / 'templates' / 'modules.rst' ) ) :
            with open( x, 'r' ) as fin :
                y = fin.read( ).replace( 'noxfile', '' ).replace( 'setup', '' )
            with open( x, 'w' ) as fout :
                fout.write( y )
        for x in ( 'noxfile.rst', 'setup.rst' ) :
            if ( ( pathlib.Path.cwd( ) / 'templates' / x ).is_file( ) ) :
                os.remove( str( pathlib.Path.cwd( ) / 'templates' / x ) )
        session.run( 'sphinx-build', str( pathlib.Path.cwd( ) / 'templates' ), str( pathlib.Path.cwd( ) / 'docs' ) )
        session.run( 'git', 'add', str( pathlib.Path.cwd( ) / 'docs' / '*' ), external = True )
        session.run( 'git', 'add', str( pathlib.Path.cwd( ) / 'templates' / '*' ), external = True )

@nox.session( venv_backend = 'none' )
def image( session ) -> None :

    """ Image.
    """

    if ( pathlib.Path( 'dockerfile' ).is_file( ) ) :
        build( session )
        session.run( 'docker', 'build', '--tag', REPOSITORY, '.', external = True )

@nox.session( venv_backend = 'none' )
def notebook( session ) -> None :

    """ Notebook.
    """

    if ( pathlib.Path( 'notebooks' ).is_dir( ) ) :
        os.chdir( 'notebooks' )
        value = [ x for x in glob.glob( '*.ipynb', recursive = True ) ]
        if ( value ) :
            session.run( 'jupyter', 'notebook', value[ 0 ] )

@nox.session( venv_backend = 'none' )
def push( session ) -> None :

    """ Push.
    """

    if ( pathlib.Path( '.git' ).is_dir( ) ) :
        x = REPOSITORY.split( '-' )
        package = x[ max( len( x ) - 2, 0 ) ]
        if ( pathlib.Path( package ).is_dir( ) ) :
            session.run( 'git', 'add', str( pathlib.Path.cwd( ) / package / '*' ), external = True )
        if ( pathlib.Path( 'service' ).is_dir( ) ) :
            session.run( 'git', 'add', str( pathlib.Path.cwd( ) / 'service' / '*' ), external = True )
        if ( pathlib.Path( 'tests' ).is_dir( ) ) :
            session.run( 'git', 'add', str( pathlib.Path.cwd( ) / 'tests' / '*' ), external = True )
        status( session )
        value = input( '[ ' + REPOSITORY + ' ] message : ' )
        if ( value ) :
            if ( session.run( 'git', 'commit', '--all', '--message', value, external = True ) ) :
                session.run( 'git', 'push', external = True )

@nox.session( venv_backend = 'none' )
def status( session ) -> None :

    """ Status.
    """

    if ( pathlib.Path( '.git' ).is_dir( ) ) :
        print( '[ ' + REPOSITORY + ' ]' )
        session.run( 'git', 'status', '--short', external = True )

@nox.session( venv_backend = 'none' )
def tag( session ) -> None :

    """ Tag.
    """

    if ( pathlib.Path( '.git' ).is_dir( ) ) :
        session.run( 'git', 'tag', '--list', external = True )
        value = input( '[ ' + REPOSITORY + ' ] annotate : ' )
        if ( value ) :
            session.run( 'git', 'tag', '--annotate', value, '--force', '--message', '.', external = True )
            session.run( 'git', 'push', '--force', '--tags', external = True )

@nox.session( venv_backend = 'none' )
def tests( session ) -> None :

    """ Tests.
    """

    if ( pathlib.Path( 'tests' ).is_dir( ) ) :
        if ( [ u for u in pathlib.Path( 'tests' ).iterdir( ) ] ) :
            try :
                if ( pathlib.Path( 'docker-compose.yml' ).is_file( ) ) :
                    session.run( 'docker', 'compose', 'up', '--detach', external = True )
                    time.sleep( 10.0 )
                session.run( 'python', '-m', 'pip', 'install', '-e', '.' )
                session.run( 'pytest', '--capture=no', '--verbose', '-s' )
                shutil.rmtree( '.pytest_cache', ignore_errors = True )
            finally :
                if ( pathlib.Path( 'docker-compose.yml' ).is_file( ) ) :
                    session.run( 'docker', 'compose', 'down', external = True )

@nox.session( venv_backend = 'none' )
def typing( session ) -> None :

    """ Typing.
    """

    session.run( 'mypy', SOURCE )
