from yaml_where.range import Position, Range


def test_proper_contained():
    containing = Range.from_parts(0, 0, 10, 10)
    contained = Range.from_parts(1, 1, 9, 9)
    assert contained <= containing
    assert not containing <= contained


def test_identical_ranges():
    containing = Range.from_parts(0, 0, 10, 10)
    contained = Range.from_parts(0, 0, 10, 10)
    assert contained <= containing
    assert containing <= contained


def test_self_comparison():
    containing = Range.from_parts(0, 0, 10, 10)
    contained = containing
    assert contained <= containing
    assert containing <= contained


def test_disjoint():
    preceding = Range.from_parts(0, 0, 10, 10)
    following = Range.from_parts(11, 0, 20, 10)
    assert not preceding <= following
    assert not following <= preceding


def test_overlap():
    preceding = Range.from_parts(0, 0, 10, 10)
    following = Range.from_parts(5, 5, 20, 20)
    assert not preceding <= following
    assert not following <= preceding


def test_contained_single_line():
    containing = Range.from_parts(0, 0, 0, 10)
    contained = Range.from_parts(0, 1, 0, 9)
    assert contained <= containing
    assert not containing <= contained


def test_identical_single_line():
    containing = Range.from_parts(0, 0, 0, 10)
    contained = Range.from_parts(0, 0, 0, 10)
    assert contained <= containing
    assert containing <= contained


def test_self_single_line():
    containing = Range.from_parts(0, 0, 0, 10)
    contained = containing
    assert contained <= containing
    assert containing <= contained

def test_disjoint_single_line():
    preceding = Range.from_parts(0, 0, 0, 10)
    following = Range.from_parts(0, 20, 0, 30)
    assert not preceding <= following
    assert not following <= preceding


def test_overlap_single_line():
    preceding = Range.from_parts(0, 0, 0, 10)
    following = Range.from_parts(0, 5, 0, 15)
    assert not preceding <= following
    assert not following <= preceding