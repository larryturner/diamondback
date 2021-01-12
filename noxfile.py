""" **Description**

        Nox project management.

    **Example**

        ::

            nox --list

            nox --sessions build clean dist docs push status tests

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-12.

    **Definition**

"""

import glob
import nox
import os
import shutil
import typing


@nox.session( venv_backend = 'none' )
def build( session ) -> None :

    """ Build Docker image.
    """

    if ( os.path.exists( 'dockerfile' ) ) :

        session.run( 'docker', 'build', '--tag', os.getcwd( ).split( os.path.sep )[ -1 ] + ':latest', '.' )


@nox.session( venv_backend = 'none' )
def clean( session ) -> None :

    """ Clean repository.
    """

    remove( './build' )

    remove( './**/__pycache__' )

    remove( './**/.pytest_cache' )


@nox.session( venv_backend = 'none' )
def dist( session ) -> None :

    """ Build distributions.
    """

    remove( './dist/*' )

    if ( os.path.exists( 'setup.py' ) ) :

        session.run( 'python', 'setup.py', 'sdist', 'bdist_wheel' )

    clean( session )


@nox.session( venv_backend = 'none' )
def docs( session ) -> None :

    """ Build documents.
    """

    if ( os.path.exists( 'sphinx' ) ) :

        remove( [ x for x in glob.glob( './sphinx/*.rst' ) if ( x.split( os.path.sep )[ -1 ] != 'index.rst' ) ] )

        session.run( 'sphinx-apidoc', '--force', '--output', './sphinx', '.' )

        remove( './docs/*' )

        if ( os.path.exists( 'images' ) ) :

            shutil.copytree( './images', './docs/images', dirs_exist_ok = True )

        session.run( 'sphinx-build', './sphinx', './docs' )


@nox.session( venv_backend = 'none' )
def push( session ) -> None :

    """ Push repository.
    """

    if ( os.path.exists( '.git' ) ) :

        session.run( 'git', 'status', '--short' )

        value = input( '[ ' + os.getcwd( ).split( os.path.sep )[ -1 ] + ' ] message : ' )

        if ( value ) :

            try :

                if ( session.run( 'git', 'commit', '--all', '--message', value ) ) :

                    session.run( 'git', 'push', 'origin', 'master' )

            except :

                pass

        url = 'https://github.schneider-electric.com/sesa14073/' + os.getcwd( ).split( os.path.sep )[ -1 ] + '.git'

        session.run( 'git', 'push', '--mirror', url )


@nox.session( venv_backend = 'none' )
def status( session ) -> None :

    """ Check status.
    """

    if ( os.path.exists( '.git' ) ) :

        session.run( 'git', 'status', '--short' )


@nox.session( venv_backend = 'none' )
def tests( session ) -> None :

    """ Run tests.
    """

    if ( os.path.exists( 'tests' ) ) :

        if ( os.listdir( 'tests' ) ) :

            session.run( 'pytest', '--capture=no', '--verbose' )


# Private.

def remove( path : typing.Union[ str, typing.List[ str ] ] ) -> None :

    """ Remove path, expand for wildcards.

        Arguments :

            path - Path ( str, list( str ) ).
    """

    if ( path ) :

        v = [ ]

        if ( isinstance( path, str ) ) :

            if ( path.find( '*' ) >= 0 ) :

                v = glob.glob( path, recursive = True )

            else :

                v = [ path ]

        elif ( not isinstance( v, list ) ) :

            raise ValueError( 'Path = ' + str( path ) )

        for x in v :

            try :

                if ( os.path.isdir( x ) ) :

                    shutil.rmtree( x, ignore_errors = True )

                else :

                    os.remove( x )

            except :

                pass
