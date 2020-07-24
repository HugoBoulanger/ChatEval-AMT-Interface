import csv
import os
import random


def read_csv(path, with_header=False):
    with open(path, newline='') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
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
    return rows_per_dialog


def format_validity(sce_path, dst_path, nb_annot_per_hit=3):
    sce_rows = read_csv(sce_path, with_header=True)
    rows_per_dialog = get_rows_per_dialog(sce_rows)

    validity_rows = []
    for turns in rows_per_dialog:
        for i in range(1, len(turns)):
            validity_row = [''] + ['[empty line]'] * 4
            validity_row[0] = turns[i][0]
            for j in range(min(i+1, 4)):
                validity_row[-(1+j)] = turns[i-j][2]
            validity_rows.append(validity_row)

    headers = []
    for i in range(nb_annot_per_hit):
        headers.extend([f'NUMBER_{i+1}', f'DIALOG_{i+1}_1', f'DIALOG_{i+1}_2', f'DIALOG_1_3', f'DIALOG_{i+1}_4'])
    dst_rows = [headers]
    # dst_rows = [['NUMBER_1', 'DIALOG_1_1', 'DIALOG_1_2', 'DIALOG_1_3', 'DIALOG_1_4',
    #              'NUMBER_2', 'DIALOG_2_1', 'DIALOG_2_2', 'DIALOG_2_3', 'DIALOG_2_4',
    #              'NUMBER_3', 'DIALOG_3_1', 'DIALOG_3_2', 'DIALOG_3_3', 'DIALOG_3_4']]

    random.shuffle(validity_rows)
    nb_hits = len(validity_rows) // nb_annot_per_hit + (1 if len(validity_rows) % nb_annot_per_hit != 0 else 0)
    for i in range(nb_hits):
        dst_row = []
        for j in range(i, min(len(validity_rows), i+3)):
            dst_row.extend(validity_rows[j])
        dst_rows.append(dst_row)

    write_csv(dst_path, dst_rows)


if __name__ == '__main__':
    random.seed(1)

    dir = os.path.dirname(os.path.abspath(__file__))
    sce = os.path.join(dir, 'topical_sample.csv')
    dst = os.path.join(dir, 'topical_sample_amt_validity.csv')
    format_validity(sce, dst)
