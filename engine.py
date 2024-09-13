import time

from simple_db import SimpleDatabase


def print_selected(header, rows):
    # header is a list of column names, rows is a list of rows
    # in turn, each row is a list of column values
    # e.g., if header = ['student name', 'ID', 'mark']
    # join command below will result in "student name, ID, mark"
    print('_' * 30) # repeat symbol '_' 30 times, thus creating a printed 'line'
    print(', '.join(header))
    print('_' * 30)
    for row in rows:
        print(', '.join(row))
    print('_' * 30)


def run_engine():
    print("Welcome to the SimpleQL Database Management System!")
    db = SimpleDatabase()

    while True:
        command = input("Enter command: ")
        if not command.endswith(";"):
            print("Commands should end with ; symbol.")
            continue

        command = command[:-1]  # to remove ; from the end
        if command == "exit":
            print("Leaving, bye!")
            break

        elif command == "show tables":
            # modify this section, so that the command
            # also prints columns for which index was built
            # note that our DBMS only supports loading one table at a time
            table_name = db.get_table_name()
            if table_name is None:
                print("... no tables loaded ...")
            else:
                #print table's name
                print(table_name)
                #print built index
                index_columns=[]
                #loop through each column index
                for i in range(len(db.header)):
                    column = db.header[i]
                    #print all index for each column if exist
                    if db.b_trees[i]:
                        index_columns.append(f"Index on column {column}")
                if index_columns:
                    #print \n after
                    print("\n".join(index_columns))


        elif command.startswith("copy "):
            # e.g., copy my_table from 'file_name.csv'
            words = command.split() # breaks down command into words
            # words[0] should be copy, words[1] should be table name, etc.
            if len(words) != 4:
                # we expect a particular number of words in this command
                print("Incorrect command format")
                continue

            table_name = words[1]
            file_name = words[3][1:-1] # to remove ' around file name
            db.load_table(table_name, file_name)

        elif command.startswith("select * from "):
            # e.g., select * from my_table where name="Bob"
            command = command.replace("=", " = ") # ensure spaces around =
            words = command.split() # breaks down command into words
            if len(words) != 8:
                # we expect a particular number of words in this command
                print("Incorrect command format")
                continue

            table_name = words[3]
            column_name = words[5]
            column_value = words[7][1:-1] # to remove " around the value

            start = time.time()
            header, rows = db.select_rows(table_name, column_name, column_value)
            end = time.time()

            if len(header) == 0:
                print("... no such table ...")
            else:
                print_selected(header, rows)
                print("Time elapsed: ", round(1000*(end - start)), " ms")

        # add code for processing create index and drop index here ...

        #create index
        elif command.startswith("create index on "):
            words = command.split()
            #uncrorrect command
            if len(words) != 4:
                print("Incorrect command.")
                continue

            column_name = words[3]

            #check if column exists
            if column_name not in db.columns:
                print(f"No such column {column_name} exists.")
                continue

            #get col id to check if index exist
            col_id = db.columns[column_name]
            #check if index exist
            if db.b_trees[col_id] is not None:
                print(f"Index already exists on column {column_name}.")
                continue

            #create index
            if column_name in db.columns:
                db.create_index(column_name)
                print(f"Created index for {column_name}.")

        #drop index
        elif command.startswith("drop index on "):
            words = command.split()
            column_name = words[3]
            #uncrorrect command
            if len(words) != 4:
                print("Incorrect command.")
                continue

            #check if column exists
            if column_name not in db.columns:
                print(f"No such column {column_name} exists.")
                continue

            #get col id to check if index exist
            col_id = db.columns[column_name]
            #check if index exist
            if db.b_trees[col_id] is None:
                print(f"No index on column {column_name}.")
                continue

            #drop index
            if column_name in db.columns:
                db.drop_index(column_name)
                print(f"Dropped index for {column_name}.")

        else:
            print("Unrecognized command!")

        print() # empty line after each command


if __name__ == "__main__":
    run_engine()
