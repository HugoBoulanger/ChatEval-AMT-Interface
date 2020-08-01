import boto3
import argparse
import sys
import re
from html_gen import *
import random

sys.path.append('../python/utils')
sys.path.append('../python/format')
import utils
from format import *
from task_dictionaries import *


def make_dialogs(path_to_csv):
    rows = read_csv(path_to_csv)
    hed = rows[0]
    rows = rows[1:]
    for i in range(len(hed)):
        hed[i] = hed[i].strip(';')
    seg = hed.index('SEG')
    uid = hed.index('UID')
    for i in range(len(rows)):
        rows[i] = [rows[i][uid], rows[i][seg].strip(';')]
    dialogs = get_rows_per_dialog(rows)
    return dialogs

def make_segments(dialogs, window, min_size=2):
    min_size = min(min_size, window)

    segments = []
    for d in dialogs:
        for i in range(min_size, len(d)):
            segments.append((d[i][0], [d[j][1] for j in range(max(0, i - window + 1), i + 1)]))

    rand = random.Random()
    rand.seed(a=1)
    rand.shuffle(segments)

    return segments


def add_attention_checks(segments, n):
    rand = random.Random()
    rand.seed(a=1)

    new_segments = []
    i = 0

    while i < len(segments):
        batch = segments[i: min(i + n, len(segments))]
        attention = ("ATTENTION-CHECK", rand.choice(segments)[1])
        attention[1][-1] = rand.choice(segments)[1][-1]
        batch.append(attention)
        rand.shuffle(batch)
        new_segments.extend(batch)
        i += n - 1

    return new_segments


def create_HIT(hit_description, hit_id, mturk, path_instructions, dialogs, task, sandbox=False, qualification=False):
    question_html_value = generate_html_filled(path_instructions, 
                                               generate_n_questions_filled(
                                                   '<u>Read</u> the context sentences then <u>rate</u> the last sentence.',
                                                   task_question_dictionary[task],
                                                   task_answer_dictionary[task],
                                                   dialogs,
                                                   task_warning_dictionary[task]),
                                                dialogs)

    question_html_value = question_html_value.encode('ascii', 'xmlcharrefreplace').decode()
    try:
        # These parameters define the HIT that will be created
        # question is what we defined above
        # max_assignments is the # of unique Workers you're requesting
        # title, description, and keywords help Workers find your HIT
        # duration is the # of seconds Workers have to complete your HIT
        # reward is what Workers will be paid when you approve their work
        # Check out the documentation on CreateHIT for more details
        if sandbox == False:
            check = raw_input("You are about to launch into production. Are you sure? [y/N] ")
            if not check in ['Y', 'y', 'Yes', 'yes']:
                exit()

        if qualification:
            response = mturk.create_hit(
                Question=question_html_value,
                MaxAssignments=hit_description['MaxAssignments'],
                Title=hit_description['Title'],
                Description=hit_description['Description'],
                Keywords=hit_description['Keywords'],
                AssignmentDurationInSeconds=hit_description['AssignmentDurationInSeconds'],
                LifetimeInSeconds=hit_description['LifetimeInSeconds'],
                Reward=f"{hit_description['Reward'] * len(dialogs)}",
                QualificationRequirements=[{'QualificationTypeId':"3TYM2RQLI3DD9VFPRP5NMOCSI6AL9O",
                                          'Comparator':"EqualTo",
                                          'IntegerValues':[1],
                                          'RequiredToPreview': True}]
                )
        else:
            response = mturk.create_hit(
                Question=question_html_value,
                MaxAssignments=hit_description['MaxAssignments'],
                Title=hit_description['Title'],
                Description=hit_description['Description'],
                Keywords=hit_description['Keywords'],
                AssignmentDurationInSeconds=hit_description['AssignmentDurationInSeconds'],
                LifetimeInSeconds=hit_description['LifetimeInSeconds'],
                Reward=f"{hit_description['Reward'] * len(dialogs)}")

    except Exception as e:
        import pdb; pdb.set_trace()
        print('Problem creating HIT')
        print(e)
        exit(1)

    hit_type_id = response['HIT']['HITGroupId']
    hit_id = response['HIT']['HITId']
    print("Your HIT has been created. You can see it at: "),
    print("https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id))
    print("Your HIT ID is: {}".format(hit_id))

    return hit_id

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Launches AMT HITs for ranking task.')
    parser.add_argument('task', type=str, help="task name")
    parser.add_argument('path_csv', type=str, help="path towards the csv containing data")
    parser.add_argument('--name', type=str, help='hit name')
    parser.add_argument('-b', '--sandbox',
                        default=False, action='store_true',
                        help='Set to true to run in the sandbox.')
    parser.add_argument('-n', type=int, default=10, help="Number of judgments (default 10)")
    parser.add_argument('--window', type=int, default=4, help="dialog window size (default 4)")
    parser.add_argument('--wage_per_judgement', type=float, default=0.01, help='Wage per judgement (default 0.01)')
    parser.add_argument('--duration', type=int, default=180, help="Assignment Duration in seconds")
    parser.add_argument('--lifetime', type=int, default=172800, help="Lifetime of the Hits")
    parser.add_argument('--keywords', type=str, default='dialogue, evaluation, response, chatting', help="Keywords of the HIT")
    parser.add_argument('--description', type=str, default='Annotation of conversations')
    parser.add_argument('--max_assignments', type=int, default=1)
    parser.add_argument('--title', type=str, default='JSALT 2020 : Annotation of conversation.')
    parser.add_argument('--qualification', action="store_true", default=False)
    parser.add_argument('--hit_file', type=str, default='hits.txt')
    args = parser.parse_args()

    # Create your connection to MTurk


    mturk = utils.create_mturk_client(args.sandbox)


    if args.sandbox == False:
        check = input("You are about to launch into production. Are you sure? [y/N] ")
        if not check in ['Y','y','Yes','yes']:
            exit()

    hit_description = {'Title': args.title,
                       'MaxAssignments' : args.max_assignments,
            'Description': args.description,
            'Keywords': args.keywords,
            'AssignmentDurationInSeconds': args.duration,
            'LifetimeInSeconds': args.lifetime,
            'Reward': args.wage_per_judgement}


    dialogs = make_dialogs(args.path_csv)
    segments = make_segments(dialogs, args.window)

    segments = add_attention_checks(segments, args.n)

    hit_ids = []
    for i in range(0, len(segments), args.n):
        hit_id = create_HIT(hit_description, args.name, mturk, task_instruction[args.task], segments[i:min(i + args.n, len(segments))], args.task, sandbox=args.sandbox, qualification=args.qualification)
        hit_ids.append(hit_id)


    with open(args.hit_file, 'w') as f_out:
        for hit_id in hit_ids:
            f_out.write('%s\n' % (hit_id))
