#!/usr/bin/python3
###############################################################################
#Programa Estoque
#Autores: Arthur Sturza, Wagner Andrade e Wesley Santos
#Data: 25/11/2022
#
#Este programa foi elaborado como entrega final do módulo 1 (Python básico) do
#curso Santander Corders (turma de Engenharia de Dados) ministrado pela A.D.A..
#O objetivo é elaborar um programa para administrar um estoque de produtos 
#seguindo alguns requisitos.
#
###############################################################################

################################# Bibliotecas #################################
import pandas as pd
from tkinter import filedialog, Tk

################################### Classes ###################################
class Estoque:
    def __init__(self):
        self.prototipoEstoque = {}
        self.prototipoProduto = {
                                'nome':'name',
                                'preço':'price',
                                'quantidade':'0'
                                } # Características do produto cadastrado

    def buscar_produto(self, codigo: str = 'product_code', nome: str = 'product_name') -> str:
        """Realiza a busca do produto tanto pelo código quanto pelo nome"""

        if codigo in self.prototipoEstoque.keys(): # Verifique se o código existe no estoque
            return f'**Codigo {codigo} já cadastrado para o produto {self.prototipoEstoque[codigo]["nome"]}', False
        for nomes in self.prototipoEstoque.values(): # verifica se o nome do produto existe no estoque
            if nome == nomes['nome']:
                return f'**Produto {nome} já cadastrado', False
        return '**Novo produto', True


    def mostrar_produtos(self) -> pd.DataFrame:
        """Exibe a lista de produtos destacadas em formato de dataframe do pandas"""

        df = pd.DataFrame.from_dict(self.prototipoEstoque, orient='index',
                                columns=['codigo', 'nome', 'preço', 'quantidade']) # Transforma o dicionário num DataFrame
        df = df.sort_values(by=['codigo'], ignore_index=True)
        if len(df) == 0:
            return '\n**Não há produtos cadastrados'
        return df


    def atualizar_produto(self, codigo_produto: str) -> dict:
        """Atualiza os atributos do produto que possui o codigo_produto informado"""
        produtoTemp = {}

        if codigo_produto in self.prototipoEstoque.keys(): # Verifica se o produto está cadastrado
            for key in self.prototipoEstoque[codigo_produto].keys():
                if key == 'codigo': # Separa o código para não permitir que o usuário o altere
                    produtoTemp.update({key:codigo_produto})
                    continue
                value = input(f'Digite o(a) novo(a) {key} do produto cadastrado: ')
                produtoTemp.update({key:value})

            return self.prototipoEstoque.update({produtoTemp['codigo']:produtoTemp})

        print('\n**Não há produtos com esse nome')


    def deletar_produto(self, codigo_produto: str) -> bool:
        """Remove do dicionário o produto que possui o codigo_produto informado"""

        if codigo_produto in self.prototipoEstoque.keys():
            print(f'**Produto {self.prototipoEstoque[codigo_produto]["nome"]} deletado com sucesso')
            self.prototipoEstoque.pop(codigo_produto) # Remove o produto do estoque
            return True

        else:
            print('**Produto não localizado no banco')
            return False


    def cadastrarProduto(self) -> dict:
        """Realiza o cadastro de novos produtos"""
        produtoTemp = {}

        for key in self.prototipoProduto.keys():
            value = input(f'Digite {key} do produto cadastrado: ')
            produtoTemp.update({key:value})
        # Abaixo ocorre o update no dicionário quando já houver algum produto
        produtoTemp.update({'codigo':str((int(max(self.prototipoEstoque)) if len(self.prototipoEstoque) > 0 else 0) + 1)}) 
        

        msg, validacao = self.buscar_produto(produtoTemp['codigo'], produtoTemp['nome'])
        if validacao:
            print('\n**Produto inserido no estoque')
            return self.prototipoEstoque.update({produtoTemp['codigo']:produtoTemp})
        else:
            print(msg)


    def exportar_estoque(self) -> None:
        """Exporta o estoque atual para um arquivo .csv criado no filesystem do usuário"""
        try:
            df = self.mostrar_produtos() # Obtém o DataFrame
            df.to_csv('estoque.csv', index=False, sep=";", encoding='latin-1') # Salva o arquivo de forma a ser legível via Excel
            print('\n**Exportação realizada com sucesso')
        except:
            print("**Algo deu errado ao tentar exportar o arquivo")


    def valida_formato_arquivo(*kargs) -> bool:
        """Valida se o arquivo possui o cabeçalho ['codigo', 'nome', 'preço', 'quantidade']"""
        if list(kargs[1].index.values) == ['codigo', 'nome', 'preço', 'quantidade']: # Compara os índices da série com o padrão esperado
            return True
        else:
            return False


    def importar_estoque(self):
        """Importa o estoque à partir de um arquivo .csv presente no filesystem do usuário"""
        root = Tk()

        list_codigo = []
        list_nome = []
        list_preco = []
        list_qtd = []

        file = filedialog.askopenfile() # Solicita a seleção do arquivo ao usuário utilizando uma interface gráfica com tkinter
        root.destroy() # Encerra a janela do tkinter

        if file == None: #Valida se algum arquivo foi selecionado
            print('**Operação cancelada. Nenhum arquivo selecionado.')
            return
        if file.name.split(".")[-1] != "csv": # Valida o formato do arquivo
            print('**Formato incorreto. Por favor selecione um arquivo .csv.')
            return

        df = pd.read_csv(file, sep=';', encoding='latin-1', index_col=False) # Transforma o arquivo em um dataframe

        validacao = self.valida_formato_arquivo(df.iloc[0]) # Executa o método de validação do padrão do arquivo
        if validacao:
            df_dict = df.to_dict()
            # Popula listas com o conteúdo do arquivo e depois as transforma em um dicionário no padrão esperado
            for value in df_dict['codigo'].values():
                list_codigo.append(str(value))

            for value in df_dict['nome'].values():
                list_nome.append(str(value))

            for value in df_dict['preço'].values():
                list_preco.append(value)

            for value in df_dict['quantidade'].values():
                list_qtd.append(value)

            for index in range(len(list_codigo)):
                self.prototipoEstoque.update({list_codigo[index]:{'nome':list_nome[index],'preço':list_preco[index],'quantidade':list_qtd[index],'codigo':list_codigo[index]}})

            print('**Estoque importado com sucesso!')
        else:
            print('**Arquivo fora do padrão esperado. Importação interrompida.')


    def menuEstoque(self):
        """Menu do programa. Interage com o usuário e retorna a string correspondente a opção selecionada."""
        print('\n------------------------------------------------\n*MENU*\n1- Inserir Produto\n2- Atualizar Produto\n3- Excluir Produto\n4- Consultar Lista de Produtos\n5- Importar arquivo\n6- Exportar arquivo\n0- Encerrar\n')
        option = input('Digite a opção desejada: ')
        if option == '1':
            print('---->Você escolheu "1- Inserir Produto"\n')
            self.cadastrarProduto()
            print('\n')

        elif option == '2':
            print('---->Você escolheu "2- Atualizar Produto"\n')
            if len(self.prototipoEstoque) == 0:
                print('\n**Ainda não há produto cadastrado no estoque')
            else:
                codigo_produto = input('Digite o código do produto que gostaria de atualizar: ')
                self.atualizar_produto(codigo_produto)
            print('\n')

        elif option == '3':
            print('---->Você escolheu "3- Excluir Produto"\n')
            if len(self.prototipoEstoque) == 0:
                print('\n**Ainda não há produto cadastrado no estoque')
            else:
                codigo_produto = input('Digite o código do produto que gostaria de excluir: ')
                self.deletar_produto(codigo_produto)

        elif option == '4':
            print('---->Você escolheu "4- Consultar Lista de Produtos"\n------------LISTA DE PRODUTOS ABAIXO------------\n')
            print(self.mostrar_produtos())
            print('\n')

        elif option == '5':
            print('---->Você escolheu "5- Importar arquivo"\n')
            self.importar_estoque()
            print('\n')
            
        elif option == '6':
            print('---->Você escolheu "6- Exportar arquivo"\n')
            if len(self.prototipoEstoque) == 0:
                print('\n**O estoque ainda está vazio. Não será possível exportar o arquivo.')
            else:
                self.exportar_estoque()
            print('\n')
            
        elif option == '0':
            print('**Encerrando #Programa Estoque#')
        else:
            print('---->Entrada incorreta. Tente novamente.')

        return option


################################## Objetos ###################################
estoque = Estoque()


#################################### Main #####################################

loop = 1

print('\n**Bem vindo ao programa Estoque. Escolha uma opção do menu para continuar.**')
while loop != '0':
    loop = estoque.menuEstoque()

