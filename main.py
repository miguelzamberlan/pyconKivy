# -*- coding: utf-8 -*-
__version__ = '0.1'

from collections import OrderedDict
import pymysql
import kivy
kivy.require('1.10.0')

# Imports kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.clock import Clock


class TelaPrincipal(Screen):

    def on_enter(self, *args):

        # Abrimos uma conexão com o banco de dados:
        conexao = pymysql.connect(host='SEU_HOST', 
                                    db='SEU_DB', 
                                    user='SEU_USER', 
                                    passwd='SUA_PASS')

        # Cria um cursor:
        cursor = conexao.cursor()

        # Executa o comando:
        cursor.execute("SELECT * FROM contato")

        # Recupera o resultado:
        resultado = cursor.fetchall()

        contatos = OrderedDict()
        contatos['Nome'] = {}
        contatos['E-mail'] = {}

        dadosNome = []
        dadosEmail = []

        for dados in resultado:
            dadosNome.append(dados[1])
            dadosEmail.append(dados[2])

        # Finaliza a conexão
        conexao.close()

        dados_length = len(dadosNome)
        idx = 0
        while idx < dados_length:
            contatos['Nome'][idx] = dadosNome[idx]
            contatos['E-mail'][idx] = dadosEmail[idx]
            idx += 1

        col_titles = [k for k in contatos.keys()]
        rows_len = len(contatos[col_titles[0]])
        self.columns = len(col_titles)

        table_data = []
        for t in col_titles:
            table_data.append(
                {'text': str(t), 'size_hint_y': None, 'height': 60, 'bcolor': (.06, .45, .45, 1)})

        for r in range(rows_len):
            for t in col_titles:
                table_data.append(
                    {'text': str(contatos[t][r]), 'size_hint_y': None, 'height': 40, 'bcolor': (.06, .25, .25, 1)})

        self.ids.table_floor_layout.cols = self.columns
        self.ids.table_floor.data = table_data


class TelaLancamento(Screen):

    def on_enter(self):
        self.ids.msg.text = ""
        self.ids.txt_nome.text = ""
        self.ids.txt_email.text = ""
    
    def gravarDados(self):
        if (self.ids.txt_nome.text != "") and (self.ids.txt_email.text !=  ""):
            # Abrimos uma conexão com o banco de dados:
            conexao = pymysql.connect(host='SEU_HOST',
                                    db='SEU_DB',
                                    user='SEU_USER',
                                    passwd='SUA_PASS')

            # Cria um cursor:
            cursor = conexao.cursor()

            nome = self.ids.txt_nome.text
            email = self.ids.txt_email.text

            # construção da string SQL que insere um registro.
            sql = "INSERT INTO contato(nome,email) VALUES ('%s', '%s')" % (nome, email)

            try:
                # Execute o comando
                cursor.execute(sql)
                # Confirme a inserção na base de dados
                conexao.commit()
                msg = "Registro inserido com sucesso!"
                self.ids.txt_nome.text = ""
                self.ids.txt_email.text = ""

            except:
                # limpe tudo se algo saiu errado
                conexao.rollback()
                msg = "Erro na inserção de dados"

            # fecha a conexão
            conexao.close()
        else:
            msg = "Preencha todos os campos!"
        
        self.ids.msg.text = msg



####
####
#### Iniciar o Builder com o ScreenManager
####
####

Builder.load_file("kv/appcontatos.kv")


# Create the screen manager

sm = ScreenManager()
sm.add_widget(TelaPrincipal())
sm.add_widget(TelaLancamento())


class Contatos(App):

    def build(self):
        sm.current = "TelaPrincipal"
        return sm


if __name__ == '__main__':
    Janela = Contatos()
    Janela.title = "Gestor de Contatos"
    Janela.run()
