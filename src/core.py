#!/user/bin/python3
# -*- coding: utf-8 -*-

"""
This module customizes the user interface and defines
the control flow of the Mincover program
"""

import os
import re
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication
from PyQt5.QtWidgets import QMainWindow, QDialog, QFileDialog
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore

from view.dictionary import Ui_Dictionary
import database

__all__ = ["UI"]


_translate = QtCore.QCoreApplication.translate


class UI(QMainWindow):
    """
    The UI class is the delegate of QMainWindow. It is the interface
    between the main application and the user interface
    """
    def __init__(self):
        super(UI, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_Dictionary()
        self.ui.setupUi(self)

        self.index = 0
        self.current_results = []
        
        self.init_ui()                
        self.show()

    def init_ui(self):
        """Initialize and define properties of the main window"""
        self.resultset = []
        self.populate_en()        
        self.set_callbacks()
        #self.setGeometry(300, 100, 450, 620)
        #self.setWindowTitle('Jargon Dictionary')
        #self.setWindowIcon(QIcon('icon.png'))
                

    ###################     Callbacks   ###################

    def set_callbacks(self):
        self.ui.preflang.currentIndexChanged.connect(self.set_language)        
        self.ui.btn_search.clicked.connect(self.search)
        self.ui.btn_next.clicked.connect(self.next_page)
        self.ui.btn_prev.clicked.connect(self.prev_page)
        

    def search(self):
        category = self.ui.category.currentText()
        subject = self.ui.subject.text().strip()
        term = self.ui.term.text().strip()
        lang = self.ui.preflang.currentText()

        result = []
        if lang == "EN":
            self.result = database.english_search(category, subject, term)
        else:
            self.result = database.french_search(category, subject, term)
        
        #self.update_content(result)
        self.index = 0
        self.update_content()        
        return

    def set_language(self):
        lang = self.ui.preflang.currentText()
        if lang == "EN":
            self.populate_en()
            self.ui.btn_category.setText("Category")
            self.ui.btn_subject.setText("Subject")
            self.ui.btn_term.setText("Term")
        else:
            self.populate_fr()
            self.ui.btn_category.setText("Categorié")
            self.ui.btn_subject.setText("Sujet")
            self.ui.btn_term.setText("Term")

    ###################     Update   ###################

    def populate_en(self):
        category_list = database.category_en()

        for i in range(self.ui.category.count() - 1, -1, -1):
            self.ui.category.removeItem(i)
        
        self.ui.category.addItem(QIcon(), "All categories")
        for text in category_list:
            self.ui.category.addItem(QIcon(), text)

    def populate_fr(self):
        category_list = database.category_fr()
        
        for i in range(self.ui.category.count() - 1, -1, -1):
            self.ui.category.removeItem(i)        
        
        self.ui.category.addItem(QIcon(), "Toutes categoriés")
        for text in category_list:
            self.ui.category.addItem(QIcon(), text)

    def update_content(self):
        
        if self.result == [] or len(self.result) == 0 or self.result == None:
            self.ui.content.setHtml("<b>No results. Please search for a new term or increase the scope of your search<b>")
            return
        
        self.ui.summary.setHtml('''
<dl>
    <dt><b>Category:<b></dt>
    <dd>{0}</dd>
    <dt><b>Subject:<b></dt>
    <dd>{1}</dd>
    <dt><b>Term:<b></dt>
    <dd>{2}</dd>
    <dt><b>Abbreviations:<b></dt>
    <dd>{3}</dd>
    <dt><b>Synonyms:<b></dt>
    <dd>{4}</dd>
</dl>
        '''.format(self.result[self.index][0], self.result[self.index][1], self.result[self.index][2], self.result[self.index][4],self.result[self.index][6].replace(';', '<br>')))
        
        content_string = '''
<dl>
'''
        
        for text in self.result[self.index][8:]:
            if text is None:
                continue
            content_string += "<dt><b>" + text.split(": ",1)[0] + "<b></dt>"
            content_string += "<dd>" + text.split(": ",1)[1] + "<dd>"
        content_string += "</dl>"
        self.ui.content.setHtml(content_string)


    def next_page(self):
        if self.index < len(self.result) - 1:
            self.index += 1
            self.update_content()

    def prev_page(self):
        if self.index > 0:
            self.index -= 1
            self.update_content()
