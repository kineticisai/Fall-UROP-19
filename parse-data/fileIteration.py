import parse
import sqlite3
import sys
import os
#files in the folder are sequentially ordered, for each folder there is first and last file number
#also note that each file starts with 0, but python doesn't support number assignment like x=01
firstFile = 301001
lastFile = 304271

def overwriteAll(init, final):
    conn = sqlite3.connect('UROP_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS nlp_data
             ([file_id] INTEGER PRIMARY KEY,[abstract] text, [intro] text, [conclusion] text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS failed_data
             ([file_id] INTEGER PRIMARY KEY,[abstract] text, [intro] text, [conclusion] text)''')

    unicode_fail_count = 0
    doesnt_exist = 0
    other_error_count = 0
    failed_data_count = 0
    data_count = 0
    while init < final:
        #my code has the folder named 2003copy, replace with your folder name
        try:
            file = "/Users/nadiawaid/Documents/UROP/2003/"
            file = os.path.join(file, '0'+str(init))
            parsed_file = parse.parse_file(file)
            if None in parsed_file:
                for i in range(len(parsed_file)):
                    if parsed_file[i] is None:
                        parsed_file[i] = 'None'
                #c.execute('''INSERT OR REPLACE INTO failed_data(init, parsed_file[0], parsed_file[1], parsed_file[2]) VALUES(?,?,?,?);''', (init, parsed_file[0], parsed_file[1], parsed_file[2]))
                c.execute('''INSERT OR REPLACE INTO failed_data VALUES (?,?,?,?);''', (init, parsed_file[0], parsed_file[1], parsed_file[2]))
                conn.commit()
                failed_data_count +=1
            else:
                c.execute('''INSERT OR REPLACE INTO nlp_data VALUES (?,?,?,?);''', (init, parsed_file[0], parsed_file[1], parsed_file[2]))
                conn.commit()
                data_count+=1
        except UnicodeDecodeError:
            unicode_fail_count+=1
        except IOError:
            doesnt_exist+=1
        except Exception as e:
            print(init, e)
            other_error_count += 1
        init+=1
    c.close()
    conn.close()
    return unicode_fail_count, doesnt_exist, other_error_count, failed_data_count, data_count

print(overwriteAll(firstFile, lastFile))
