""" **Description**
        Nox project management.

    **Example**
        
        ::
        
            nox --list
            nox --sessions build clean docs image notebook push status tag tests typing
    
    **License**
        © 2019 - 2023 Schneider Electric Industries SAS. All rights reserved.
    
    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2020-10-12.
"""

import glob
import nox
import os
import pathlib
import requests
import shutil
import time

nox.options.sessions = [ 'build', 'image', 'docs', 'tests' ]

repository = pathlib.Path.cwd( ).name
x = repository.split( '-' )
source = 'service' if ( pathlib.Path( 'service' ).is_dir( ) ) else x[ max( len( x ) - 2, 0 ) ]

@nox.session( venv_backend = 'none' )
def build( session ) -> None :

    """ Build distribution.
    """

    if ( pathlib.Path( 'setup.py' ).is_file( ) ) :
        shutil.rmtree( 'dist', ignore_errors = True )
        session.run( 'python', '-m', 'build', '-s', '-w' )
        shutil.rmtree( 'build', ignore_errors = True )
        session.run( 'git', 'add', str( pathlib.Path.cwd( ) / 'dist' / '*' ) )

@nox.session( venv_backend = 'none' )
def clean( session ) -> None :

    """ Clean repository.
    """

    for x in ( '.mypy_cache', '.nox', '.pytest_cache', 'build', 'dist', 'docs' ) :
        shutil.rmtree( x, ignore_errors = True )
    for x in [ x for x in glob.glob( f'**{str( pathlib.Path( "/" ) )}', recursive = True ) if ( '__pycache__' in x ) ] :
        shutil.rmtree( x, ignore_errors = True )

@nox.session( venv_backend = 'none' )
def docs( session ) -> None :

    """ Build documentation.
    """

    if ( pathlib.Path( 'templates' ).is_dir( ) ) :
        shutil.rmtree( 'docs', ignore_errors = True )
        ( pathlib.Path.cwd( ) / 'docs' ).mkdir( )
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
        session.run( 'git', 'add', str( pathlib.Path.cwd( ) / 'docs' / '*' ) )
        session.run( 'git', 'add', str( pathlib.Path.cwd( ) / 'templates' / '*' ) )

@nox.session( venv_backend = 'none' )
def image( session ) -> None :

    """ Build image.
    """

    if ( pathlib.Path( 'dockerfile' ).is_file( ) ) :
        build( session )
        session.run( 'docker', 'build', '--tag', repository, '.' )

@nox.session( venv_backend = 'none' )
def notebook( session ) -> None :

    """ Run notebook.
    """

    if ( pathlib.Path( 'notebooks' ).is_dir( ) ) :
        os.chdir( 'notebooks' )
        value = [ x for x in glob.glob( '*.ipynb', recursive = True ) ]
        if ( value ) :
            session.run( 'jupyter', 'notebook', value[ 0 ] )

@nox.session( venv_backend = 'none' )
def push( session ) -> None :

    """ Push repository.
    """

    if ( pathlib.Path( '.git' ).is_dir( ) ) :
        package = repository.split( '-' )
        package = package[ max( len( package ) - 2, 0 ) ]
        if ( pathlib.Path( package ).is_dir( ) ) :
            session.run( 'git', 'add', str( pathlib.Path.cwd( ) / package / '*' ) )
        if ( pathlib.Path( 'service' ).is_dir( ) ) :
            session.run( 'git', 'add', str( pathlib.Path.cwd( ) / 'service' / '*' ) )
        if ( pathlib.Path( 'tests' ).is_dir( ) ) :
            session.run( 'git', 'add', str( pathlib.Path.cwd( ) / 'tests' / '*' ) )
        status( session )
        value = input( '[ ' + repository + ' ] message : ' )
        if ( value ) :
            if ( session.run( 'git', 'commit', '--all', '--message', value ) ) :
                session.run( 'git', 'push', 'origin', 'master' )
        try :
            url = 'https://github.schneider-electric.com'
            requests.request( method = 'head', url = url, timeout = 2 )
            value = input( '[ ' + repository + ' ] mirror : ' )
            if ( value ) :
                session.run( 'git', 'push', '--mirror', url + '/' + value + '/' + repository + '.git' )                
        except Exception :
            pass

@nox.session( venv_backend = 'none' )
def status( session ) -> None :

    """ Check status.
    """

    if ( pathlib.Path( '.git' ).is_dir( ) ) :
        print( '[ ' + repository + ' ]' )
        session.run( 'git', 'status', '--short' )

@nox.session( venv_backend = 'none' )
def tag( session ) -> None :

    """ Push tag.
    """

    if ( pathlib.Path( '.git' ).is_dir( ) ) :
        session.run( 'git', 'tag', '--list' )
        value = input( '[ ' + repository + ' ] annotate : ' )
        if ( value ) :
            session.run( 'git', 'tag', '--annotate', value, '--force', '--message', '.' )
            session.run( 'git', 'push', '--force', '--tags' )

@nox.session( venv_backend = 'none' )
def tests( session ) -> None :

    """ Run tests.
    """

    if ( pathlib.Path( 'tests' ).is_dir( ) ) :
        if ( [ u for u in pathlib.Path( 'tests' ).iterdir( ) ] ) :
            try :
                if ( pathlib.Path( 'docker-compose.yml' ).is_file( ) ) :
                    session.run( 'docker', 'compose', 'up', '--detach' )
                    time.sleep( 10.0 )
                session.run( 'python', '-m', 'pip', 'install', '-e', '.' )
                session.run( 'pytest', '--capture=no', '--verbose', '-s' )
                shutil.rmtree( '.pytest_cache', ignore_errors = True )
            finally :
                if ( pathlib.Path( 'docker-compose.yml' ).is_file( ) ) :
                    session.run( 'docker', 'compose', 'down' )

@nox.session( venv_backend = 'none' )
def typing( session ) -> None :

    """ Run typing.
    """

    session.run( 'mypy', source )
