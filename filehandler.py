# Custom File Reader Class

class FileHandler:
    def __init__(self, file_name):
        self.file_name = f'input/{file_name}'

    def set_file_name(self, file_name ):
        self.file_name = f'input/{file_name}'

    def read_first_line(self):
        try: 
            with open(self.file_name, 'r') as file:
                first_line = file.readline().strip()
                integers = list(map(int, first_line.split()))
                if len(integers) != 3:
                    raise ValueError( 'Expected three integers separated by a space' )
                return integers
        except FileNotFoundError:
            print( f'Error: File \'{self.file_name}\' not found.' )
        except ValueError as ve:
            print( f'Error: A value error occured: {ve}' )
        except Exception as e: 
            print( f'Error: An unexpected error occured: {e}' )