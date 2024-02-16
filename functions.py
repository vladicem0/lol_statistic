import datetime
import matplotlib.pyplot as plt
from riotwatcher import LolWatcher, ApiError
from database import read, add


def number_converting(rmn_num: str) -> str:
    ranks = {
        'I': '1',
        'II': '2',
        'III': '3',
        'IV': '4'
    }
    return ranks[rmn_num]


def in_rank(rank: str) -> int:
    match rank[0].lower():
        case 'i':
            rank = 5 - int(rank[1])
        case 'b':
            rank = 9 - int(rank[1])
        case 's':
            rank = 13 - int(rank[1])
        case 'g':
            rank = 17 - int(rank[1])
        case 'p':
            rank = 21 - int(rank[1])
        case 'e':
            rank = 25 - int(rank[1])
        case 'd':
            rank = 29 - int(rank[1])
        case 'm':
            rank = 30 - int(rank[1:])
        case 'g':
            rank = 31 - int(rank[1:])
        case 'c':
            rank = 32 - int(rank[1:])
        case _:
            quit(-1)
    return rank


def out_rank(rank: int) -> str:
    if rank < 5:
        rank = 'i' + str(5 - int(rank))
    elif rank < 9:
        rank = 'b' + str(9 - int(rank))
    elif rank < 13:
        rank = 's' + str(13 - int(rank))
    elif rank < 17:
        rank = 'g' + str(17 - int(rank))
    elif rank < 21:
        rank = 'p' + str(21 - int(rank))
    elif rank < 25:
        rank = 'e' + str(25 - int(rank))
    elif rank < 29:
        rank = 'd' + str(29 - int(rank))
    elif rank < 30:
        rank = 'm' + str(30 - int(rank))
    elif rank < 31:
        rank = 'g' + str(31 - int(rank))
    else:
        rank = 'c' + str(32 - int(rank))
    return rank


def struct_help() -> None:
    stat = read()
    print('\n'.join(stat[0]))


def game() -> None:
    api_key = ''  # Персональный ключ api (меняется ежедневно)
    watcher = LolWatcher(api_key)
    region = ''
    name = ''
    riot_id = watcher.summoner.by_name(region, name)
    ranked = watcher.league.by_summoner(region, riot_id['id'])
    print(ranked)
    match_detail = watcher.match.matchlist_by_puuid(region, riot_id['puuid'])
    pt = watcher.league.by_summoner(region, riot_id['id'])
    participants = watcher.match.by_id(region, match_detail[0])['info']['participants']
    ranks, data, count, role = [], [], 0, ''

    for i in range(10):
        if participants[i]['summonerName'] == name:
            participant = participants[i]
            role = participant['role']
            for k, v in participant.items():
                print(k, v)
            data = [[participant['championName'], int(participant['win']), participant['kills'],
                    participant['deaths'], participant['assists'], 'opponent`s rank', 'average rank',
                    participant['timePlayed']//60, participant['totalMinionsKilled'],
                    participant['totalDamageDealtToChampions'], participant['damageDealtToTurrets'],
                    participant['goldEarned'], participant['visionScore']], [i for i in range(13)]]
            print(data)
        else:
            rank = watcher.league.by_summoner(region, watcher.summoner.by_name(region,
                                                                               participants[i]['summonerName'])['id'])
            if len(rank) != 0:
                for j in range(len(rank)):
                    if rank[j]['queueType'] == 'RANKED_SOLO_5x5':
                        ranks.append(rank[j]['tier'][0] + number_converting(rank[j]['rank']))
                        count += 1
    data[0][6] = 0
    #for i in range(10):
    #    if participants[i]['role'] == role and participants[i]['summonerName'] != name:
    #        data[5] = watcher.league.by_summoner(region, watcher.summoner.by_name(region, participants[i]['summonerName'])['id'])
    #add(data)


def statistic(ch: str = None) -> None:
    if not ch:
        ch = []  # Статистика по умолчанию
    else:
        ch = list(ch.split())

    stat = read()

    for i in range(len(ch)):
        data = [["Винрейт:", "Убийства:", "Смерти:", "Содействия:", "Продолжительность игр:", "Миньоны:",
                 "Урон по чемпионам:", "Урон по башням:", "Среднее золото:", "Средний обзор:"],
                [0 for _ in range(10)]]
        stats, ch_count = [], 0
        for j in range(len(stat) - 1):
            stats.append(stat[j + 1][:5] + stat[j + 1][7:])

        for j in range(len(stats)):
            if stats[j][0] == ch[i]:
                ch_count += 1
                for k in range(10):
                    data[1][k] += int(stats[j][k + 1])

        print(f'Статистика ранговых игр на чемпионе {ch[i]}:')
        if ch_count > 0:
            print(f'Количество игр: {ch_count}')
            print(f'{data[0][0]} {round(int(data[1][0]) / ch_count * 100)[:5], 2}%')
            for j in range(9):
                data[1][j + 1] /= ch_count
                print(data[0][j + 1], round(int(data[1][j + 1], 2)))
        else:
            print('Нет игр на заданном чемпионе')
        print()


def wr() -> None:
    stat = read()
    stats, ch = [], {}
    for i in range(len(stat) - 1):
        stats.append(stat[i + 1][:2])

    for i in range(len(stats)):
        if stats[i][0] in ch.keys():
            ch[stats[i][0]][0] += 1
            ch[stats[i][0]][1] += int(stats[i][1])
        else:
            ch[stats[i][0]] = [1, int(stats[i][1])]

    for key in ch:
        print(f'Чемпион {key} имеет винрейт {str(ch[key][1] / ch[key][0] * 100)[:5]}% за {ch[key][0]} игр')


def t_win(ch: str = 'all') -> None:
    stat = read()
    time = {15: 0, 20: 0, 25: 0, 30: 0, 35: 0, 40: 0}
    stats, time_range = [], [0 for _ in range(6)]
    for i in range(len(stat) - 1):
        if stat[i][0] == ch or ch == 'all':
            stats.append(stat[i + 1][1:2] + stat[i + 1][7:8])

    for i in range(len(stats)):
        for j in range(6):
            if int(stats[i][1]) <= 17 + j * 5:
                time[15 + j * 5] += int(stats[i][0])
                time_range[j] += 1
                stats[i][1] = 50
    for i in range(6):
        time[15 + i * 5] /= time_range[i] / 100

    t = [15, 20, 25, 30, 35,
         40]  # Фактическое значение для каждой шкалы равно [t-2:t+2], т.е. t=20 = 18-22 включительно
    plt.title(f'Зависимость винрейта от времени для чемпиона {ch}')
    plt.xlabel("Время")
    plt.ylabel("Частота побед (%)")
    plt.grid()
    plt.plot(t, [time[i] for i in t])
    plt.show()


def log() -> None:
    f = open('log.txt', 'r+')
    last = (f.readlines()[sum(1 for _ in open('log.txt', 'r')) - 4]).split()[2:4]
    f.write(datetime.datetime.today().strftime('%d.%m.%Y') + '\n')
    f.write(f'Количество игр: {str(input())}\n')
    rnk, lp = map(str, input().split())
    f.write(f'Текущее эло: {rnk} {lp} лп\n')
    f.write(f'Разница лп: {(in_rank(rnk) - 9) * 100 + int(lp) - (in_rank(last[0]) - 9) * 100 - int(last[1])}\n\n\n')
    f.close()
