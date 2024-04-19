import pytest
from rest_framework import serializers

from mung_manager.common.utils import inline_serializer, make_mock_object


@pytest.fixture
def mock_object():
    return make_mock_object(foo=1, bar="bar")


def test_inline_serializer_creates_a_serializer(mock_object):
    serializer = inline_serializer(
        fields={
            "foo": serializers.IntegerField(),
            "bar": serializers.CharField(),
        }
    )

    # Output
    result = serializer.to_representation(mock_object)
    expected = {"foo": 1, "bar": "bar"}

    assert expected == result

    # Input
    payload = {"foo": 1, "bar": "bar"}
    result = serializer.to_internal_value(payload)
    expected = {"foo": 1, "bar": "bar"}

    assert expected == result


def test_inline_serializer_passes_kwargs(mock_object):
    serializer = inline_serializer(
        many=True,
        fields={
            "foo": serializers.IntegerField(),
        },
    )

    objects = [mock_object]

    # Output
    result = serializer.to_representation(objects)
    expected = [{"foo": 1}]

    assert expected == result

    # Input
    payload = [{"foo": 1}]
    result = serializer.to_internal_value(payload)
    expected = [{"foo": 1}]

    assert expected == result
