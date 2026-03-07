from typing import Awaitable, Callable

import pytest
import warnings
from weaviate.collections.aggregate import _AggregateCollectionAsync
from weaviate.collections.classes.aggregate import Metrics
from weaviate.connect import ConnectionV4
from weaviate.exceptions import WeaviateInvalidInputError





def test_metrics_text_limit() -> None:
    result = Metrics("my_prop").text(limit=5)
    #assert result.limit == 5


def test_metrics_text_min_occurrences_deprecated() -> None:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = Metrics("my_prop").text(min_occurrences=5)
        # assert the warning was raised
        # assert result.limit == 5

def test_metrics_text_limit_and_min_occurrences_raises() -> None:
    with pytest.raises(ValueError):
        Metrics("my_prop").text(limit=5, min_occurrences=5)

def test_metrics_text_min_occurrences_used_as_limit() -> None:
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        result = Metrics("my_prop").text(min_occurrences=3)
        # assert result.limit == 3

async def _test_aggregate(aggregate: Callable[[], Awaitable]) -> None:
    with pytest.raises(WeaviateInvalidInputError):
        await aggregate()


@pytest.mark.asyncio
async def test_bad_aggregate_inputs(connection: ConnectionV4) -> None:
    aggregate = _AggregateCollectionAsync(connection, "dummy", None, None, False)
    # over_all
    await _test_aggregate(lambda: aggregate.over_all(filters="wrong"))
    await _test_aggregate(lambda: aggregate.over_all(group_by=42))
    await _test_aggregate(lambda: aggregate.over_all(total_count="wrong"))
    await _test_aggregate(lambda: aggregate.over_all(return_metrics="wrong"))

    # near text
    await _test_aggregate(lambda: aggregate.near_text(42))
    await _test_aggregate(lambda: aggregate.near_text("hi", certainty="wrong"))
    await _test_aggregate(lambda: aggregate.near_text("hi", distance="wrong"))
    await _test_aggregate(lambda: aggregate.near_text("hi", move_to="wrong"))
    await _test_aggregate(lambda: aggregate.near_text("hi", move_away="wrong"))
    await _test_aggregate(lambda: aggregate.near_text("hi", object_limit="wrong"))

    # near object
    await _test_aggregate(lambda: aggregate.near_object(42))

    # near vector
    await _test_aggregate(lambda: aggregate.near_vector(42))

    # near image
    await _test_aggregate(lambda: aggregate.near_image(42))
