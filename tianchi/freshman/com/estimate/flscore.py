st = open("F:\\acm\\pycharm\\project\\tianchi\\freshman\\source\\offline_groundtruth.csv")
answer = []

for ans in st.readlines():
    answer.append(ans)
answer = set(answer)

you = []
for y in open("F:\\acm\\pycharm\\project\\tianchi\\freshman\\source\\ans.csv"):
    if y[0] == 'u':
        continue
    you.append(y)
you = set(you)

inter = answer & you

print(len(answer), len(you), len(inter))

print('hit number =', len(inter))
if len(inter) > 0:
    a = len(answer)
    b = len(you)
    c = len(inter)
    R = 1.0 * c / a * 100
    P = 1.0 * c / b * 100
    F1 = 2.0 * R * P / (R + P)
    print('F1/P/R %.2f%%/%.2f%%/%.2f%%\n' % (F1, P, R))
