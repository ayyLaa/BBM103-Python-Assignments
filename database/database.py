from sys import argv
import ast
import re


def create_table(database, table_name, columns):
    if table_name in database:
        raise ValueError(f"Table {table_name} already exists")

    # Create dictionary with table names as keys and
    # dictionaries (with columns as keys and empty lists as values) as values
    database[table_name] = {column: [] for column in columns}

    return database


def insert(database, table_name, rows):
    if table_name not in database:
        raise KeyError(f"Table {table_name} not found")

    # Get list of columns from database dictionary
    columns = list(database[table_name].keys())

    if len(rows) != len(columns):
        raise ValueError(
            f"Number of values ({len(rows)}) "
            f"does not match the number of columns ({len(columns)})\n"
        )

    # Append each value to corresponding column
    for column, row in zip(columns, rows):
        database[table_name][column].append(row)

    return database


def delete(database, table_name, conditions):
    if table_name not in database:
        raise KeyError(f"Table {table_name} not found")

    rows_deleted = 0
    columns = list(database[table_name].keys())

    for condition_key in conditions.keys():
        if condition_key not in columns:
            raise KeyError(f"Column {condition_key} does not exist")

    if len(conditions) == 0:
        rows_deleted = len(database[table_name][columns[0]])
        for column in columns:
            database[table_name][column] = []
    else:
        indexes_to_delete = []
        # Iterate through each row to find the index of rows to delete
        for i in range(len(database[table_name][columns[0]])):
            row = {} # Create dictionary to keeps each rows values
            # Add the column-value pairs to dictionary for the current row
            for column in columns:
                row[column] = database[table_name][column][i]
            # Check if all conditions match the current row's values
            if all(
                str(row[key]) == str(value) for key, value in conditions.items()
            ):
               indexes_to_delete.append(i)

        # Delete in reverse order to avoid index shifting
        for index in reversed(indexes_to_delete):
            for column in columns:
                del database[table_name][column][index]
            rows_deleted += 1

    return database, rows_deleted


def select(database, table_name, columns,
           conditions):
    if table_name not in database:
        raise KeyError(f"Table {table_name} not found")

    # If columns are not specified, get all columns
    if columns == "*":
        columns = list(database[table_name].keys())

    rows = []  # Collect rows that match the given conditions as list

    for column in columns:
         if column not in list(database[table_name].keys()):
            raise KeyError(f"Column {column} does not exist")

    for condition_key in conditions.keys():
        if condition_key not in list(database[table_name].keys()):
            raise KeyError(f"Column {condition_key} does not exist")

    #Check is there conditions if there are no conditions specified select all rows
    #else select rows given by condition
    if len(conditions) == 0:
        for i in range(len(database[table_name][columns[0]])):
            row = []
            for column in columns:
                row.append(database[table_name][column][i])
            rows.append(tuple(row))
    else:
        for i in range(len(database[table_name][columns[0]])):
            row = {}
            for column in list(database[table_name].keys()):
                row[column] = database[table_name][column][i]
            # Check if all conditions match the current row's values
            if all(
                str(row[key]) == str(value) for key, value in conditions.items()
            ):
                row_to_select = ()
                for column in columns:
                    row_to_select += (database[table_name][column][i],)
                rows.append(row_to_select)

    return rows


def join(database, table_name1, table_name2,
         join_on_column):
    if table_name1 not in database:
        raise KeyError(f"Table {table_name1} does not exist")
    elif table_name2 not in database:
        raise KeyError(f"Table {table_name2} does not exist")

    columns1 = list(database[table_name1].keys())
    columns2 = list(database[table_name2].keys())

    if join_on_column not in columns1 or join_on_column not in columns2:
        raise KeyError(f"Column {join_on_column} does not exist")

    rows1 = []
    rows2 = []
    table3_columns = columns1 + columns2
    table3_rows = []

    #Get rows from both tables
    for i in range(len(database[table_name1][columns1[0]])):
        row = {}
        for column1 in list(database[table_name1].keys()):
            row[column1] = database[table_name1][column1][i]
        rows1.append(row)

    for j in range(len(database[table_name2][columns2[0]])):
        row = {}
        for column2 in list(database[table_name2].keys()):
            row[column2] = database[table_name2][column2][j]
        rows2.append(row)

    # Compare rows in both table and merge them if they match with the join column
    for row1 in rows1:
        for row2 in rows2:
            if row1[join_on_column] == row2[join_on_column]:
                merged_rows = (
                        [row1[column1] for column1 in columns1] +
                        [row2[column2] for column2 in columns2]
                )
                table3_rows.append(merged_rows)

    return table3_rows, table3_columns, len(table3_rows)


def update(database, table_name, updates,
           conditions):
    if table_name not in database:
        raise KeyError(f"Table {table_name} not found")

    columns = list(database[table_name].keys())

    for update_key in updates.keys():
        if update_key not in columns:
            raise KeyError(f"Column {update_key} does not exist")

    for condition_key in conditions.keys():
        if condition_key not in columns:
            raise KeyError(f"Column {condition_key} does not exist")

    rows_updated = 0
    for i in range(len(database[table_name][columns[0]])):
        row = {}
        for column in columns:
            row[column] = database[table_name][column][i]
        # Check if all conditions for updating match the current row's values
        # If match update it with updates
        if all(
            str(row[key]) == str(value) for key, value in conditions.items()
        ):
            for column_to_update, row_to_update in updates.items():
                database[table_name][column_to_update][i] = row_to_update
            rows_updated += 1

    return database, rows_updated


def count(database, table_name, conditions):

    if table_name not in database:
        raise KeyError(f"Table {table_name} not found")

    number_of_entries = 0
    columns = list(database[table_name].keys())

    for condition_key in conditions.keys():
        if condition_key not in columns:
            raise KeyError(f"Column {condition_key} does not exist")

    # If no conditions provided count all rows
    if len(conditions) == 0:
       number_of_entries = len(database[table_name][columns[0]])
    else:
        for i in range(len(database[table_name][columns[0]])):
            row = {}
            for column in columns:
                row[column] = database[table_name][column][i]
            # Check if all conditions match the current row's values
            if all(
                str(row[key]) == str(value) for key, value in conditions.items()
            ):
                 number_of_entries += 1

    return number_of_entries


def print_output(database, table_name, command,
                 columns, conditions, rows,
                 updates, rows_updated, rows_deleted,
                 number_of_entries, rows_joined, join_on_column,
                 error_message):
    print(f"{'#'*22} {command} {'#'*25}")

    if command == "CREATE":
        print(f"Table '{table_name}' created with columns: {columns}")

    elif command == "INSERT":
        if error_message is not None:
            print(error_message)
        print(f"Inserted into '{table_name}': {tuple(rows)}")
        if (error_message is not None and "Table" not in error_message) or \
            error_message is None:
            print_table(
                [row for row in zip(*database[table_name].values())],
                list(database[table_name].keys()),
                table_name
            )

    elif command == "SELECT":
        if error_message is not None:
            print(error_message)
            select_result = None
        else:
            select_result = select(database, table_name, columns, conditions)
        print(f"Condition: {conditions}")
        print(f"Select result from '{table_name}': {select_result}")

    elif command == "COUNT":
        if error_message is not None:
            print(error_message)
        else:
            print(f"Count: {count(database, table_name, conditions)}")
        print(f"Total number of entries in '{table_name}' is {number_of_entries}")

    elif command == "UPDATE":
        print(f"Updated '{table_name}' with {updates} where {conditions}")
        if error_message is not None:
            print(error_message)
        print(f"{rows_updated} rows updated.")
        if (error_message is not None and "Table" not in error_message) or \
            error_message is None:
            print_table(
                [row for row in zip(*database[table_name].values())],
                list(database[table_name].keys()),
                table_name
            )

    elif command == "DELETE":
        print(f"Deleted from '{table_name}' where {conditions}")
        if error_message is not None:
            print(error_message)
        print(f"{rows_deleted} rows deleted.")
        if (error_message is not None and "Table" not in error_message) or \
            error_message is None:
            print_table(
                [row for row in zip(*database[table_name].values())],
                list(database[table_name].keys()),
                table_name
            )

    elif command == "JOIN":
        table_name1 = table_name[0]
        table_name2 = table_name[1]
        print(f"Join tables {table_name1} and {table_name2}")
        if error_message is not None:
            print(error_message)
        else:
            print(f"Join result ({rows_joined} rows):")
            joined_rows, joined_columns, _ = \
                join(database, table_name1, table_name2, join_on_column)
            print_table(joined_rows, joined_columns, "Joined Table")

    print(55 * "#", "\n")


def print_table(rows, columns, table_name):
    print(f"\nTable: {table_name}")

    # If rows is a single string convert it to list
    if rows and isinstance(rows[0], str):
        rows = [rows]

    # Get the max length for each column
    columns_widths = [
        max(len(str(data)) for data in column)
        for column in zip(columns, *rows)
    ]

    # Create table border
    table_border = ""
    for width in columns_widths:
        table_border += "+" + "-" * (width + 2)
    table_border += "+"
    print(table_border)

    # Print the column headers
    # Each column name is left-justified
    print("".join(
        f"| {str(columns[i]).ljust(columns_widths[i])} "
        for i in range(len(columns))
    ) + "|")
    print(table_border)

    # Print the rows
    # Each row is left-justified
    for row in rows:
        print("".join(
            f"| {str(row[i]).ljust(columns_widths[i])} "
            for i in range(len(row))
        ) + "|")
    print(table_border)


def main():
    if len(argv) != 2:
        print("It should be written as: python database.py <input_file>")
        return

    # Initialize the database as an empty dictionary
    database = {}

    try:
        with open(argv[1], "r") as input_file:
            # Check if the input file is empty
             if not input_file.read():
                 print("Input text is empty.")
                 return
             input_file.seek(0)
            # Iterate over each line in input file.
             for line in input_file:
                 # Skip empty lines
                 if not line.strip():
                     continue
                 else:
                      # Get database command and table name from command statement.
                      command_statement = line.strip().split(maxsplit=2)
                      command = command_statement[0]
                      table_name = command_statement[1]
                      if len(command_statement) < 3:
                          command_statement.append("")

                      if command == "CREATE_TABLE":
                         try:
                             # Check if columns are provided
                             if not command_statement[2].strip():
                                 raise ValueError(f"Syntax error in {command}. No provided columns.\n")

                             # Check if there is one or more columns
                             if "," in command_statement[2]:
                                columns = command_statement[2].split(",")
                             else:
                                 columns = [command_statement[2].strip()]

                             # Check if any columns' name is empty
                             if any(not column.strip() for column in columns):
                                 raise ValueError(f"Syntax error in {command}. Invalid column names.\n")

                             database = create_table(database, table_name, columns)
                             print_output(database, table_name, "CREATE",
                                          columns, None, None,
                                          None, None, None,
                                          None, None, None,
                                          None)
                         except ValueError as e:
                             print(str(e).strip("'"))

                      elif command == "INSERT":
                          try:
                              # Check if values are provided
                              if not command_statement[2].strip():
                                  raise ValueError(f"Syntax error in {command}. No provided values.\n")

                              # Check if there is one or more rows
                              if "," in command_statement[2]:
                                  rows = command_statement[2].split(",")
                              else:
                                  rows = [command_statement[2].strip()]

                              database = insert(database, table_name, rows)
                              print_output(database, table_name, command,
                                           None, None, rows,
                                           None, None, None,
                                           None,None, None,
                                           None)
                          except ValueError as e:
                              print(str(e).strip("'"))
                          except KeyError as e:
                              print_output(database, table_name, command,
                                           None, None, rows,
                                           None, None, None,
                                           None,None, None,
                                           str(e).strip("'"))

                      elif command == "DELETE":
                           try:
                               # Check if there is WHERE clause
                               if "WHERE" in command_statement[2]:
                                  # Extract everything after WHERE
                                  where_clause = command_statement[2].split("WHERE", 1)[1].strip()
                                  # If there is nothing after WHERE raise error
                                  if not where_clause:
                                      raise ValueError(
                                          f"Syntax error in {command}. "
                                          f"No conditions provided after WHERE.\n"
                                      )
                                  elif where_clause == "{}":
                                      raise ValueError(
                                          f"Syntax error in {command}."
                                          f"It should be used DELETE {table_name} to delete all rows.\n"
                                      )
                                  else:
                                       # Match everything between {} to get conditions
                                       commands = re.findall(r'\{.*?}|\S+', command_statement[2])
                                       # Parse input to Python object in this case dictionary
                                       conditions = ast.literal_eval(commands[1])
                               else:
                                   # There's no WHERE clause, all rows will be deleted
                                   conditions = {}
                               database, deleted_rows = delete(database, table_name, conditions)
                               print_output(database, table_name, command,
                                            None, conditions, None,
                                            None, None, deleted_rows,
                                            None,None, None,
                                            None)
                           except KeyError as e:
                               print_output(database, table_name, command,
                                            None, conditions, rows,
                                            None, None,0,
                                            None,None, None,
                                            str(e).strip("'"))
                           except ValueError as e:
                               print(str(e).strip("'"))

                      elif command == "COUNT":
                           try:
                               # Check if there is WHERE clause
                               if "WHERE" in command_statement[2]:
                                  # Extract everything after WHERE
                                  where_clause = command_statement[2].split("WHERE", 1)[1].strip()
                                  # Check if conditions are correct
                                  # if conditions "*"  count all rows
                                  if  where_clause == "*":
                                      conditions = {}
                                  elif where_clause == "{}":
                                      raise ValueError(
                                          f"Syntax error in {command}. Invalid conditions."
                                          f"It should be used COUNT {table_name} WHERE * to count all rows.\n"
                                      )
                                  elif not where_clause:
                                      raise ValueError(f"Syntax error in {command}. Invalid conditions.\n")
                                  else:
                                      # Match everything between {} to get conditions
                                      commands = re.findall(r'\{.*?}|\S+', command_statement[2])
                                      # Check if conditions are provided
                                      if not commands:
                                         raise ValueError(f"Syntax error in {command}. Invalid conditions.\n")
                                  # Parse input to Python object in this case dictionary
                                  conditions = ast.literal_eval(commands[1])
                               else:
                                   raise ValueError(f"Syntax error {command}. Missing WHERE clause.\n")
                               print_output(database, table_name, command,
                                            None, conditions, None,
                                            None, None, None,
                                            count(database, table_name, conditions),None, None,
                                            None)
                           except KeyError as e:
                               print_output(database, table_name, command,
                                            None, conditions, None,
                                            None, None,None,
                                            0,None, None,
                                            str(e).strip("'"))
                           except ValueError as e:
                               print(str(e).strip("'"))

                      elif command == "SELECT":
                           try:
                               # Check if there is WHERE clause
                               if "WHERE" in command_statement[2]:
                                  # Match everything before and after WHERE to get columns and conditions
                                  match = re.match(r"^(.*?)\s+WHERE\s+(.*)$", command_statement[2])

                                  # Check if WHERE clause is valid
                                  if match:
                                     # Extract columns
                                     columns = match.group(1).strip()
                                     # Extract conditions
                                     conditions = match.group(2).strip()
                                  else:
                                      raise ValueError(f"Syntax error in {command}. Invalid WHERE clause.\n")

                                  # Check how column are given
                                  if columns == "*":
                                         pass
                                  else:
                                        if len(columns) == 1:
                                            columns = [columns]
                                        else:
                                            columns = columns.split(",")
                                  # Check if any columns' name is empty
                                  if any(not column.strip() for column in columns):
                                      raise ValueError(f"Syntax error in {command}. Invalid column names.\n")
                                  conditions = ast.literal_eval(conditions)
                               else:
                                   conditions = {}
                                   if command_statement[2] == "*":
                                      columns = "*"
                                   else:
                                       if len(command_statement[2]) == 1:
                                           columns = [command_statement[2]]
                                       else:
                                           columns = command_statement[2].split(",")

                               select(database, table_name, columns, conditions)
                               print_output(database, table_name, command,
                                            columns, conditions, None,
                                            None,None, None,
                                           None,None, None,
                                            None)
                           except KeyError as e:
                               print_output(database, table_name, command,
                                            columns, conditions, None,
                                            None, None,None,
                                            None,None, None,
                                            str(e).strip("'"))
                           except ValueError as e:
                               print(str(e).strip("'"))

                      elif command == "UPDATE":
                          try:
                             if not command_statement[2].strip():
                                 raise ValueError(f"Syntax error in {command}. No provided conditions.\n")
                             # Match everything before and after WHERE to get columns and conditions
                             match = re.match(r"^(.*?)\s+WHERE\s+(.*)$", command_statement[2])
                             # Check if WHERE clause is valid
                             if match:
                                updates = match.group(1).strip()
                                conditions = match.group(2).strip()
                             else:
                                 raise ValueError(f"Syntax error in {command}. Invalid updates or conditions.\n")

                             # Check if conditions are provided
                             if conditions == "{}":
                                 raise ValueError(f"Syntax error in {command}. Conditions cannot be empty.\n")
                             else:
                                 updates = ast.literal_eval(updates)
                                 conditions = ast.literal_eval(conditions)

                             database, rows_updated = update(database, table_name, updates, conditions)
                             print_output(database, table_name, command,
                                             None, conditions, None,
                                             updates, rows_updated, None,
                                             None,None, None,
                                             None)

                          except KeyError as e:
                              print_output(database, table_name, command,
                                           None, conditions, None,
                                           updates, 0,None,
                                           None,None, None,
                                           str(e).strip("'"))
                          except ValueError as e:
                              print(str(e).strip("'"))

                      elif command == "JOIN":
                           try:
                               if not command_statement[2].strip():
                                   raise ValueError(f"Syntax error in {command}. No provided join column.\n")

                               # Check if there are two tables
                               if "," not in table_name:
                                   raise ValueError(f"Syntax error in {command}. There must be two tables.\n")

                               tables = table_name.split(",")

                               # Check if table names are valid
                               if not tables[0].strip() or not tables[1].strip():
                                   raise ValueError(f"Syntax error in {command}. One or both of the table names are invalid.\n")

                               # Check if there is colum after ON
                               if not command_statement[2].split("ON", 1)[1].strip():
                                   raise ValueError(f"Syntax error in {command}. Join column cannot be empty.\n")

                               table_name1 = tables[0]
                               table_name2 = tables[1]
                               join_on_column = command_statement[2].split("ON", 1)[1].strip()

                               _, _, joined_rows = \
                                   join(database, table_name1, table_name2, join_on_column)
                               print_output(database, tables, command,
                                            None, None, None,
                                            None, None, None,
                                            None, joined_rows, join_on_column,
                                            None)
                           except KeyError as e:
                               print_output(database, tables, command,
                                            None, None, None,
                                            None, None,None,
                                            None,None, None,
                                            str(e).strip("'"))
                           except ValueError as e:
                               print(str(e).strip("'"))
                      else:
                          # Skip unrecognized commands.
                          continue
    # Handle errors related to file access
    except FileNotFoundError:
        print("Input file does not exist.")
        return
    except PermissionError:
        print("Permission denied.")
        return

if __name__ == '__main__':
    main()