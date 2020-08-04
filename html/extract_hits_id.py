import re

id_mat = re.compile(r'Your HIT ID is: (.*)\n')

f = open('./first_public_hits.txt', 'r')
lines = f.readlines()
f.close()

hit_ids = []
for l in lines:
    match = id_mat.match(l)
    if match is not None:
        hit_ids.append(match[1] + '\n')

f = open('./first_public.txt', 'w')
f.writelines(hit_ids)
f.close()