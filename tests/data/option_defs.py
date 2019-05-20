from typing import NamedTuple, List, Dict


class OptionsOnly(NamedTuple):
    a1: int
    a2: float
    a3: str
    a4: bool
    a5: List[int]
    a6: List[float]
    a7: List[str]
    a8: List[bool]
    a9: Dict[str, int]
    a10: Dict[str, float]
    a11: Dict[str, str]
    a12: Dict[str, bool]
    a13: List[List[int]]
    a14: List[Dict[str, int]]
    a15: Dict[str, Dict[str, int]]
    a16: Dict[str, List[int]]


class OptionsDefaults(NamedTuple):
    a1: int = 5
    a2: float = 5.5
    a3: str = "abc"
    a4: bool = True
    a5: List[int] = [5, 5]
    a6: List[float] = [5.5, 5.5]
    a7: List[str] = ["abc", "abc"]
    a8: List[bool] = [True, False]
    a9: Dict[str, int] = {"a": 5, "b": 5}
    a10: Dict[str, float] = {"a": 5.5, "b": 5.5}
    a11: Dict[str, str] = {"a": "ab", "b": "bc"}
    a12: Dict[str, bool] = {"a": True, "b": False}
    a13: List[List[int]] = [[1, 2], [3, 4]]
    a14: List[Dict[str, int]] = [{"a": 5, "b": 5}, {"a": 5, "b": 5}]
    a15: Dict[str, Dict[str, int]] = {"a": {"a": 5, "b": 5}, "b": {"a": 5, "b": 5}}
    a16: Dict[str, List[int]] = {"a": [1, 2], "b": [3, 4]}
