from the_module.beacon import admin_cli
import pytest



def test_main_create_table(parse):
    main = admin_cli.main(parse.create_table)
    assert main is True

def test_insert_data():
    main = admin_cli.main('-vcf')
    assert main is True

def test_main_find_dup():
    main = admin_cli.main('-fd')
    assert main is ""

def test_print():
    main = admin_cli.main('-p')
    assert main is ""

def test_main_count_variants():
    main = admin_cli.main('-c')
    assert main == 3

def test_update():
    main = admin_cli.main('-u')
    assert main is True

def test_delete():
    main= admin_cli.main('delete') 
    assert main is True

   
# assert admin_cli.main == 

#assert "hello" == "Hai" is an assertion failure.
#assert x == y,"test failed because x=" + str(x) + " y=" + str(y)#

#https://stackoverflow.com/questions/18160078/how-do-you-write-tests-for-the-argparse-portion-of-a-python-module