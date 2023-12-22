import sqlite3
import random


def generate_questions(test_theme):
    name = 'geoma_db'
    con = sqlite3.connect(name)
    questions = []
    if test_theme == 'Все':
        all_id = [1, 2, 3, 4, 5]
        random.shuffle(all_id)
        for idx in all_id:
            result = con.execute(f"""SELECT formula.formula_name FROM formula
            WHERE formula.shape_id = (SELECT id FROM shape WHERE id = '{idx}')""").fetchall()
            name = con.execute(f"""SELECT name FROM SHAPE WHERE id = {idx}""").fetchall()
            rand_idx = random.randint(0, 4)
            questions.append([name[0][0], result[rand_idx][0]])
    else:
        result = con.execute(f"""SELECT formula.formula_name FROM formula
            WHERE formula.shape_id = (SELECT id FROM shape WHERE name = '{test_theme}')""").fetchall()
        name = test_theme
        random.shuffle(result)
        questions = [[name, i[0]] for i in result]
    for i in range(len(questions)):
        elem = questions[i]
        task = elem[1]
        result = con.execute(
            f"""SELECT formula.formula FROM formula WHERE formula.formula_name = '{task}'""").fetchall()
        result = result[0][0]
        result = result.replace(' ', '')
        questions[i].append(result)

    con.close()
    return questions
    # фигура, название формулы, формула


def check_results(user_answer, questions):
    kol = 0
    right_answer = list()
    user = list()
    diff = list()
    for i in range(len(questions)):
        tmp = questions[i][2]
        tmp = [i for i in tmp]
        tmp.sort()
        right_answer.append(''.join(tmp))
    for i in range(len(user_answer)):
        tmp = user_answer[i]
        tmp = [i for i in tmp]
        tmp.sort()
        user.append(''.join(tmp))
    for i in range(len(user_answer)):
        if user[i] == right_answer[i]:
            kol += 1
        else:
            diff.append((user_answer[i], questions[i][2]))
    return kol, diff


def update_db(theme, name, result):
    name_db = 'geoma_db'
    con = sqlite3.connect(name_db)
    cur = con.cursor()
    f = True
    tmp = con.execute(f"""SELECT name FROM results WHERE name = '{name}'""").fetchall()
    if len(tmp) == 0 or name not in tmp[0]:
        query = f"""INSERT INTO results(theme, name, result) VALUES ('{theme}', '{name}', {result})"""
        res = cur.execute(query)
        f = False
    else:
        tmp = con.execute(f"""SELECT result, theme FROM results WHERE name = '{name}'""").fetchall()
        for e in tmp:
            if theme in e:
                f = False
                if e[0] < result:
                    query = f"""UPDATE results SET result = {result} WHERE name = '{name}' AND theme = '{theme}'"""
                    res = cur.execute(query)
                break
    if f:
        query = f"""INSERT INTO results(theme, name, result) VALUES ('{theme}', '{name}', {result})"""
        res = cur.execute(query)
    con.commit()

