import sqlite3 as sl


def read() -> list:
    con = sl.connect('lol.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM static")
        rows = cur.fetchall()

        stat = []
        for row in rows:
            stat.append(list(row))
    return stat


def _delete() -> None:
    con = sl.connect('lol.db')
    print('Действие приведет к ПОЛНОЙ ОЧИСТКЕ БД!!!')
    print('Для подтверждения введите УДАЛИТЬ')
    if str(input()) == 'УДАЛИТЬ':
        cur = con.cursor()
        sql = """DELETE from static"""
        cur.execute(sql)
        con.commit()
        print('Удаление успешно')
        cur.close()

        with con:
            con.executemany(
                'INSERT INTO static (ch, k, d, a, rank, arank, res, time, cs, dmg, tdmg, gold, vis) '
                'values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                [tuple(['Чемпион', 'Результат игры', 'Убийства', 'Смерти', 'Содействия',
                        'Ранг оппонента', 'Средний ранг игроков', 'Продолжительность игры',
                        'Миньоны', 'Урон по чемпионам', 'Урон по башням',
                        'Заработанное золото', 'Обзор'])])


def add(data: list) -> None:
    con = sl.connect('lol.db')
    with con:
        con.executemany('INSERT INTO static (ch, k, d, a, rank, arank, res, time, cs, dmg, tdmg, gold, vis) '
                        'values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [tuple(data[1])])
