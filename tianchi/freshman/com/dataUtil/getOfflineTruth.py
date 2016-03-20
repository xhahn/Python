def getTruthData(srcFile,dstFile):
    fw = open(dstFile, 'w')

    for line in open(srcFile):
        array = line.strip().split(',')
        if array[0] == 'user_id' or not array[2] == '4':
            continue
        fw.write('%s,%s\n' % (array[0], array[1]))
    fw.close()