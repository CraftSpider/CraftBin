
from typing import Tuple, Union, List, Optional, Dict, Callable

Number = Union[int, float]

class User:

    __slots__ = ... # type: Tuple[str, ...]

    name = ... # type: str
    cash = ... # type: Number

    def __init__(self, name: str, cash: Number) -> None: ...

    def __str__(self) -> str: ...


class Round:

    __slots__ = ... # type: Tuple[str, ...]

    number = ... # type: int
    red_teams = ... # type: List[int]
    blue_teams = ... # type: List[int]
    _result = ... # type: Optional[bool]

    def __init__(self, number: int, red_teams: List[int], blue_teams: List[int]) -> None: ...

    def __str__(self) -> str: ...

    def resolve_round(self, result: str) -> None: ...

    def get_winner(self) -> Optional[str]: ...


class Bet:

    __slots__ = ... # type: Tuple[str, ...]

    user = ... # type: User
    round = ... # type: Round
    amount = ... # type: Number
    result = ... # type: str

    def __init__(self, user: User, _round: Round, amount: Number, result: str) -> None: ...


class Data:

    __slots__ = ... # type: Tuple[str, ...]

    users = ... # type: List[User]
    rounds = ... # type: List[Round]
    bets = ... # type: List[Bet]

    def __init__(self, users: List[User] = ..., rounds: List[Round] = ..., bets: List[Bet] = ...) -> None: ...

    def add_user(self, user: User) -> None: ...

    def add_round(self, _round: Round) -> None: ...

    def add_bet(self, bet: Bet) -> None: ...

    def get_user(self, name: str) -> Optional[User]: ...

    def get_round(self, num: int) -> Optional[Round]: ...

    def remove_user(self, name: str) -> Optional[User]: ...

    def remove_round(self, num: int) -> Optional[Round]: ...

commands = Dict[str, Callable]

def command(name: str = ...) -> Callable[[Callable], Callable]: ...

def load_file(filename: str) -> Data: ...

def create_user(data: Data, username: str = ..., start_val: str = ...) -> None: ...

def remove_user(data: Data, username: str = ...) -> None: ...

def create_round(data: Data, round_num: str = ..., red_team: str = ..., blue_team: str = ...) -> None: ...

def remove_round(data: Data, num: str = ...) -> None: ...

def resolve_round(data: Data, num: str = ..., result: str = ...) -> None: ...

def add_bet(data: Data, name: str = ..., num: str = ..., amount: str = ..., result: str = ...) -> None: ...

def resolve_bets(data: Data) -> None: ...

def _list(data: Data, form: str = ...) -> None: ...

def help_command(data: Data) -> None: ...