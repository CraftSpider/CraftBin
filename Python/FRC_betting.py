# FRC Betting through command line
import utils.file_readers as file_util
import utils.interp as interp
import pickle

data_file = "data/FRC_Data.dat"


class User:

    __slots__ = ("name", "cash")

    def __init__(self, name, cash):
        self.name = name
        self.cash = cash

    def __str__(self):
        return self.name


class Round:

    __slots__ = ("number", "red_teams", "blue_teams", "_result")

    def __init__(self, number, red_teams, blue_teams):
        self.number = number
        self.red_teams = red_teams.copy()
        self.blue_teams = blue_teams.copy()
        self._result = None

    def __str__(self):
        return str(self.number)

    def resolve_round(self, result):
        if self._result is None:
            self._result = result is "BLUE"
        else:
            raise AttributeError

    def get_winner(self):
        if self._result is True:
            return "BLUE"
        elif self._result is False:
            return "RED"
        else:
            return None


class Bet:

    __slots__ = ("user", "round", "amount", "result")

    def __init__(self, user, _round, amount, result):
        self.user = user
        self.round = _round
        self.amount = amount
        self.result = result


class Data:

    __slots__ = ("users", "rounds", "bets")

    def __init__(self, users=None, rounds=None, bets=None):
        self.users = users or []
        self.rounds = rounds or []
        self.bets = bets or []

    def __del__(self):
        print("Saving Data")
        file_util.overwrite_file(data_file, pickle.dumps(self), "wb")

    def add_user(self, user):
        self.users.append(user)

    def add_round(self, _round):
        self.rounds.append(_round)

    def add_bet(self, bet):
        self.bets.append(bet)

    def get_user(self, name):
        for item in self.users:
            if item.name == name:
                return item
        return None

    def get_round(self, num):
        for item in self.rounds:
            if item.number == num:
                return item
        return None

    def remove_user(self, name):
        for item in self.users:
            if item.name == name:
                break
        else:
            return None
        self.users.remove(item)
        return item

    def remove_round(self, num):
        for item in self.rounds:
            if item.number == num:
                break
        else:
            return None
        self.rounds.remove(item)
        return item


class FRCContext(interp.Context):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = self.interpreter.data


runner = interp.Interpreter("FRC Betting", opening="FRC Betting V1.1", ctx_class=FRCContext)


def load_file(filename):
    with open(filename, "rb") as file:
        try:
            return pickle.load(file)
        except EOFError:
            return None


@runner.command(name="createuser", pass_ctx=True)
def create_user(ctx, username="", start_val=""):
    username = username or input("Username: ")
    start_val = start_val or input("Starting cash: ")
    try:
        start_val = float(start_val)
    except ValueError:
        print("Invalid starting cash")
        return
    user = User(username, start_val)
    ctx.data.add_user(user)
    print("Created user", user.name, "with starting value", user.cash)


@runner.command(name="removeuser", pass_ctx=True)
def remove_user(ctx, username):
    username = username or input("Username: ")
    user = ctx.data.remove_user(username)
    if user:
        print("Removed user " + user.name)
    else:
        print("User doesn't exist")


@runner.command(name="createround", pass_ctx=True)
def create_round(ctx, round_num="", red_team="", blue_team=""):
    round_num = round_num or input("Round Number: ")
    red_team = red_team or input("Red Alliance: ").strip()
    blue_team = blue_team or input("Blue Alliance: ").strip()
    try:
        round_num = int(round_num)
    except ValueError:
        print("Invalid round number")
        return
    red_team = list(map(int, red_team.split()))
    blue_team = list(map(int, blue_team.split()))
    if len(blue_team) != 3 or len(red_team) != 3:
        print("Please give 3 teams on each alliance!")
        return
    _round = Round(round_num, red_team, blue_team)
    ctx.data.add_round(_round)
    print("Created round #{}".format(_round.number))


@runner.command(name="removeround", pass_ctx=True)
def remove_round(ctx, num=""):
    num = num or input("Round Number: ")
    try:
        num = int(num)
    except ValueError:
        print("Invalid round number")
    _round = ctx.data.remove_round(num)
    if _round:
        print("Removed round", _round.number)
    else:
        print("Round doesn't exist")


@runner.command(name="resolveround", pass_ctx=True)
def resolve_round(ctx, num="", result=""):
    num = num or input("Round Number: ")
    result = result or input("Winner: ").upper()
    try:
        num = int(num)
    except ValueError:
        print("Invalid round number")
        return
    if result != "RED" and result != "BLUE":
        result = "UNKNOWN"
    _round = ctx.data.get_round(num)
    if _round:
        _round.resolve_round(result)
        print("Round result set")
    else:
        print("Round doesn't exist")


@runner.command(name="addbet", pass_ctx=True)
def add_bet(ctx, name="", num="", amount="", result=""):
    name = name or input("Username: ")
    num = num or input("Round Number: ")
    result = result or input("Result Guess: ").upper()
    amount = amount or input("Bet Total: ")
    try:
        num = int(num)
    except ValueError:
        print("Invalid round number")
        return
    try:
        amount = int(amount)
    except ValueError:
        print("Bet Total must be a whole number")
        return
    if result != "RED" and result != "BLUE":
        print("Invalid result guess")
        return
    user = ctx.data.get_user(name)
    _round = ctx.data.get_round(num)
    if user and _round:
        if user.cash >= amount:
            user.cash = user.cash - amount
            bet = Bet(user, _round, amount, result)
            ctx.data.add_bet(bet)
        else:
            print("Insufficient funds")
    else:
        print("Invalid username or round number")


@runner.command(name="resolvebets", pass_ctx=True)
def resolve_bets(data):
    pot = {}
    winners = {}
    resolved = []
    for bet in data.bets:
        name = bet.user.name
        num = bet.round.number
        amount = bet.amount
        result = bet.result

        if data.get_round(num).get_winner() is None:
            continue
        if pot.get(num):
            pot[num] += amount
        else:
            pot[num] = amount
        if data.get_round(num).get_winner() == result:
            if winners.get(num):
                winners[num] += [name]
            else:
                winners[num] = [name]
        resolved.append(bet)
    for bet in resolved:
        data.bets.remove(bet)
    for num in winners:
        winnings = round(pot[num] / len(winners[num]), 2)
        for winner in winners[num]:
            data.get_user(winner).cash += winnings


@runner.command(name="list", pass_ctx=True)
def _list(ctx, form=""):
    form = form or input("Users or Rounds? ").strip()
    form = form.upper()
    if form == "USERS":
        for user in ctx.data.users:
            print("Name:", user.name)
            print("Current Value:", user.cash)
    elif form == "ROUNDS":
        for _round in ctx.data.rounds:
            print("Number:", _round.number)
            print("Red Alliance:", _round.red_teams[0], _round.red_teams[1], _round.red_teams[2])
            print("Blue Alliance:", _round.blue_teams[0], _round.blue_teams[1], _round.blue_teams[2])
            print("Result:", _round.get_winner())
    elif form == "BETS":
        for bet in ctx.data.bets:
            print("User:", bet.user)
            print("Round:", bet.round)
            print("Result:", bet.result)
            print("Amount:", bet.amount)


@runner.command(name="help")
def help_command():
    print("Welcome to FRC Betting V1.1.")
    print("Valid commands:")
    print("LIST: Lists current saved users or rounds")
    print("CREATEUSER: Create a new user")
    print("DELETEUSER: Remove an existing user")
    print("CREATEROUND: Create a new competition round")
    print("DELETEROUND: Remove an old competition round")
    print("RESOLVEROUND: Declare a winner for a round")
    print("ADDBET: Create a new bet from a user for a round")


def main():
    data = load_file(data_file) or Data()
    runner.data = data
    runner.run()


if __name__ == "__main__":
    main()
