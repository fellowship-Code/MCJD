import sqlite3

connection = sqlite3.connect('data/index.db')
cursor = connection.cursor()

categories_en = None
categories_fr = None


def category_en():
    global cursor
    global categories_en
    
    if categories_en != None:
        return categories_en
    
    cursor.execute("select distinct category from subject_en order by category")
    categories_en = []
    for row in cursor.fetchall():
        categories_en.append(row[0])
    return categories_en

def category_fr():
    global cursor
    global categories_fr
    
    if categories_fr != None:
        return categories_fr
    
    cursor.execute("select distinct category_fr from subject_fr order by category_fr")
    categories_fr = []
    for row in cursor.fetchall():
        categories_fr.append(row[0])
    return categories_fr


def english_search(category, subject, text):    
    if category == "All categories":
        if (subject == "" or subject == "*") and text != "*" and text != "":                                    
            return search_term_en(text)
        elif text != "*" and text != "":
            return search_subject_en(subject, text)
    elif (subject == "" or subject == "*") and text != "*" and text != "":
        return search_all(category, None, text)
    elif text != "*" and text != "":
        return search_all(category, subject, text)
    
def french_search(category, subject, text):
    if category == "Toutes categoriés":
        if (subject == "" or subject == "*") and text != "*" and text != "":
            search_fr(text)
        elif text != "*" and text != "":
            search_fr(subject, text)
    elif (subject == "" or subject == "*") and text != "*" and text != "":
        search_fr(category, None, text)
    elif text != "*" and text != "":
        search_fr(category, subject, text)


def search_term_en(text):    
    global categories_en
    
    param = (text + '%',)
    resultset = []

    for category in categories_en:
        curr_category = category.replace(' ', '')
        dbstring = 'data/dict_en/' + curr_category + '.db'        
        dbconn = sqlite3.connect(dbstring)
        dbcursor = dbconn.cursor()
        dbcursor.execute("select * from " + curr_category + " where TERM_EN like ?", param)
        rows = dbcursor.fetchall()
        dbconn.close()
        
        for i in range(len(rows)):
            resultset.append((category,) + rows[i])
        if len(resultset) > 15:
            return resultset
    return resultset

def search_subject_en(subject, text):
    global categories_en
    
    param = (subject + '%', text + '%',)
    resultset = []
    for category in categories_en:
        curr_category = category.replace(' ', '')
        dbstring = 'data/dict_en/' + curr_category + '.db'
        dbconn = sqlite3.connect(dbstring)
        dbcursor = dbconn.cursor()
        rows = dbcursor.execute("select * from " + curr_category + " where subject_en like ? and term_en like ?", param).fetchall()
        dbconn.close()
        for i in range(len(rows)):
            resultset.append((category,) + rows[i])
        if len(resultset) > 15:
            return resultset
    return resultset

def search_all(category, subject, text):
    global categories_en
    
    if subject == '' or subject == '*' or subject is None:
        subject = ''
    
    param = (subject + '%', text + '%')
    resultset = []    
    dbstring = 'data/dict_en/' + categoryreplace(' ', '') + '.db'
    dbconn = sqlite3.connect(dbstring)
    dbcursor = dbconn.cursor()        
    rows = dbcursor.execute("select * from " + category.replace(' ', '') + " where SUBJECT_EN like ? and TERM_EN like ?", param).fetchall()
    dbconn.close()
    for i in range(len(rows)):
        resultset.append((category,) + rows[i])
        if len(resultset) > 15:
            return resultset
    return resultset

def search_fr(text):
    pass

def search_fr(subject, text):
    pass

def search_fr(category, subject, text):
    pass
