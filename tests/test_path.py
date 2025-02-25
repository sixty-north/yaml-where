from yaml_where import path


def test_key_repr():
    assert repr(path.Key("key")) == "Key(value=key)"


def test_key_str():
    assert str(path.Key("key")) == "key/key"


def test_value_repr():
    assert repr(path.Value("value")) == "Value(value=value)"


def test_value_str():
    assert str(path.Value("value")) == "value/value"

def test_item_str():
    assert str(path.Item("value")) == "item/value"



def test_index_repr():
    assert repr(path.Index(0)) == "Index(value=0)"


def test_index_str():
    assert str(path.Index(0)) == "index/0"
