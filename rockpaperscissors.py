from random import choice as rand_choice
from collections import Counter
from time import sleep as time_sleep
from rich.console import Console as rich_console
from rich.table import Table as rich_table
from shutil import rmtree
from pathlib import Path

RED = "rgb(255,0,0)"
BLUE = "rgb(0,0,255)"
GREEN = "rgb(0,255,0)"
HOTPINK = "rgb(255,105,180)"

VALID_CHOICES = ["r", "p", "s"]

console = rich_console()


def delete_pycache(base_dir="."):
    for pycache in Path(base_dir).rglob("__pycache__"):
        rmtree(pycache)


def TypeWriter(text: str, color: str = "white", delay: float | int = 0):
    for c in text:
        console.print(c, style=color, end="")
        time_sleep(delay)
    console.print()


def InputUserForChoice() -> str | None:

    choice = "x"

    while True:
        choice = input("enter choice [rock -> r / paper -> p / scissors -> ] : ")

        if choice.casefold().strip() == "nothing":
            TypeWriter("you asked for it...\n", delay=0.08)
            TypeWriter(
                "Your worst sin is that you have destroyed and betrayed yourself for nothing\n",
                delay=0.08,
            )
            time_sleep(2)
            return None

        if choice in VALID_CHOICES:
            return choice

        else:
            console.print("INVALID INPUT BY USER !!", style=RED)
            console.print("user entered : " + str(choice), style=RED)
            console.print(
                "valid choices : [rock -> r / paper -> p / scissors -> s]", style=GREEN
            )
            continue


def GetAdminChoice() -> str:

    return rand_choice(VALID_CHOICES)


def GetWinner(UserChoice: str, AdminChoice: str) -> bool | None:

    user = UserChoice.casefold()
    admin = AdminChoice.casefold()

    if user not in VALID_CHOICES or admin not in VALID_CHOICES:

        error_message = f"""VALUE ERROR !!
        from fn : def GetWinner(UserChoice:str, AdminChoice:str) -> bool | None:
        values allowed to this fn are : {VALID_CHOICES}
        you passed value : {UserChoice}, {AdminChoice}"""

        raise ValueError(error_message)

    if user == admin:
        return None

    if user == "r":
        return False if admin == "p" else True

    if user == "p":
        return False if admin == "s" else True

    if user == "s":
        return False if admin == "r" else True


def PrintGameStatistics(stats_dict: dict) -> None:

    user_wins = stats_dict["win_record"].count(True)
    admin_wins = stats_dict["win_record"].count(False)
    draw_matches = stats_dict["win_record"].count(None)

    console.print("FINAL RESULT -> ", style=HOTPINK)

    if user_wins > admin_wins:
        console.print("USER won the game\n", style=HOTPINK)
    elif admin_wins > user_wins:
        console.print("ADMIN won the game\n", style=HOTPINK)
    else:
        console.print("MATCH DRAW\n", style=GREEN)

    table = rich_table(
        title="GAME RESULT", style="rgb(0,150,0)", title_justify="center"
    )

    table.add_column("attributes", justify="center", style="red")
    table.add_column("value", justify="center", style="red")

    table.add_row("total rounds played ", str(stats_dict["total_rounds"]), style="blue")
    table.add_row("user wins           ", str(user_wins), style="blue")
    table.add_row("admin wins          ", str(admin_wins), style="blue")
    table.add_row(
        "draws               ",
        str(draw_matches),
        style="blue",
    )

    print()
    console.print(table)
    print()

    rounds_played = len(stats_dict["win_record"])

    if rounds_played > 3:

        moves_table = rich_table(
            title="most Used Moves",
            title_justify="center",
            style="rgb(0,150,0)",
        )

        moves_table.add_column("attributes", justify="center")
        moves_table.add_column("values", justify="center")

        most_used_user_choice = Counter(stats_dict["user_moves"]).most_common(1)[0][0]

        most_used_admin_choice = Counter(stats_dict["admin_moves"]).most_common(1)[0][0]

        moves_table.add_row(
            "most used user choice",
            most_used_user_choice,
            style="rgb(0,150,0)",
        )

        moves_table.add_row(
            "most used admin choice",
            most_used_admin_choice,
            style="rgb(0,150,0)",
        )

        print()
        console.print(moves_table)
        print()


def PrintCurrentWinnerColored(winner: bool | None) -> None:

    if winner is None:
        TypeWriter("DRAW\n", color=GREEN, delay=0.02)
    elif winner is True:
        TypeWriter("USER won this round\n", color=BLUE, delay=0.02)
    else:
        TypeWriter("ADMIN won this round\n", color=RED, delay=0.02)


def PlayGame():

    total_rounds = int(
        input("enter the number of rounds you want to play (1 / 3 / 5 / 7) : ")
    )

    if total_rounds not in (1, 3, 5, 7):
        console.print("INVALID INPUT BY USER !!", style=RED)
        console.print("valid rounds = [1, 3, 5, 7]", style=GREEN)
        return

    game_stats = {
        "total_rounds": total_rounds,
        "user_moves": [],
        "admin_moves": [],
        "win_record": [],
    }

    user_wins = 0
    admin_wins = 0
    majority = (total_rounds // 2) + 1

    for i in range(total_rounds):

        user_choice = InputUserForChoice()
        admin_choice = GetAdminChoice()

        if user_choice is None:
            continue

        game_stats["user_moves"].append(user_choice)
        game_stats["admin_moves"].append(admin_choice)

        current_winner = GetWinner(user_choice, admin_choice)
        game_stats["win_record"].append(current_winner)

        TypeWriter(f"ROUND -> {i + 1}\n", color=RED, delay=0.05)

        TypeWriter(
            "user choice : "
            + str(user_choice)
            + "\nadmin choice : "
            + str(admin_choice)
            + "\n",
            color=GREEN,
            delay=0.02,
        )

        PrintCurrentWinnerColored(current_winner)

        if current_winner is True:
            user_wins += 1

        if current_winner is False:
            admin_wins += 1

        if user_wins == majority:
            game_stats["total_rounds"] = len(game_stats["win_record"])
            console.print("\nUSER HAS WON THE MAJORITY OF ROUNDS !", style=HOTPINK)
            break

        if admin_wins == majority:
            game_stats["total_rounds"] = len(game_stats["win_record"])
            console.print("\nADMIN HAS WON THE MAJORITY OF ROUNDS !", style=HOTPINK)
            break

    PrintGameStatistics(game_stats)
