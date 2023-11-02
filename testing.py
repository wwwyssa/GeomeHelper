import sqlite3
import random


def generate_questions(test_theme):
    name = 'geoma'
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
        questions = [[name, i[0]] for i in result]
    for i in range(len(questions)):
        elem = questions[i]
        task = elem[1]
        result = con.execute(
            f"""SELECT formula.formula FROM formula WHERE formula.formula_name = '{task}'""").fetchall()
        questions[i].append(result[0])

    con.close()
    print(questions)
    return questions


generate_questions('Трапеция')
