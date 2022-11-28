#!/usr/bin/python3
###############################################################################
# Stock Programa
# Autors: Arthur Sturza, Wagner Andrade e Wesley Santos
# Date: 25/11/2022
#
# This program was created as the final delivery of module 1 (Basic Python) of
# Santander Corders course (Data Engineering class) taught by A.D.A..
# The objective is to develop a program to manage a stock of products
# following some requirements.
#
###############################################################################

# Version 2
# Written after the teacher's comments and suggestions
#
# Changes:
# 1 - Rewrite the code to English
# 2 - Establish standard Camel Case or Snake Case
# 3 - Subdivide import_data() method into other methods
# 

################################# Bibliotecas #################################
import pandas as pd
from tkinter import filedialog, Tk

################################### Classes ###################################
class Stock:
    def __init__(self):
        self.stock_prototype = {}
        self.PRODUCT_PROTOTYPE = {
                                'name':'name',
                                'price':'price',
                                'amount':'0'
                                } # Characteristics of the registered product

    def search_product(self, code: str = 'product_code', name: str = 'product_name') -> str:
        """Searches for the product by code or name"""

        if code in self.stock_prototype.keys(): # Check if the code exists
            return f'**Code {code} already registered for the product {self.stock_prototype[code]["name"]}', False
        for names in self.stock_prototype.values(): # Check if the name exists
            if name == names['name']:
                return f'**Product {name} already registered', False
        return '**New product', True


    def show_products(self) -> pd.DataFrame:
        """Displays list of highlighted products in pandas dataframe format"""

        df = pd.DataFrame.from_dict(self.stock_prototype, orient='index',
                                columns=['code', 'name', 'price', 'amount']) # Transform a dict into a DataFrame
        df = df.sort_values(by=['code'], ignore_index=True)
        if len(df) == 0:
            return '\n**There are no registered products'
        return df


    def refresh_product(self, product_code: str) -> dict:
        """Updates the attributes of the product that has the informed product_code"""
        produtoTemp = {}

        if product_code in self.stock_prototype.keys(): # Check if the product is registered
            for key in self.stock_prototype[product_code].keys():
                if key == 'code': # Separates the code to not allow the user to change it
                    produtoTemp.update({key:product_code})
                    continue
                value = input(f'Enter the new {key} of the registered product: ')
                produtoTemp.update({key:value})

            return self.stock_prototype.update({produtoTemp['code']:produtoTemp})

        print('\n**There are no products with this name')


    def delete_product(self, product_code: str) -> bool:
        """Removes from the dictionary the product that has the informed product_code"""

        if product_code in self.stock_prototype.keys():
            print(f'**Product {self.stock_prototype[product_code]["name"]} deleted successfuly')
            self.stock_prototype.pop(product_code) # Remove product from stock
            return True

        else:
            print('**Product not found')
            return False


    def insert_product(self) -> dict:
        """Register new products"""
        produtoTemp = {}

        for key in self.PRODUCT_PROTOTYPE.keys():
            value = input(f'Type {key} of the registered product:')
            produtoTemp.update({key:value})
        # Below occurs the update in the dictionary when there is already a product
        produtoTemp.update({'code':str((int(max(self.stock_prototype)) if len(self.stock_prototype) > 0 else 0) + 1)}) 
        

        msg, valid = self.search_product(produtoTemp['code'], produtoTemp['name'])
        if valid:
            print('\n**Product placed in stock')
            return self.stock_prototype.update({produtoTemp['code']:produtoTemp})
        else:
            print(msg)


    def export_data(self) -> None:
        """Export the data to a .csv file in users filesystem"""
        try:
            df = self.show_products() # Get the DataFrame
            df.to_csv('estoque.csv', index=False, sep=";", encoding='latin-1') # Saves the file to a format that could be used in Excel
            print('\n**Export successful')
        except:
            print("**Something went wrong trying to export the file")


    def select_file(self) -> object:
        root = Tk()

        file = filedialog.askopenfile() # Prompt the user to select the file using a graphical interface with tkinter
        root.destroy() # Close the tkinter window

        if file == None: # Validate if any file has been selected
            print('**Operation cancelled. No file selected.')
            return
        if file.name.split(".")[-1] != "csv": # Validate the file format
            print('**Incorrect format. Please select a .csv file.')
            return

        return file


    def validate_file_pattern(*kargs) -> bool:
        """Check if the file header is ['code', 'name', 'price', 'amount']"""
        if list(kargs[1].columns.values) == ['code', 'name', 'price', 'amount']: # Compare series index with the standard
            return True
        else:
            return False
    

    def get_lists_from_dict(*kargs) -> tuple:
        """Receive the df_dict and 1 list for each column"""
    
        list_code = [str(value) for value in kargs[1]['code'].values()]
        list_name = [str(value) for value in kargs[1]['name'].values()]
        list_price = [str(value) for value in kargs[1]['price'].values()]
        list_amount = [str(value) for value in kargs[1]['amount'].values()]
        return list_code, list_name, list_price, list_amount


    def import_data(self):
        """Imports inventory from a .csv file present on the user's filesystem"""
        file = self.select_file()
        
        if file:
            df = pd.read_csv(file, sep=';', encoding='latin-1', index_col=False) # Turn the file into a dataframe

            valid = self.validate_file_pattern(df) # Run the file pattern validation method

            if valid:
                df_dict = df.to_dict()
                
                # Populate lists with the contents of the file and then turn them into a dictionary in the expected pattern
                data_lists = self.get_lists_from_dict(df_dict)
                for index in range(len(data_lists)-1):
                    self.stock_prototype.update({data_lists[0][index]:{'name':data_lists[1][index],
                        'price':data_lists[2][index],'amount':data_lists[3][index],'code':data_lists[0][index]}})

                print('**Stock imported successfully!')
            else:
                print('**File outside the expected pattern. Import stopped.')


    def stock_menu(self):
        """Program menu. Interacts with the user and returns the string corresponding to the selected option."""
        print('\n' + '-'*48 + '\n*MENU*\n1- Insert Product\n2- Update Product\n3- Delete Product' +
                '\n4- Consult Product List\n5- Import file\n6- Export file\n0- Close\n')
        option = input('Enter the desired option: ')
        if option == '1':
            print('---->You chose "1- Insert Product"\n')
            self.insert_product()
            print('\n')

        elif option == '2':
            print('---->You chose "2- Update Product"\n')
            if len(self.stock_prototype) == 0:
                print('\n**There is no product registered in stock yet')
            else:
                code_produto = input('Enter the product code you would like to update: ')
                self.refresh_product(code_produto)
            print('\n')

        elif option == '3':
            print('---->You chose "3- Delete Product"\n')
            if len(self.stock_prototype) == 0:
                print('\n**There is no product registered in stock yet')
            else:
                code_produto = input('Enter the product code you would like to delete:')
                self.delete_product(code_produto)

        elif option == '4':
            print('---->You chose "4- Consult Product List"\n' + '-'*12 + 'PRODUCT LIST BELOW'+ '-'*12 + '\n')
            print(self.show_products())
            print('\n')

        elif option == '5':
            print('---->You chose "5- Import file"\n')
            self.import_data()
            print('\n')
            
        elif option == '6':
            print('---->You chose "6- Export file"\n')
            if len(self.stock_prototype) == 0:
                print('\n**Stock is still empty. It will not be possible to export the file.')
            else:
                self.export_data()
            print('\n')
            
        elif option == '0':
            print('**Closing #Stock Program#')
        else:
            print('---->Incorrect input. Try again.')

        return option


################################## Objetos ###################################
stock = Stock()


#################################### Main #####################################

loop = 1

print('\n**Welcome to the Stock program. Choose an option from the menu to continue.**')
while loop != '0':
    loop = stock.stock_menu()

