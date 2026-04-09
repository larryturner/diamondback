"""**Description**
    *Serial* encodes and decodes an instance to a Base-85 encoded serialized
    string with elective gzip compression, and generates SHA3-256 hash codes.

    Decode decodes a Base-85 encoded serialized string to an instance.
    Elective compression is applied with gzip and automatically detected.

    Encode encodes an instance to a Base-85 encoded serialized string.
    Elective compression is applied with gzip.

    Code generates an SHA3-256 hash code of an encoded serialized string,
    with applications in security and version control.  Encode with
    compression embeds a datetime context, and code will not be consistent
    or deterministic.

    An instance may be an object or a collection, referenced by abstract or
    concrete types, and the instance will be completely encoded and decoded,
    without custom encoding definitions.

    Singleton.

    Thread safe.

**Example**

    .. code-block:: python

        from diamondback import Serial
        import pandas

        # Define a model instance of any supported type.

        x = pandas.DataFrame(dict(fruit = ["orange", "apple", "kiwi"], value = [1.25, 1.5, 0.30]))

        # Encode and decode a model instance with compression.

        y = Serial.encode(x)
        z = Serial.decode(y)

        # Encode and decode a model instance without compression.

        y = Serial.encode(x, compress=False)
        z = Serial.decode(y)

        # Generate an SHA3-256 code.

        code = Serial.code(y)

**License**
    `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
    © 2018 - 2026 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

**Author**
    Larry Turner, Schneider Electric, AI Hub, 2018-07-13.
"""

import base64
import gzip
import hashlib
import io
import pickle
from typing import Any


class Serial(object):
    """Serial."""

    @staticmethod
    def code(x: str, encoding: str = "utf-8") -> str:
        """Code generates an SHA3-256 hash code.

        Parameters
        ----------
        x: str
        encoding: str

        Returns
        -------
        y: str
        """

        if not x:
            raise ValueError(f"X = {x}")
        if not encoding:
            raise ValueError(f"Encoding = {encoding}")
        return hashlib.sha3_256(bytes(x, encoding)).hexdigest()

    @staticmethod
    def decode(x: str, encoding: str = "utf-8") -> Any:
        """Decodes a Base-85 encoded serialized string to an instance.  Elective
        compression is applied with gzip and automatically detected.

        Parameters
        ----------
        x: str
        encoding: str

        Returns
        -------
        y: Any
        """

        if not x:
            raise ValueError(f"X = {x}")
        if not encoding:
            raise ValueError(f"Encoding = {encoding}")
        u = base64.b85decode(bytes(x, encoding))
        try:
            with io.BytesIO(gzip.decompress(u)) as fio:
                y = pickle.load(fio)  # noqa
        except Exception:
            with io.BytesIO(u) as fio:
                y = pickle.load(fio)  # noqa
        return y

    @staticmethod
    def encode(x: Any, compress: bool = True, encoding: str = "utf-8") -> str:
        """Encodes an instance to a Base-85 encoded serialized string.  Elective
        compression is applied with gzip.

        Parameters
        ----------
        x: Any
        compress: bool
        encoding: str

        Returns
        -------
        y: str
        """

        if not encoding:
            raise ValueError(f"Encoding = {encoding}")
        with io.BytesIO() as fio:
            pickle.dump(x, fio)
            y = str(base64.b85encode(gzip.compress(fio.getvalue()) if compress else fio.getvalue()), encoding)
        return y
