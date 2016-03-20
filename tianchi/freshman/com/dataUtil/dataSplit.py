def dataSplit(srcFile, dstFile, featIndex, featVal):

    fr = open("tianchi_fresh_comp_train_item.csv")
    item = []
    for line in fr.readlines():
        i = line.strip().split(',')[0]
        if i == 'item_id':
            continue
        item.append(i)
    item = set(item)

    fsrc = open(srcFile,'r')
    content = fsrc.readlines()
    fsrc.close()
    fwd = open(dstFile, 'w')
    fws = open(srcFile, 'w')

    for line in content:
        temp = line.strip().split(',')
        if not temp[1] in item:
            print("delete")
            continue
        if temp[featIndex] > featVal:
            fwd.write(line)
        else:
            fws.write(line)
    fwd.close()
    fws.close()


