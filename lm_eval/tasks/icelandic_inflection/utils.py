import json
from typing import Any, List, Mapping, cast

from lm_eval.api.filter import Filter


def json_match(sampled_json: Any, correct_json: Any) -> bool:
    """Return True if the sampled completion in JSON format
    matches a correct answer, component by component"""
    if sampled_json is None or correct_json is None:
        # Missing values are never correct
        return False
    if isinstance(sampled_json, dict):
        if isinstance(correct_json, dict):
            sample = cast(Mapping[str, Any], sampled_json)
            correct = cast(Mapping[str, Any], correct_json)
            all_keys = set(sample.keys()) | set(correct.keys())
            return all(json_match(sample.get(key), correct.get(key)) for key in all_keys)
        else:
            return False
    elif isinstance(sampled_json, list):
        if isinstance(correct_json, list):
            slist = cast(List[Any], sampled_json)
            clist = cast(List[Any], correct_json)
            if len(slist) != len(clist):
                # Lists must have the same length
                return False
            return all(json_match(s, c) for s, c in zip(slist, clist))
        else:
            return False
    # Not a structured item: do a direct comparison
    return sampled_json == correct_json


def json_metric(items):
    try:
        # Get substring between first and last curly braces
        sampled_json = json.loads(items[0])
        correct_json = json.loads(items[1])
    except json.JSONDecodeError:
        # Invalid JSON is always wrong
        return 0
    return int(json_match(sampled_json, correct_json))

