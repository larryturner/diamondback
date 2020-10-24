""" **Description**

        Nox configuration.

    **Example**

        ::

            nox --list

            nox --sessions dist docs push status tests

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


@nox.session( venv_backend = 'none' )
def dist( session ) -> None :

    """ Build distributions.
    """

    shutil.rmtree( './build', ignore_errors = True )

    shutil.rmtree( './dist', ignore_errors = True )

    for x in glob.glob( './**/__pycache__', recursive = True ) :

        shutil.rmtree( x, ignore_errors = True )

    if ( os.path.exists( 'setup.py' ) ) :

        session.run( 'python', 'setup.py', 'sdist', 'bdist_wheel' )


@nox.session( venv_backend = 'none' )
def docs( session ) -> None :

    """ Build documents.
    """

    if ( os.path.exists( 'sphinx' ) ) :

        for x in [ x for x in glob.glob( './sphinx/*.rst' ) if ( x.split( os.path.sep )[ -1 ] != 'index.rst' ) ] :

            os.remove( x )

        session.run( 'sphinx-apidoc', '-f', '-o', './sphinx', '.' )

        shutil.rmtree( './docs', ignore_errors = True )

        if ( os.path.exists( 'images' ) ) :

            shutil.copytree( './images', './docs/images', dirs_exist_ok = True )

        session.run( 'sphinx-build', '-b', 'html', '-d', './docs/doctrees', './sphinx', './docs' )


@nox.session( venv_backend = 'none' )
def push( session ) -> None :

    """ Push repository.
    """

    if ( os.path.exists( '.git' ) ) :

        session.run( 'git', 'status', '--short' )

        value = input( '[ ' + os.getcwd( ).split( os.path.sep )[ -1 ] + ' ] message : ' )

        if ( value ) :

            if ( session.run( 'git', 'commit', '--all', '--message', value ) ) :

                session.run( 'git', 'push', 'origin', 'master' )

        url = 'https://github.schneider-electric.com/sesa14073/' + os.getcwd( ).split( os.path.sep )[ -1 ] + '.git'

        session.run( 'git', 'push', '--mirror', url )


@nox.session( venv_backend = 'none' )
def status( session ) -> None :

    """ Check status.
    """

    session.run( 'git', 'status', '--short' )


@nox.session( venv_backend = 'none' )
def tests( session ) -> None :

    """ Run tests.
    """

    if ( os.path.exists( 'tests' ) ) :

        session.run( 'pytest', '--verbose' )
