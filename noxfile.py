""" **Description**

        Nox project management.

    **Example**

        ::

            nox --list

            nox --sessions clean dist docs image notebook push status tag tests

    **License**

        © 2020 - 2021 Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-12.

    **Definition**

"""

import glob
import nox
import os
import requests
import shutil
import time

repository = os.getcwd( ).split( os.path.sep )[ -1 ]

@nox.session( venv_backend = 'none' )
def clean( session ) -> None :

    """ Clean repository.
    """

    for x in ( '.mypy_cache', '.nox', '.pytest_cache', 'build', 'dist', 'docs' ) :

        shutil.rmtree( x, ignore_errors = True )

    for x in [ x for x in glob.glob( '**/', recursive = True ) if ( '__pycache__' in x ) ] :

        shutil.rmtree( x, ignore_errors = True )

@nox.session( venv_backend = 'none' )
def dist( session ) -> None :

    """ Build distribution.
    """

    if ( os.path.exists( 'setup.py' ) ) :

        shutil.rmtree( 'dist', ignore_errors = True )

        session.run( 'python', 'setup.py', 'sdist', 'bdist_wheel', 'build' )

        session.run( 'git', 'add', './dist/*' )

@nox.session( venv_backend = 'none' )
def docs( session ) -> None :

    """ Build documentation.
    """

    if ( os.path.exists( 'sphinx' ) ) :

        shutil.rmtree( 'docs', ignore_errors = True )

        os.makedirs( 'docs' )

        session.run( 'sphinx-apidoc', '--force', '--output', './sphinx', '.', 'tests' )

        session.run( 'sphinx-build', './sphinx', './docs' )

        session.run( 'git', 'add', './docs/*' )

        session.run( 'git', 'add', './sphinx/*' )

@nox.session( venv_backend = 'none' )
def image( session ) -> None :

    """ Build image.
    """

    if ( os.path.exists( 'dockerfile' ) ) :

        dist( session )

        try :

            session.run( 'az', 'acr', 'login', '--name', 'ecaregistry' )

        except Exception :

            pass

        session.run( 'docker', 'build', '--tag', repository, '--build-arg', 'FEED_LOGIN', '--build-arg', 'FEED_PASSWORD', '.' )

@nox.session( venv_backend = 'none' )
def notebook( session ) -> None :

    """ Run jupyter notebook.
    """

    if ( os.path.exists( 'jupyter' ) ) :

        os.chdir( 'jupyter' )

        value = [ x for x in glob.glob( '*.ipynb', recursive = True ) ]

        if ( value ) :

            session.run( 'jupyter', 'notebook', value[ 0 ] )

@nox.session( venv_backend = 'none' )
def push( session ) -> None :

    """ Push repository.
    """

    if ( os.path.exists( '.git' ) ) :

        package = repository.split( '-' )

        package = package[ max( len( package ) - 2, 0 ) ]

        if ( os.path.exists( './' + package ) ) :

            session.run( 'git', 'add', './' + package + '/*' )

        if ( os.path.exists( './service' ) ) :

            session.run( 'git', 'add', './service/*' )

        if ( os.path.exists( './tests' ) ) :

            session.run( 'git', 'add', './tests/*' )

        status( session )

        value = input( '[ ' + repository + ' ] message : ' )

        if ( value ) :

            try :

                if ( session.run( 'git', 'commit', '--all', '--message', value ) ) :

                    session.run( 'git', 'push', 'origin', 'master' )

            except Exception :

                pass

        try :

            url = 'https://github.schneider-electric.com'

            requests.request( method = 'head', url = url, timeout = 2 )

            value = input( '[ ' + repository + ' ] account : ' )

            if ( value ) :

                session.run( 'git', 'push', '--mirror', url + '/' + value + '/' + repository + '.git' )                

        except Exception :

            pass

@nox.session( venv_backend = 'none' )
def status( session ) -> None :

    """ Check status.
    """

    if ( os.path.exists( '.git' ) ) :

        print( '[ ' + repository + ' ]' )

        session.run( 'git', 'status', '--short' )

@nox.session( venv_backend = 'none' )
def tag( session ) -> None :

    """ Push tag.
    """

    if ( os.path.exists( '.git' ) ) :

        session.run( 'git', 'tag', '--list' )

        value = input( '[ ' + repository + ' ] annotate : ' )

        if ( value ) :

            session.run( 'git', 'tag', '--annotate', value, '--force', '--message', '.' )

            try :

                session.run( 'git', 'push', '--force', '--tags' )

            except Exception :

                pass

@nox.session( venv_backend = 'none' )
def tests( session ) -> None :

    """ Run tests.
    """

    if ( os.path.exists( 'tests' ) ) :

        if ( os.listdir( 'tests' ) ) :

            if ( os.path.exists( 'docker-compose.yml' ) ) :

                try :

                    session.run( 'az', 'acr', 'login', '--name', 'ecaregistry' )

                except Exception :

                    pass

                try :

                    session.run( 'docker', 'compose', 'up', '--detach' )

                    time.sleep( 10.0 )

                except Exception :

                    pass

            try :

                session.run( 'pytest', '--capture=no', '--verbose' )

                shutil.rmtree( '.pytest_cache', ignore_errors = True )

            except Exception :

                pass

            if ( os.path.exists( 'docker-compose.yml' ) ) :

                try :

                    session.run( 'docker', 'compose', 'down' )

                except Exception :

                    pass
