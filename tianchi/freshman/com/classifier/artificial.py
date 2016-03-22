#对ans中的user-item进行过滤
def userFilt(ans, filtB_dic):
    filt_dic = {}
    filt = set()

    for line in open("alldata.csv"):
        line = line.replace('\n', '')
        array = line.split(',')
        if not array[0] in filt_dic:
            filt_dic[array[0]] = [0, 0, 0, 0]
        filt_dic[array[0]][int(array[2])-1] += 1

    for user in filt_dic:
        if filt_dic[user][0] == 0:
            continue
        #1.该用户从没买过东西
        #2.该用户购买-浏览比太低
        if filt_dic[user][3] == 0 \
                or 1.0 * filt_dic[user][3] / filt_dic[user][0] < 0.01:
            filt.add(user)

    for uid in ans:
        if (uid[0], uid[1]) in filtB_dic:
            if filtB_dic[(uid[0], uid[1])] < uid[2]: #加入购物车之后,预测日之前,购买
                ans.remove(uid)
    return filt

def getData(rawDataPath,preDay):
    import csv

    buy = []
    trainData = []

    with open(rawDataPath, 'r') as rawData:
        reader = csv.DictReader(rawData)
        for row in reader:
            time = row['time'].split(' ')
            user = row['user_id']
            item = row['item_id']
            type = row['behavior_type']

            #将 yyyy-mm-dd 转换成从第一天开始的天数，第一天为2014-11-18，且11月18日，day为1
            if time[0].split('-')[1] == '12':
                day = 13 + int(time[0].split('-')[2])
            else:
                day = int(time[0].split('-')[2]) - 17

            if preDay - day > 3 or preDay - day < 0:  #三日之外的数据
                continue
            if preDay == day:  #预测日当天 get offline_groundtruth
                if type == '4':
                    buy.append((user, item))
            else: ##训练集
                uid = (user, item, (preDay - day)*24 - int(time[1]))  # calculate hours before the last day
                if type == '3':
                    trainData.append(uid)

    buy = set(buy)
    trainData = list(set(trainData))
    print('trainData length = ', len(trainData))
    return trainData, buy


def train(rawDataPath):

    top_all = [0.0 for i in range(72)]
    for preDay in range(4,31):  ##循环27次，从11月18日开始，到12月17日

        trainData, buy = getData(rawDataPath, preDay)
        trainData_dic = {}

        for uid in trainData:
            time = uid[2]
            if time in trainData_dic:
                trainData_dic[time].append((uid[0], uid[1]))
            else:
                trainData_dic[time] = [(uid[0], uid[1])]

        count_buy = [0 for i in range(72)]

        for i in range(72):
            key = i+1
            if not key in trainData_dic:
                continue
            for ui in trainData_dic[key]:
                if ui in buy:
                    count_buy[key-1] += 1
                    buy.remove(ui)
        print('count_buy', count_buy)

        prob = [0.0 for i in range(72)]
        for i in range(72):
            if not i+1 in trainData_dic:
                continue
            prob[i] = 1.0 * count_buy[i] / len(trainData_dic[i+1])

        print('prob', prob)

        for i in range(72):
            top_all[i] += prob[i]

    sort = [i+1 for i in range(72)]  #begin with 1
    sort = sorted(zip(sort, top_all), key=lambda x:x[1], reverse=True)

    for i in range(10):print(sort[i])
    top = set(x[0] for x in sort[0:22])  #get the top k time

    print(top)

    return top

def predict(top, predictData, answer):
    offline_offline_candidate_data = []
    filtB_dic = {}
    for line in open(predictData):
        line = line.replace('\n', '')
        array = line.split(',')
        if array[0] == 'user_id':
            continue

        time = array[-1].strip().split(' ')
        uid = (array[0], array[1], (day - int(time[0].split('-')[2]))*24 - int(time[1]))  # calculate hours before the last day

        if array[2] == '3':
            offline_offline_candidate_data.append(uid)
        if array[2] == '4':
            if (uid[0], uid[1]) in filtB_dic:
                if filtB_dic[(uid[0], uid[1])] > uid[2]:
                    filtB_dic[(uid[0], uid[1])] = uid[2]
            else:
                filtB_dic[(uid[0], uid[1])] = uid[2]

    offline_offline_candidate_data = list(set(offline_offline_candidate_data))

    ans = []

    for uid in offline_offline_candidate_data:
        if uid[2] in top:
            ans.append(uid)
    ans = list(set(ans))

    filt = userFilt(ans, filtB_dic)

    wf = open(answer, 'w')
    wf.write('user_id,item_id\n')
    i = 0
    for uid in ans:
        if not uid[0] in filt:
            wf.write('%s,%s\n' % (uid[0], uid[1]))
        else:
            i += 1
    print(i)
    wf.close()

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('trainData', type = str)
	parser.add_argument('predictData', type = str)
	parser.add_argument('answer', type = str)
	args = vars(parser.parse_args())
    
	top = train(args['trainData']

    predict(top, args['predictData'], args['answer'])

	
main()


