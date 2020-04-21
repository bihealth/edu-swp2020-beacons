import sys
import re
import requests

"""
Provides command line interface for beacon
"""


def main():
    """
    Takes command line inputs from user, makes request for the variance and prints answer

    """
    print("Welcome to our project beacon software!\n")
    cont = True
    while cont:
        inp = input("Please enter your variant (chr-pos-ref-alt):\n")
        # if input is valid - communication to database and send answer
        if _check_input(inp):
            try:

                rep = requests.get("http://localhost:5000/api/" + inp)
                res = " - ".join(map(str, rep.json()["results"]))
                if isinstance(rep.json()["results"][4], bool):
                    print("The result of your request is:")
                    print(res, "\n")
                else:
                    print(  # pragma: nocover
                        "\nWe have troubles with the database, please ask your admin for help.\n"
                    )
                    print("The occuring error is: '", rep.json()["results"][4], "'\n")  # pragma: nocover
            except Exception as e:  # pragma: nocover
                print(  # pragma: nocover
                    "\nWe have troubles reaching the server, please ask your local administrator or start 'rest_apy.py' in a seperate terminal."
                )
                print(e.argv[0])  # pragma: nocover
        else:
            print(
                "Your input has the wrong format. For futher information tipp --help."
            )

        inp = input(
            "If you like to continue: Press [c]\nIf you like to quit: Press [q]\n"
        )
        if inp == "c":
            cont = True  # pragma: nocover
        elif inp == "q":
            cont = False
        else:
            print(
                "You did not choose an understandible input. Your session is quited now."
            )
            cont = False
    print("Thank you for using our tool.")


def _check_input(var_str):  # maybe better to check each input seperately
    """
    Checks if the input is a valid variant string
    :param var_str: string supposed to be in the format 'chr-pos-ref-alt'
    :return: bool which tells wether the input is valid
    """
    pattern = re.compile(
        r"""([1-9]|[1][0-9]|[2][0-2]|[XY])  # the chromosome
                        -(\d+)     # the position
                        -[ACGT]+   #RawDescriptionHelpFormatter,
                        -[ACGT]+  # alt""",
        re.X,
    )
    if re.fullmatch(pattern, var_str) is None:
        return False
    else:
        return True


def init():
    if __name__ == "__main__":
        sys.exit(main())  # pragma: nocover


init()
