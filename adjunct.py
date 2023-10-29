
from typing import Dict, Union


def get_annos(cls: type, annos: Dict[str, type]) -> Dict[str, type]:
    """
    Returns class annotations recursively in the order of inheritance.
    An equivalent non-recursive approach would use the reverse class' method resolution order (MRO).
    """
    for b in cls.__bases__:
        annos = get_annos(b, annos)
    if hasattr(cls, '__annotations__'):
        annos.update(cls.__annotations__)
    return annos


def fields(obj: Union[type, object]) -> Dict[str, type]:
    """
    Returns annotations of a class or class instance in the order of inheritance.
    """
    return get_annos(obj, {}) if isinstance(obj, type) else get_annos(obj.__class__, {})


def used_fields(obj: Union[type, object]) -> Dict[str, type]:
    """
    Returns annotations of a class or class instance that were initialized with some value.
    """
    return {k: obj._FIELDS[k] for k in obj._FIELDS if hasattr(obj, k)}


def unused_fields(obj: Union[type, object]) -> Dict[str, type]:
    """
    Returns "bare" annotations of a class or class instance,
    i.e. those that haven't been initialized with some value yet.
    """
    return {k: obj._FIELDS[k] for k in obj._FIELDS if not hasattr(obj, k)}


def __eq__(self, other):
    if type(self) is type(other):
        return True
    return NotImplemented


def _process_class(cls: type, eq: bool) -> type:
    setattr(cls, '_FIELDS', fields(cls))
    setattr(cls, 'used_fields', used_fields)
    setattr(cls, 'unused_fields', unused_fields)
    if eq:
        setattr(cls, '__eq__', __eq__)
    return cls


def adjunct(cls=None, /, *, eq=True):
    def wrap(cls):
        return _process_class(cls, eq)
    if cls is None:
        # we're called with parenthesis as @adjunct(...)
        return wrap
    # we're called without parenthesis as @adjunct
    return wrap(cls)
