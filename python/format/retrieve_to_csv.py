import pickle as pkl
from xml.etree import ElementTree
import csv
import re

number = re.compile(r'NUMBER_([0-9]*)')
answer = re.compile(r'ANSWER_([0-9]*)')

def convert(path_pkl, path_out):

    pik = pkl.load(open(path_pkl, 'rb'))
    #print(pik)
    with open(path_out, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        column_names = ['UID', 'ANSWER', 'ANNOTATOR']
        spamwriter.writerow(column_names)
        for hit in pik:
            comments = []
            hit_id = None
            for assign in hit['Assignments']:
                hit_id = assign['HITId']
                worker = assign['WorkerId']
                root = ElementTree.fromstring(assign['Answer'])
                lis = {}
                for i in range(len(root)):
                    l = []
                    for j in range(len(root[i])):
                        l.append(root[i][j].text)
                    match_n = number.match(l[0])
                    if match_n is not None:
                        if match_n[1] in lis.keys():
                            lis[match_n[1]][0] = l[1]
                        else:
                            lis[match_n[1]] = [l[1], '', worker]
                    else:
                        match_a = answer.match(l[0])
                        if match_a is not None:
                            if match_a[1] in lis.keys():
                                lis[match_a[1]][1] = l[1]
                            else:
                                lis[match_a[1]] = ['', l[1], worker]
                        else:
                            if l[0] == 'comment':
                                comments.append(f"{worker}, {l[1]}\n")
                print(lis)
                for k, v in lis.items():
                    spamwriter.writerow(v)
            if hit_id is not None:
                f = open(f"comments_{hit_id}.txt", 'w')
                f.writelines(comments)
                f.close()




if __name__ == '__main__':

    convert('../../html/amt_hit_responses.pkl', './test.csv')