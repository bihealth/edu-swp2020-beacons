import argparse
import sys
#import beacon.common

def main(args):
    """ var_str = user input
    Output (print): Annotated Variant
    the function receives some command parameters like the Variant    string or help
    host$ python beacon.user_cli.py var_str
    """
    pass
def _check_input(var_str):
    """Input: variant_str
    Output: check_bool
    function checks if input has correct input format
    """
    #it checks inputs with common id here
    logincheck = cur.execute(loadname, login)


def _help_():
    #mit argsparse
    """with click button (html) can see following instructions
    1) what to input(varianble type: no special letters)
    2) how and where to type in
    3) how to change search types
    """
    parser = argparse.ArgumentParser(description='TEST TEST ')
    #here define argment
    parser.add_argument('--target',required=True, help='target variant')
    parser.add_argument('--user',required=False,default='admin',help='choose user')
    #here save typed argument
    args= parser.parse_args()

    print(args.target)
    print(args.user)    

