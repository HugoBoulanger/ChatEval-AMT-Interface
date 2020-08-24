import csv
import os
import random
import numpy as np


def read_csv(path, with_header=False):
    with open(path, newline='', encoding='utf8') as f:
        reader = csv.reader(f)
        # rows = [row for row in reader]
        rows = []
        try:
            for r in reader:
                rows.append(r)
        except UnicodeDecodeError as err:
            print(f'{err}\n last row = {rows[-1]}')
    if with_header:
        rows = rows[1:]
    return rows


def write_csv(path, rows):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def get_rows_per_dialog(rows):
    rows_per_dialog = []
    d_uid = '-'.join(rows[0][0].split('-')[:2])
    d_current = []
    for r in rows:
        d_uid_current = '-'.join(r[0].split('-')[:2])
        if d_uid == d_uid_current:
            d_current.append(r)
        else:
            rows_per_dialog.append(d_current)
            d_current = [r]
            d_uid = d_uid_current
    rows_per_dialog.append(d_current)
    return rows_per_dialog


def get_dialogue_segments(rows_per_dialog, nb_context_turn):
    dialogue_segments = []
    for turns in rows_per_dialog:
        for i in range(1, len(turns)):
            segment = [turns[i][0]] + ['[empty line]'] * nb_context_turn
            for j in range(min(i+1, nb_context_turn)):
                segment[-(1+j)] = turns[i-j][2]
            dialogue_segments.append(segment)
    return dialogue_segments


def get_attention_check(rows_per_dialog, nb_context_turn):
    indexes = random.sample(list(range(len(rows_per_dialog))), 2)
    t1 = rows_per_dialog[indexes[0]][random.randint(0, len(rows_per_dialog[indexes[0]]) - 1)][2]
    t2 = rows_per_dialog[indexes[1]][random.randint(0, len(rows_per_dialog[indexes[1]]) - 1)][2]
    return ['[attention check]'] + ['[empty line]'] * (nb_context_turn - 2) + [t1, t2]


def format_validity(sce_path, dst_dir_path, nb_context_turn=4, nb_annot_per_hit=3, attention_check='default'):
    print(f'--- {sce_path} ---')
    sce_rows = read_csv(sce_path, with_header=True)
    rows_per_dialog = get_rows_per_dialog(sce_rows)
    print(f'nb of dialogues = {len(rows_per_dialog)}')
    # print(f'nb of turns to annotate expected = {len(sce_rows) - len(rows_per_dialog)}')

    validity_rows = get_dialogue_segments(rows_per_dialog, nb_context_turn)
    print(f'nb of turns to annotate = {len(validity_rows)}')

    headers = []
    for i in range(nb_annot_per_hit + (1 if attention_check == 'random_turns' else 0)):
        headers.append(f'NUMBER_{i + 1}')
        for j in range(nb_context_turn):
            headers.append(f'DIALOG_{i + 1}_{j + 1}')
    dst_rows = [headers]

    nb_hits = len(validity_rows) // nb_annot_per_hit + (1 if len(validity_rows) % nb_annot_per_hit != 0 else 0)
    # print(f'nb of hits expected = {nb_hits}')
    if attention_check == 'random_turns':
        for i in range(nb_annot_per_hit - len(validity_rows) % nb_annot_per_hit):
            validity_rows.append(get_attention_check(rows_per_dialog, nb_context_turn))
        if len(validity_rows) % nb_annot_per_hit != 0:
            return
    random.shuffle(validity_rows)
    for i in range(nb_hits):
        j_min = i * nb_annot_per_hit
        j_max = min(len(validity_rows), j_min + nb_annot_per_hit)
        dst_row = []
        for j in range(j_min, j_max):
            dst_row.append(validity_rows[j])
        if attention_check == 'default':
            for j in range(j_max, j_min + nb_annot_per_hit):
                dst_row.append(['None', '[empty line]', '[empty line]', '[empty line]', 'Please select valid.'])
        if attention_check == 'random_turns':
            dst_row.append(get_attention_check(rows_per_dialog, nb_context_turn))
        random.shuffle(dst_row)
        dst_row_flat = []
        for segment in dst_row:
            dst_row_flat.extend(segment)
        dst_rows.append(dst_row_flat)

    print(f'nb of hits = {len(dst_rows) - 1}')

    dst_path = os.path.join(dst_dir_path,
                            os.path.basename(sce_path).replace('.csv', f'_amt_validity_context_{nb_context_turn}_nb_annot_{nb_annot_per_hit}.csv'))
    write_csv(dst_path, dst_rows)


def sample_turns(sce_path, nb_turns, dst_dir_path):
    sce_rows = read_csv(sce_path, with_header=False)

    dst_rows = [sce_rows[0]]
    d_uid = '-'.join(sce_rows[0][0].split('-')[:2])
    nb_conv = 0
    for r in sce_rows[1:]:
        d_uid_current = '-'.join(r[0].split('-')[:2])
        if d_uid == d_uid_current:
            dst_rows.append(r)
        else:
            if len(dst_rows) >= nb_turns:
                break
            dst_rows.append(r)
            d_uid = d_uid_current
            nb_conv += 1

    dst_path = os.path.join(dst_dir_path,
                            os.path.basename(sce_path).replace('.csv',
                                                               f'_sample_{len(dst_rows)-1}_turns_{nb_conv}_conv.csv'))
    write_csv(dst_path, dst_rows)


if __name__ == '__main__':
    random.seed(1)

    # dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data')
    #
    # sce = os.path.join(dir, 'topical_sample.csv')
    # format_validity(sce, dir, nb_context_turn=4, nb_annot_per_hit=10, attention_check='random_turns')
    #
    # sce = os.path.join(dir, 'empathy_sample.csv')
    # format_validity(sce, dir, nb_context_turn=4, nb_annot_per_hit=10, attention_check='random_turns')

    dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                       'data')

    sce = os.path.join(dir, 'topical_main.csv')
    sample_turns(sce, 500, dir)

    sce = os.path.join(dir, 'MPATHY_main.csv')
    sample_turns(sce, 500, dir)
