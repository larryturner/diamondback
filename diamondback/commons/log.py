"""**Description**
    A log instance formats and writes log entries with a specified level
    and stream using loguru. Log entries contain an ISO 8601 datetime
    and level.  Dynamic stream redirection and level specification
    are supported.

    Log uses lazy initialization to coexist with loguru, and removes or
    creates loguru handlers only on explicit stream assignment or write.
    In lazy initialization an existing default loguru handler, with an
    identity equal to 0, and a stream assignment of sys.stdout is removed,
    and a new loguru handler with a stream assignment of sys.stdout and a
    level of "Info" is created.

    In stream assignments subsequent to initialization, only loguru
    handlers previously created by Log will be removed, as the Log design
    pattern does not define multicast.  The ability to create and modify
    externally defined loguru handlers, multicast, and utilize any native
    loguru functionality is supported.

    Levels defined by loguru are supported, including custom definitions,
    which may have an associated numerical value greater than or equal to
    zero.  Levels may be dynamically modified without creating, deleting,
    or modifying a loguru handler.  Levels are case insensitive on
    assignment, though loguru uses upper case.

    Singleton.

    Thread safe.

**Example**

    .. code-block:: python

        from diamondback import Log
        import io
        import numpy
        import sys

        try :
            # Set Log level to "Info", the default level.

            Log.level("Info")
            Log.write("Info", "Test Log write.")

            # Standard output.

            Log.stream(sys.stdout)
            Log.write("Info", f"Valid = {True}")

            # Memory stream.

            stream = io.StringIO()
            Log.stream(stream)
            x = numpy.random.rand(2, 2)
            Log.write("Info", f"X = {x}")

            # Read and reset memory stream.
            value = stream.getvalue()
            _, _ = stream.truncate(0), stream.seek(0)

            # File.

            with open("log-2112.txt", "w") as fout:
                Log.stream(fout)
                x = numpy.random.rand(2, 2)
                Log.write("Warning", f"X = {x}")
        except Exception as ex :
            Log.write("Error", ex)

**License**
    `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_
    © 2018 - 2025 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

**Author**
    Larry Turner, Schneider Electric, AI Hub, 2018-03-22.
"""

from loguru import logger
from threading import RLock
from typing import Any
import numpy
import os
import sys


class Log(object):
    """Log."""

    numpy.set_printoptions(formatter=dict(float="{:.6f}".format))

    LEVEL: tuple[str, ...] = ("Critical", "Error", "Warning", "Success", "Info", "Debug", "Trace")

    _identity = 0
    _level = logger.level("Info".upper())
    _rlock = RLock()

    @classmethod
    def level(cls, level: str) -> None:
        """Level.

        Arguments:
            level: str - in LEVEL.
        """

        with Log._rlock:
            try:
                Log._level = logger.level(level.upper())
            except Exception:
                raise ValueError(f"Level = {level} Expected Level in {Log.LEVEL}")

    @classmethod
    def stream(cls, stream: Any) -> None:
        """Stream.

        Arguments:
            stream: Any, hasattr("write") - in (sys.stderr, sys.stdout, open(< path >, "w" or "a")).
        """

        with Log._rlock:
            if (not stream) or (not hasattr(stream, "write")):
                raise ValueError(f"Stream = {stream} Expected Write")
            try:
                logger.remove(Log._identity)
            except ValueError:
                pass
            Log._identity = logger.add(
                stream,
                level=0,
                format="<blue>{time:YYYY-MM-DDTHH:mm:ss.SSZ}</blue> <level>{level}</level> {message}",
            )

    @classmethod
    def write(cls, level: str, entry: str | Exception) -> None:
        """Formats and writes log entries using loguru with a specified level
        and stream.  Log entries contain an ISO 8601 datetime and level.

        Arguments:
            level: str - in LEVEL.
            entry: str | Exception.
        """

        with Log._rlock:
            if not Log._identity:
                Log.stream(sys.stdout)
            try:
                v = logger.level(level.upper())
            except Exception:
                raise ValueError(f"Level = {level} Expected Level in {Log.LEVEL}")
            if v.no >= Log._level.no:
                if isinstance(entry, Exception):
                    entry = f"Exception = {type(entry).__name__} {entry}"
                    info = sys.exc_info()[-1]
                    while info:
                        entry += (
                            f" @ File = {info.tb_frame.f_code.co_filename.split(os.sep)[-1]} Line = {info.tb_lineno}"
                        )
                        info = info.tb_next
                logger.log(v.name, entry)
