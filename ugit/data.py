import hashlib
import os

from collections import namedtuple

GIT_DIR = '.ugit'

def init():
    os.makedirs(GIT_DIR)
    os.makedirs(f'{GIT_DIR}/objects')


RefValue = namedtuple('RefValue', ['symbolyc', 'value'])


def update_ref(ref, value, deref = True):
    assert not value.symbolyc
    ref = _get_ref_internal(ref, deref)[0]
    ref_path = f'{GIT_DIR}/{ref}'
    os.makedirs(os.path.dirname(ref_path), exist_ok = True)
    with open(ref_path, 'w') as f:
        f.write(value.value)


def get_ref(ref, deref = True):
    return _get_ref_internal(ref, deref)


def _get_ref_internal(ref, deref):
    ref_path = f'{GIT_DIR}/{ref}'
    value = None
    if os.path.isfile(ref_path):
        with open(ref_path) as f:
            value = f.read().strip()
    
    symbolic = bool (value) and value.startswith('ref:')
    if symbolic:
        value = value.split(':', 1)[1].strip()

        if deref:
            return _get_ref_internal(value, deref = True)

    return ref, RefValue(symbolyc = symbolic, value = value)


def iter_refs(deref = True):
    refs = ['HEAD']
    for root, _, filenames in os.walk(f'{GIT_DIR}/refs/'):
        root = os.path.realpath(root)
        refs.extend(f'{root}/{name}' for name in filenames)

    for refname in refs:
        yield refname, get_ref(refname, deref = deref)


def hash_object(data, type_='blob'):
    obj = type_.encode() + b'\x00' + data
    oid = hashlib.sha1(obj).hexdigest()
    with open(f'{GIT_DIR}/objects/{oid}', 'wb') as out:
        out.write(obj)
    return oid


def get_object(oid, expected='blob'):
    with open(f'{GIT_DIR}/objects/{oid}', 'rb') as f:
        obj = f.read()

    type_, _, content = obj.partition(b'\x00')
    type_ = type_.decode()

    if expected is not None:
        assert type_ == expected, f'Expected {expected}, got {type_}'

    return content;
    
