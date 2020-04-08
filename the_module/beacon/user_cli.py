import argparse
import os
import re
import textwrap
#import beacon.common


def __main__():
    """ var_str = user input
    Output (print): Annotated Variant
    the function receives some command parameters like the Variant    string or help
    host$ python beacon.user_cli.py var_str
    """
    #first input and user communication
    print("Welcome to our project beacon software!\n" )
    cont = True
    while cont:
        inp = input("Please enter your variant (chr-pos-res-alt): \n" )
        # if input is valid - communication to database and send answer
        
        if _check_input(inp):
            try:
                print("test 1")
            except: 
                inp = input("If you like to continue: Press [c]\n If you like to quit: Press [q]")
            if inp == c: 
                cont = True
            elif inp == q:
                cont = False 
            else: 
                print("You did not choose an understandible input. Your session is quited now.")
                cont = False
        elif inp == "--help":
            helpinp = input("please type your needed help (chr-pos-res-alt)")
            _help_(helpinp)
            break
        elif inp == "exit" :
            break
        else:
            print("Your input has the wrong format. For futher information tipp --help.")
            #call help function

    print("Thank you for using our tool.")

    
    
   
def _check_input(var_str):  #maybe better to check each input seperately
    """Input: variant_str
    Output: check_bool
    function checks if input has correct input format
    """
    pattern = re.compile(r"""([1-9]|[1][0-9]|[2][0-2]|[XY])  # the chromosome
                        -(\d+)     # the position
                        -[ACGT]+   #RawDescriptionHelpFormatter,
                        -[ACGT]+  # alt""", re.X)
    if re.fullmatch(pattern, var_str) == None:
        return False
    else:
        return True


def _help_(help_var):
    const = True
    while const:
        if help_var == "chr":
            print ("information about chr \n")
        elif help_var == "pos":
            print ("information about pos \n")
        elif help_var == "res":
            print ("information about res \n")
        elif help_var == "alt":
            print ("information about alt \n")

        inp = input("any other question? y/n : \n")
        if inp == "n":
            const = False
            break
        else:
            inp_extra = input("what do you want to type in ? : \n")
            _help_(inp_extra)

    
#--help with different options
def _help_for_admin():
    print ("what kind of help do you need?")
    h_inp= input("please select your help type\n")

    parser = argparse.ArgumentParser( add_help=True,               formatter_class=argparse.RawDescriptionHelpFormatter,
                    description="""
                        Please type var_str in some way
                        """,
                    epilog="""
                        epilog should be here written
                        
                        """,
                        )

    parser.add_argument('-a', action="store_true",help=
    """ argument
            help is
            wrapped
            """,
    )
    parser.print_help()
     #here define argment
    parser.add_argument("--input",type=str ,default= ' ',help="please type in blablabla valid input format")
    parser.add_argument("--variant",help="variant should be given in format chr-pos-res-alt")
    parser.add_argument("--result",help="result will be given in yes or no form from beacon")
    parser.add_argument("--info",help="variant should be given in chr,pos,res,alt")
    
    #here save typed argument
    args= parser.parse_args()
    input = args.input
    variant = args.variant
    result = arg.result

 if __name__ == __main__():
     __main__()   
    
