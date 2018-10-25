import pytest
from feeds.activity.notification import Notification
import uuid
from feeds.util import epoch_ms
from ..conftest import test_config
from ..util import assert_is_uuid
from feeds.exceptions import (
    MissingVerbError,
    MissingLevelError,
    InvalidExpirationError
)

    # def __init__(self, actor, verb, note_object, source, level='alert', target=None,
    #              context={}, expires=None, external_key=None):

cfg = test_config()

# some dummy "good" inputs for testing
actor = "test_actor"
verb_inf = "invite"
verb_id = 1
note_object = "foo"
source = "groups"
level_name = "warning"
level_id = 2
target = ["target_actor"]
context = {"some": "context"}
expires = epoch_ms() + (10 * 24 * 60 * 60 * 1000) # 10 days
external_key = "an_external_key"

def assert_note_ok(note, **kwargs):
    keys = [
        'actor', 'object', 'source', 'target', 'context', 'expires', 'external_key'
    ]
    for k in keys:
        if k in kwargs:
            assert getattr(note, k) == kwargs[k]
    if 'verb_id' in kwargs:
        assert note.verb.id == int(kwargs['verb_id'])
    if 'verb_inf' in kwargs:
        assert note.verb.infinitive == kwargs['verb_inf']
    if 'level_id' in kwargs:
        assert note.level.id == int(kwargs['level_id'])
    if 'level_name' in kwargs:
        assert note.level.name == kwargs['level_name']
    if 'expires' not in kwargs:
        assert note.expires == note.created + (int(cfg.get('feeds', 'lifespan')) * 24 * 60 * 60 * 1000)
    assert_is_uuid(note.id)

def test_note_new_ok_no_kwargs():
    note = Notification(actor, verb_inf, note_object, source)
    assert_note_ok(note, actor=actor, verb_inf=verb_inf, object=note_object, source=source)

def test_note_new_diff_levels():
    assert_args = {
        "actor": actor,
        "verb_inf": verb_inf,
        "object": note_object,
        "source": source
    }
    for name in ['alert', 'warning', 'request', 'error']:
        note = Notification(actor, verb_inf, note_object, source, level=name)
        test_args = assert_args.copy()
        test_args['level_name'] = name
        assert_note_ok(note, **test_args)
    for id_ in ['1', '2', '3', '4']:
        note = Notification(actor, verb_inf, note_object, source, level=id_)
        test_args = assert_args.copy()
        test_args['level_id'] = id_
        assert_note_ok(note, **test_args)


def test_note_new_target():
    note = Notification(actor, verb_inf, note_object, source, target=target)
    assert_note_ok(note, actor=actor, verb_inf=verb_inf,
                   object=note_object, source=source, target=target)


def test_note_new_context():
    note = Notification(actor, verb_inf, note_object, source, context=context)
    assert_note_ok(note, actor=actor, verb_inf=verb_inf,
                   object=note_object, source=source, context=context)


def test_note_new_expiration():
    note = Notification(actor, verb_inf, note_object, source, expires=expires)
    assert_note_ok(note, actor=actor, verb_inf=verb_inf,
                   object=note_object, source=source, expires=expires)


def test_note_new_external_key():
    note = Notification(actor, verb_inf, note_object, source, external_key=external_key)
    assert_note_ok(note, actor=actor, verb_inf=verb_inf,
                   object=note_object, source=source, external_key=external_key)


def test_note_new_bad_actor():
    # TODO: Should only fail on validate - shouldn't do a lookup whenever a new note is made.
    # also, shouldn't be None.
    with pytest.raises(AssertionError) as e:
        Notification(None, verb_inf, note_object, source)
    assert "actor must not be None" in str(e.value)


def test_note_new_bad_verb():
    with pytest.raises(AssertionError) as e:
        Notification(actor, None, note_object, source)
    assert "verb must not be None" in str(e.value)

    with pytest.raises(MissingVerbError) as e:
        Notification(actor, "foobar", note_object, source)
    assert 'Verb "foobar" not found' in str(e.value)


def test_note_new_bad_object():
    # TODO: Also test object validation itself later.
    with pytest.raises(AssertionError) as e:
        Notification(actor, verb_inf, None, source)
    assert 'note_object must not be None' in str(e.value)

def test_note_new_bad_source():
    # TODO: Validate sources as being real.
    with pytest.raises(AssertionError) as e:
        Notification(actor, verb_inf, note_object, None)
    assert 'source must not be None' in str(e.value)


def test_note_new_bad_level():
    with pytest.raises(AssertionError) as e:
        Notification(actor, verb_inf, note_object, source, level=None)
    assert "level must not be None" in str(e.value)

    with pytest.raises(MissingLevelError) as e:
        Notification(actor, verb_inf, note_object, source, level="foobar")
    assert 'Level "foobar" not found' in str(e.value)


def test_note_new_bad_target():
    bad_targets = [{}, "foo", 123, False]
    for bad in bad_targets:
        with pytest.raises(AssertionError) as e:
            Notification(actor, verb_inf, note_object, source, target=bad)
        assert "target must be either a list or None" in str(e.value)


def test_note_new_bad_context():
    bad_context = [[], "foo", 123, False]
    for bad in bad_context:
        with pytest.raises(AssertionError) as e:
            Notification(actor, verb_inf, note_object, source, context=bad)
        assert "context must be either a dict or None" in str(e.value)


def test_note_new_bad_expires():
    bad_expires = ["foo", {}, []]
    for bad in bad_expires:
        with pytest.raises(InvalidExpirationError) as e:
            Notification(actor, verb_inf, note_object, source, expires=bad)
        assert "Expiration time should be the number of milliseconds" in str(e.value)
    bad_expires = [123, True, False]
    for bad in bad_expires:
        with pytest.raises(InvalidExpirationError) as e:
            Notification(actor, verb_inf, note_object, source, expires=bad)
        assert "Notifications should expire sometime after they are created" in str(e.value)


def test_validate_ok():
    pass


def test_validate_bad():
    pass


def test_validate_expiration():
    pass


def test_default_lifespan():
    pass


def test_to_dict():
    pass


def test_user_view():
    pass


def test_from_dict():
    pass


def test_serialize():
    pass


def test_deserialize():
    pass
