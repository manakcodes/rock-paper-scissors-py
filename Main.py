from rockpaperscissors import (
    HOTPINK,
    PlayGame,
    console,
    TypeWriter,
    RED,
    GREEN,
    delete_pycache,
)


if __name__ == "__main__":

    TypeWriter(
        "A minimal, terminal based Rock–Paper–Scissors game written in Python with colored output,\ntypewriter effects, and tabulated results.\n\n",
        color=HOTPINK,
        delay=0.025,
    )

    PlayGame()

    while True:
        console.print("continue game ? [Y / y / N / n] : ", style=HOTPINK)
        choice = input()

        if choice == "Y" or choice == "y":
            PlayGame()

        elif choice == "N" or choice == "n":
            delete_pycache()
            TypeWriter("***** EXIT *****", color=RED, delay=0.10)
            break

        else:
            TypeWriter("INVALID CHOICE !!", color=RED)
            TypeWriter("user entered -> " + str(choice), color=RED)
            TypeWriter("valid choices : [Y / y / N / n]", color=GREEN)

# nothing
