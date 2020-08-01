import csv
from nltk.metrics.agreement import AnnotationTask


def read_csv(path):
    with open(path, newline='', encoding='utf8') as f:
        reader = csv.DictReader(f)
        # rows = [row for row in reader]
        rows = []
        try:
            for r in reader:
                rows.append(r)
        except UnicodeDecodeError as err:
            print(f'{err}\n last row = {rows[-1]}')
    return rows


def update_dict(d, key, elt):
    if key in d:
        d[key].append(elt)
    else:
        d[key] = [elt]


def get_annotations_old(rows, nb_turns_per_hit):
    annotations = {}
    for r in rows:
        for i in range(nb_turns_per_hit):
            hit_id = r['HITId']
            uid = r[f'Input.NUMBER_{i+1}']
            id = f'{uid}_{hit_id}'
            rating = r[f'Answer.ANSWER_{i+1}']
            if id in annotations:
                annotations[id].append(rating)
            else:
                annotations[id] = [rating]
    return annotations


def get_annotations(rows, nb_turns_per_hit):
    if nb_turns_per_hit != 1:
        return get_annotations_old(rows, nb_turns_per_hit)
    annotations = {}
    for r in rows:
        uid = r['UID']
        rating = r['ANSWER']
        if uid in annotations:
            annotations[uid].append(rating)
        else:
            annotations[uid] = [rating]
    return annotations


def annotations2task_data(annotations, nb_annotators):
    data = [[] for _ in range(nb_annotators)]
    for id, ratings in annotations.items():
        if len(ratings) != nb_annotators:
            # print(f'Not enough ratings for {id}, required: {nb_annotators}, actual: {len(ratings)}')
            continue
        for i in range(nb_annotators):
            data[i].append(ratings[i])
    # print(data)

    task_data = []
    for i in range(len(data)):
        task_data.extend([str(i), str(j), str(data[i][j])] for j in range(len(data[i])))

    return task_data


def compute_agreement(sce_path, nb_turns_per_hit, nb_annotators):
    rows = read_csv(sce_path)
    annotations = get_annotations(rows, nb_turns_per_hit)
    # print(annotations)
    task_data = annotations2task_data(annotations, nb_annotators)
    # print(task_data)

    rating_task = AnnotationTask(data=task_data)
    print(f"Cohen's Kappa: {rating_task.kappa()}")
    print(f"Fleiss' Kappa: {rating_task.multi_kappa()}")


if __name__ == '__main__':
    sce = "C:\\Users\\veron\\Documents\\jsalt\\amt_test\\validity_test_HB\\Batch_288079_batch_results.csv"
    compute_agreement(sce, nb_turns_per_hit=3, nb_annotators=4)