from bytes import to_bytes


def test_to_bytes():
    dataset = {
        "some": b"some",
        1: 1,
    }
    for x, y in dataset.items():
        got = to_bytes(x)
        assert got == y, f"x {x} change to {got}, while {y} expected"
