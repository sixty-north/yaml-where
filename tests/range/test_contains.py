from yaml_where.range import Range


def test_proper_contained():
    containing = Range.from_parts(0, 0, 10, 10)
    contained = Range.from_parts(1, 1, 9, 9)
    assert contained <= containing


def test_identical_ranges():
    containing = Range.from_parts(0, 0, 10, 10)
    contained = Range.from_parts(0, 0, 10, 10)
    assert contained <= containing


def test_self_comparison():
    containing = Range.from_parts(0, 0, 10, 10)
    contained = containing
    assert contained <= containing


def test_preceding():
    preceding = Range.from_parts(0, 0, 10, 10)
    following = Range.from_parts(11, 0, 20, 10)
    assert not preceding <= following


def test_following():
    preceding = Range.from_parts(0, 0, 10, 10)
    following = Range.from_parts(11, 0, 20, 10)
    assert not following <= preceding


def test_overlap_front():
    preceding = Range.from_parts(0, 0, 10, 10)
    following = Range.from_parts(5, 5, 20, 20)
    assert not preceding <= following


def test_overlap_tail():
    preceding = Range.from_parts(0, 0, 10, 10)
    following = Range.from_parts(5, 5, 20, 20)
    assert not following <= preceding


def test_full_overlap():
    containing = Range.from_parts(0, 0, 10, 10)
    contained = Range.from_parts(1, 1, 9, 9)
    assert not containing <= contained

