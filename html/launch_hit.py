import boto3
import argparse
import sys

sys.path.append('../python/utils')
import utils


def create_HIT(path_html, hit_description, hit_id, mturk, sandbox=False):
    f = open(path_html, 'r')
    question_html_value = f.read()
    f.close()

    question_html_value = question_html_value.encode('ascii', 'xmlcharrefreplace').decode()
    print(question_html_value)
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

        response = mturk.create_hit(
            Question=question_html_value,
            MaxAssignments=hit_description['MaxAssignments'],
            Title=hit_description['Title'],
            Description=hit_description['Description'],
            Keywords=hit_description['Keywords'],
            AssignmentDurationInSeconds=hit_description['AssignmentDurationInSeconds'],
            LifetimeInSeconds=hit_description['LifetimeInSeconds'],
            Reward=hit_description['Reward'])

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
    parser.add_argument('html', type=str, help="Html hit file")
    parser.add_argument('--name', type=str, help='hit name')
    parser.add_argument('-b', '--sandbox',
                        default=False, action='store_true',
                        help='Set to true to run in the sandbox.')

    args = parser.parse_args()

    # Create your connection to MTurk


    mturk = utils.create_mturk_client(args.sandbox)


    if args.sandbox == False:
        check = input("You are about to launch into production. Are you sure? [y/N] ")
        if not check in ['Y','y','Yes','yes']:
            exit()

    hit_description = {'Title': "Testing validation generation of html.",
                       'MaxAssignments' : 1,
            'Description': "Testing the generation of the html for the validation task",
            'Keywords': "sandbox",
            'AssignmentDurationInSeconds': 180,
            'LifetimeInSeconds': 172800,
            'Reward': "0.10"}

    hit_id = create_HIT(args.html, hit_description, f"cb_eval_{args.name}", mturk, sandbox=args.sandbox)
    with open('hits.txt', 'w') as f_out:
        f_out.write(hit_id)