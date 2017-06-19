outfile = open('ips_train.csv','w')
outfile.write("predictor,date,time,logid,type,subtype,level,vd,srcip,srcport,dstip,dstport,sessionid,proto");

with open("ips_20161201_xgb.txt") as f:
    for line in f.readlines():
        
