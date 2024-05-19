"""Test daprgen."""

import daprgen


def test_import() -> None:
    """Test that the app can be imported."""
    assert isinstance(daprgen.__name__, str)
