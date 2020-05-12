"""
Provides command line interface for beacon
"""
import sys
import re
import requests
import base64
import matplotlib.pyplot as plot
import matplotlib.image as mpimg
import io

def main():
    """
    Takes command line inputs from user, makes request for the variance and prints answer

    """
    print("Welcome to our project beacon software!\n")
    ver = (False,None)
    while ver[0] is not True:
        inp = input("Please enter your secret token or enter nothing to continue as not registered user: ")
        if inp:
            ver = verify_token(inp)
            if ver[0] is None:
                print("There are troubles with the user database.")
                print("The occuring error is: '", ver[1],"'")
        else:
            inp = ""
            ver = (True, "Unregistered user")
    print("Hello", ver[1])
    cookie = inp

    cont = True
    while cont:
        inp = input("Please enter your variant (chr-pos-ref-alt):\n")
        # if input is valid - communication to database and send answer

        if _check_input(inp):
            inp_dict = string_to_dict(inp)
            out = query_request(inp_dict, cookie)
            if out[0]:
                print_results(out[1])
        else:
            print("Your input has the wrong format.")


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


def verify_token(inp):
    resp = requests.post("http://localhost:5000/api/verify", headers={"token": inp})
    if resp.json()["verified"] is None:
        return(None, resp.json()["error"])
    elif resp.json()["verified"]:
        return (True, resp.json()["user"])
    else:
        print("This is not a valid token.")
        return (False, None)


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


def string_to_dict(inp):
    inp_list = inp.split("-")
    inp_dict = {
        "chr": inp_list[0],
        "pos": inp_list[1],
        "ref": inp_list[2],
        "alt": inp_list[3],
    }
    return inp_dict


def query_request(inp_dict, cookie):

        connection_established = False
        try:
            rep = requests.post(
                "http://localhost:5000/query", json=inp_dict, headers={"token": cookie}
            )
            connection_established = True
        except Exception as e:  # pragma: nocover
            print(  # pragma: nocover
                    "\nWe have troubles reaching the server, please ask your local administrator."
            )
        if connection_established:
            outp_dict = rep.json()
            return (True, outp_dict)
        else:
            return (False, None)

def print_results(outp_dict):
    #print(outp_dict)
    if outp_dict['occ'] == None:
        if outp_dict['error'] == None:
            print("You are not allowed to make more requests from this IP-address.")
        else:
            print(  # pragma: nocover
                "We have troubles with the database, please ask your admin for help."
            )
            print("The occuring error is: '", outp_dict['error'], "'")  # pragma: nocover
    else:
        print_dict = {x: outp_dict[x] for x in outp_dict if x != 'statistic'}
        print("The result of your request is:")
        print(print_dict)
        if 'statistic' in outp_dict and outp_dict['statistic']:
            stat_byte = outp_dict['statistic'].encode('ascii')
            figure = base64.b64decode(stat_byte)
            img = mpimg.imread(io.BytesIO(figure))
            imgplot = plot.imshow(img)
            plot.savefig('stat_population_'+outp_dict['chr']+'_'+str(outp_dict['pos'])+'_'+outp_dict['ref']+'_'+outp_dict['alt']+ '.png')


def init():
    if __name__ == "__main__":
        sys.exit(main())  # pragma: nocover


init()
