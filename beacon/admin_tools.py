"""
...that maintain the database
"""

import sqlite3
import vcf
import csv
import secrets

def parse_vcf(infile, con):
    """
    Reads given files and inserts the data into a database.
    :param infile[0]: a vcf file for variants
    :param infile[1]: a tsv file for population
    :param infile[2]: a tsv or xslx file for phenotype
    :param con: connection to the database
    :rtype: bool
    """
    try:
        #reads tsv file for population and creates for each sample a dict entry with pop and sex
        populationDict = {}
        with open(infile[1], 'r') as tsv_file:
            
            tsv_reader = csv.DictReader(tsv_file, dialect='excel-tab')
            # count = 0
            try:
                for row in tsv_reader:
                    populationDict[row['Sample name']] = {'pop_code':row['Population code'], 'sex':row['Sex'] } 
            except Exception as error:
                return "An error has occured: " + str(error)
                # count = count + 1
                # if count == 8:
                #     break
        #------------------------------------------------------------------------------------
        # reads file for phenotype and creates for each sample a dict entry with hpo-term-id and hpo-term-name
        phenotypeDict = {}
        with open(infile[2], 'r') as phenotype_file:
            # count=0
            key = 0
            phenotype_reader = csv.DictReader(phenotype_file, dialect='excel-tab')
            try:
                for row in phenotype_reader:
                    phenotypeDict[key] = {'HPO-Term-ID':row['HPO-Term-ID'],'HPO-Term-Name':row['HPO-Term-Name']}
                    # print(row['HPO-Term-ID'])
                    key += 1
                    # count += 1
                    # if count == 8:
                    #     break
            except KeyError as error:
                return "An error has occured: " + str(error)
    except Exception as error:
        return "An error has occured: " + str(error)
    #------------------------------------------------------------------------------------
    pheno_key = 0
    try:
        with open(infile[0])as vcf_file:
            vcf_reader = vcf.Reader(vcf_file)
            for variant in vcf_reader:
                chr = variant.CHROM      
                pos = variant.POS
                ref = variant.REF
                alt = "".join(str(i or "") for i in variant.ALT) # add ,

                #for allel
                hemi_alt = 0
                hemi_ref = 0
                wildtype = 0
                alt_hetero = 0
                alt_homo = 0

                tempDict = {}
                for sample in variant.samples:
                    sample_id = sample.sample
                    gt = sample.gt_type

                    if sample_id in populationDict:
                        population = populationDict[sample_id]['pop_code']

                        if population not in tempDict: 
                            tempDict[population] = {'pop_wildtype':0, 'pop_alt_hetero':0, 'pop_alt_homo':0, 'pop_hemi_ref':0, 'pop_hemi_alt':0}
                        # case autosome 
                        if chr == 'Y' or chr == 'X':
                            # case male
                            if populationDict[sample_id]['sex'] == 'male':
                                if gt == 2:  # 2 => hom_alt
                                    hemi_alt += 1 
                                    tempDict[population]['pop_hemi_alt'] +=1
                                else:  # sample.gt_type == 0 => hom_ref / wildtype
                                    hemi_ref += 1
                                    tempDict[population]['pop_hemi_ref'] +=1
                            # case female
                            else: 
                                if gt == 0: 
                                    wildtype += 1
                                    tempDict[population]['pop_wildtype'] +=1
                                # elif gt == 1:
                                #     alt_hetero += 1
                                #     tempDict[population]['pop_alt_hetero'] +=1
                                else:  # gt == 2
                                    alt_homo += 1
                                    tempDict[population]['pop_alt_homo'] +=1
                        # not autosome
                        else:
                            if gt == 0:
                                wildtype += 1
                                tempDict[population]["pop_wildtype"] += 1
                            elif gt == 1:
                                alt_hetero += 1
                                tempDict[population]["pop_alt_hetero"] += 1
                            else:  # gt == 2
                                alt_homo += 1
                                tempDict[population]['pop_alt_homo'] +=1

                    else: 
                        population = None
                        if population not in tempDict: 
                            tempDict[population] = {'pop_wildtype':0, 'pop_alt_hetero':0, 'pop_alt_homo':0, 'pop_hemi_ref':0, 'pop_hemi_alt':0}
                        if gt == 0:
                            wildtype += 1
                            tempDict[population]["pop_wildtype"] += 1
                        elif gt == 1:
                            alt_hetero += 1
                            tempDict[population]["pop_alt_hetero"] += 1
                        else:  # gt == 2
                            alt_homo += 1
                            tempDict[population]['pop_alt_homo'] +=1

                #INSERT   - Duplicates allowed
                sql_str = "INSERT INTO allel (chr,pos,ref,alt, wildtype, alt_hetero, alt_homo, hemi_ref, hemi_alt) VALUES (?,?,?,?,?,?,?,?,?);"
                parameters = (chr, pos, ref, alt, wildtype, alt_hetero, alt_homo, hemi_ref, hemi_alt)
                output = con.parse_statement(sql_str, parameters)
                sql_str2 = "INSERT INTO phenotype (chr,pos,ref,alt,phenotype) VALUES (?,?,?,?,?);"
                phenotype = phenotypeDict[pheno_key]['HPO-Term-ID']+'; '+ phenotypeDict[pheno_key]['HPO-Term-Name']
                pheno_key += 1
                parameters2 = (chr, pos, ref, alt, phenotype)
                output2 = con.parse_statement(sql_str2, parameters2)

                if isinstance(output,list) is False or isinstance(output2,list) is False:  # pragma: no cover 
                    raise output or output2

                for td in tempDict:                   
                    sql_str1 = "INSERT INTO populations (chr,pos,ref,alt, wildtype, alt_hetero, alt_homo, hemi_ref, hemi_alt, population) VALUES (?,?,?,?,?,?,?,?,?,?);"
                    parameters1 = (chr, pos, ref, alt, tempDict[td]['pop_wildtype'],tempDict[td]['pop_alt_hetero'], tempDict[td]['pop_alt_homo'], tempDict[td]['pop_hemi_ref'], tempDict[td]['pop_hemi_alt'], td)
                    output1 = con.parse_statement(sql_str1, parameters1)

                    if isinstance(output1,list) is False:  # pragma: no cover
                        raise output1
            return True
    except Exception as e:
        return "An error has occured: " + str(e)



class CreateDbCommand:
    """
    Creates variant table in database.
    """

    def __init__(self):
        self.data = []

    def create_tables(self, con):
        """
        Creates variant table in database.
        :param con: connection to the database
        :rtype: bool
        """
        sql_create_db_table_allel = """
            CREATE TABLE IF NOT EXISTS allel (
            id integer PRIMARY KEY AUTOINCREMENT,
            chr text NOT NULL,
            pos integer NOT NULL,
            ref text NOT NULL,
            alt text NOT NULL,
            wildtype integer NOT NULL,
            alt_hetero integer NOT NULL,
            alt_homo integer NOT NULL,
            hemi_ref integer NOT NULL,
            hemi_alt integer NOT NULL
        );"""
        sql_create_db_table_populations = """
            CREATE TABLE IF NOT EXISTS populations (
            id integer PRIMARY KEY AUTOINCREMENT,
            chr text NOT NULL,
            pos integer NOT NULL,
            ref text NOT NULL,
            alt text NOT NULL,
            wildtype integer NOT NULL,
            alt_hetero integer NOT NULL,
            alt_homo integer NOT NULL,
            hemi_ref integer NOT NULL,
            hemi_alt integer NOT NULL,
            population text 
        );"""
        sql_create_db_table_phenotype = """
            CREATE TABLE IF NOT EXISTS phenotype (
            id integer PRIMARY KEY AUTOINCREMENT,
            chr text NOT NULL,
            pos integer NOT NULL,
            ref text NOT NULL,
            alt text NOT NULL,
            phenotype text
        );"""
        try:
            con.parse_statement(sql_create_db_table_allel, ())
            con.parse_statement(sql_create_db_table_populations, ())
            con.parse_statement(sql_create_db_table_phenotype, ())
            sql_idx_allel = "CREATE INDEX allel_idx ON allel(chr,pos,ref,alt);"
            sql_idx_population = "CREATE INDEX pop_idx ON populations(chr,pos,ref,alt);"
            sql_idx_phenotype = "CREATE INDEX phe_idx ON phenotype(chr,pos,ref,alt);"
            con.parse_statement(sql_idx_allel, ())
            con.parse_statement(sql_idx_population, ())
            con.parse_statement(sql_idx_phenotype, ())
            return True
        except sqlite3.Error as e:
            return "An error has occured: " + str(e)


class OperateDatabase:
    """
    Provides tools to maintain the database.
    """

    def __init__(self):
        self.data = []

    def print_db(self, con):
        """
        Prints whole database.
        :param con: connection to the database
        :return: database
        """
        try:
            sql_print_allel = "SELECT id, chr, pos, ref, alt , wildtype, alt_hetero, alt_homo, hemi_ref, hemi_alt FROM allel GROUP BY id, chr, pos, ref, alt, wildtype, alt_hetero, alt_homo, hemi_ref, hemi_alt;"
            output_allel = con.parse_statement(sql_print_allel, ())
            sql_print_population = "SELECT id, chr, pos, ref, alt , wildtype, alt_hetero, alt_homo, hemi_ref, hemi_alt, population FROM populations GROUP BY id, chr, pos, ref, alt, wildtype, alt_hetero, alt_homo, hemi_ref, hemi_alt, population;"
            output_population = con.parse_statement(sql_print_population, ())
            sql_print_phenotype = "SELECT id, chr, pos, ref, alt , phenotype FROM phenotype GROUP BY id, chr, pos, ref, alt, phenotype;"
            output_phenotype = con.parse_statement(sql_print_phenotype, ())
            print("TABLE allel: \n")
            for out in output_allel:
                print(out)
            print("\nTABLE populations: \n")
            for out in output_population:
                print(out)
            print("\nTABLE phenotype: \n")
            for out in output_phenotype:
                print(out)
            return ""
        except sqlite3.Error as e:
            return "An error has occured: " + str(e)

    def count_variants(self, con):
        """
        Counts the existing number of (all) Variants.
        :param con: connection to the database
        :rtype: int
        """
        try:
            sql_count_var = "SELECT COUNT(*) FROM allel GROUP BY chr, pos, alt, ref;"
            output = con.parse_statement(sql_count_var, ())
            return len(output)
        except sqlite3.Error as e:
            return "An error has occured: " + str(e)

    def updating_allel(self, con, allel):
        """
        Updates a row in the table allel of the database according to given id and input.
        :param con: connection to the database
        :param allel : (chr, pos, ref, alt, wildtype, alt_hetero, alt_homo, hemi_ref, hemi_alt, id)
        :rtype: bool
        """
        try:
            chr = allel[0]
            pos = allel[1]
            ref = allel[2]
            alt = allel[3]
            wildtype = allel[4]
            alt_hetero = allel[5]
            alt_homo = allel[6]
            hemi_ref = allel[7]
            hemi_alt = allel[8]
            id = allel[9]
            sql_str = "UPDATE allel SET chr = ?, pos = ?, ref = ?, alt = ?, wildtype = ?, alt_hetero = ?, alt_homo = ?, hemi_ref = ?, hemi_alt = ?  WHERE id = ?;"
            parameters = (
                chr,
                pos,
                ref,
                alt,
                wildtype,
                alt_hetero,
                alt_homo,
                hemi_ref,
                hemi_alt,
                id,
            )
            con.parse_statement(sql_str, parameters)
            return "The table allel has been updated. Call -p to see the changes."
        except sqlite3.Error as e:
            return "An error has occured: " + str(e)

    def updating_populations(self, con, populations):
        """
        Updates a row in the table populations of the database according to given id and input.
        :param con: connection to the database
        :param populations : (chr, pos, ref, alt, wildtype, alt_hetero, alt_homo, hemi_ref, hemi_alt, population, id)
        :rtype: bool
        """
        try:
            chr = populations[0]
            pos = populations[1]
            ref = populations[2]
            alt = populations[3]
            wildtype = populations[4]
            alt_hetero = populations[5]
            alt_homo = populations[6]
            hemi_ref = populations[7]
            hemi_alt = populations[8]
            population = populations[9]
            id = populations[10]
            sql_str = "UPDATE populations SET chr = ?, pos = ?, ref = ?, alt = ?, wildtype = ?, alt_hetero = ?, alt_homo = ?, hemi_ref = ?, hemi_alt = ?, population = ?  WHERE id = ?;"
            parameters = (
                chr,
                pos,
                ref,
                alt,
                wildtype,
                alt_hetero,
                alt_homo,
                hemi_ref,
                hemi_alt,
                population,
                id,
            )
            con.parse_statement(sql_str, parameters)
            return "The table populations has been updated. Call -p to see the changes."
        except sqlite3.Error as e:
            return "An error has occured: " + str(e)

    def updating_phenotype(self, con, phenotype):
        """
        Updates a row in the table phenotype of the database according to given id and input.
        :param con: connection to the database
        :param phenotype : (chr, pos, ref, alt, phenotype, id)
        :rtype: bool
        """
        try:
            chr = phenotype[0]
            pos = phenotype[1]
            ref = phenotype[2]
            alt = phenotype[3]
            phenotype = phenotype[4]
            id = phenotype[5]
            sql_str = "UPDATE phenotype SET chr = ?, pos = ?, ref = ?, alt = ?, phenotype = ?  WHERE id = ?;"
            parameters = (chr, pos, ref, alt, phenotype, id)
            con.parse_statement(sql_str, parameters)
            return "The table phenotype has been updated. Call -p to see the changes."
        except sqlite3.Error as e:
            return "An error has occured: " + str(e)

    def delete_data_allel(self, con, id):
        """
        Deletes a row in table allel with given id in the database.
        :param con: connection to the database
        :param id: id
        :rtype: in case error string
        """
        try:
            sql_str = "DELETE FROM allel WHERE id= ?;"
            con.parse_statement(sql_str, id)
            return "call -p to see the changes"
        except sqlite3.Error as e:
            return "An error has occured: " + str(e)

    def delete_data_populations(self, con, id):
        """
        Deletes a row in table populations with given id in the database.
        :param con: connection to the database
        :param id: id
        :rtype: in case error string
        """
        try:
            sql_str = "DELETE FROM populations WHERE id= ?;"
            con.parse_statement(sql_str, id)
            return "call -p to see the changes"
        except sqlite3.Error as e:
            return "An error has occured: " + str(e)

    def delete_data_phenotype(self, con, id):
        """
        Deletes a row in table phenotype with given id in the database.
        :param con: connection to the database
        :param id: id
        :rtype: in case error string
        """
        try:
            sql_str = "DELETE FROM phenotype WHERE id= ?;"
            con.parse_statement(sql_str, id)
            return "call -p to see the changes"
        except sqlite3.Error as e:
            return "An error has occured: " + str(e)


class UserDB:
    """
    Maintenance of the user database
    """

    def __init__(self):
        self.data = []

    def create_tables_user(self, con):
        """
        Creates variant table in database.

        :param con: connection to the database
        :rtype: bool
        """
        sql_create_login_table = """
            CREATE TABLE IF NOT EXISTS login (
            id integer PRIMARY KEY,
            name text NOT NULL,
            token text NOT NULL,
            authorization integer NOT NULL
        );"""

        sql_create_ip_table = """
            CREATE TABLE IF NOT EXISTS ip (
            id integer PRIMARY KEY,
            count_req integer NOT NULL,
            ip_addr text NOT NULL
        );"""

        try:
            output = con.parse_statement(sql_create_login_table, ())
            output2 = con.parse_statement(sql_create_ip_table, ())
            return True
        except sqlite3.Error as e:      # pragma: nocover
            return "An error has occured: " + str(e)

    def insert_user(self, acc, con):
        """
        Adds user to database with a token and authorization number and prevents duplication of usernames.

        :param username: username and authorization-key
        :param con: connection to the database
        :rtype: bool
        """
        name = acc[0]
        authorization = acc[1]
        token = secrets.token_urlsafe()
        try:
            sql_find_dup = "SELECT name FROM login WHERE name = ?"
            output = con.parse_statement(sql_find_dup, [name])
            if output == []:
                try:
                    sql_str = (
                        "INSERT INTO login(name,token,authorization) VAlUES(?,?,?);"
                    )
                    parameters = (name, token, authorization)
                    output = con.parse_statement(sql_str, parameters)
                    return True
                except sqlite3.Error as e:
                    return "An error has occured: " + str(e)
            else:
                return "Username already exists"
        except sqlite3.Error as e:
            return "An error has occured: " + str(e)

    def find_user_token(self, con, username):
        """
        finds the token for the associated username

        :param con: connection to the database
        :return: token
        """
        try:
            sql_find_dup = "SELECT token FROM login WHERE name = ?"
            output = con.parse_statement(sql_find_dup, [username])
            print("Token:")
            return output[0][0]
        except sqlite3.Error as e:
            return "An error has occured: " + str(e)

    def print_db_user(self, con):
        """
        Prints whole database.

        :param con: connection to the database
        :return: database
        """
        try:
            sql_print = "SELECT * FROM login"
            output = con.parse_statement(sql_print, ())
            print("TABLE login: \n")
            for out in output:
                print(out)
            return ""
        except sqlite3.Error as e:
            return "An error has occured: " + str(e)

    def print_ip(self, con):
        """
        Prints whole database.

        :param con: connection to the database
        :return: database
        """
        try:
            sql_print = "SELECT * FROM ip"
            output = con.parse_statement(sql_print, ())
            print("TABLE ip: \n")
            for out in output:
                print(out)
            return ""
        except sqlite3.Error as e:
            return "An error has occured: " + str(e)

    def delete_user(self, con, id):
        """
        Deletes a row with given id in the database.

        :param con: connection to the database
        :param id: id
        :rtype: bool
        """
        try:
            sql_str = "DELETE FROM login WHERE id= ?;"
            parameters = str(id)
            output = con.parse_statement(sql_str, parameters)
            print("rufe -p auf, um die Änderung zu sehen")
            return True
        except sqlite3.Error as e:
            return "An error has occured: " + str(e)

    def delete_ip(self, con, id):
        """
        Deletes a row with given id in the database.

        :param con: connection to the database
        :param id: id
        :rtype: bool
        """
        try:
            sql_str = "DELETE FROM ip WHERE id= ?;"
            parameters = str(id)
            output = con.parse_statement(sql_str, parameters)
            print("rufe -p auf, um die Änderung zu sehen")
            return True
        except sqlite3.Error as e:
            return "An error has occured: " + str(e)
