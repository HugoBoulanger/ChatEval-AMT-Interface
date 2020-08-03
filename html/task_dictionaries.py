task_answer_dictionary = {'breakdown': [('BREAKDOWN', 0), ('POSSIBLE BREAKDOWN', 1), ('NOT A BREAKDOWN', 2)],
                          'validity_3pt': [("Doesn't make sense in context", 1),
                                           ("Could make sense but not natural", 2), ("Makes sense in context", 3)],
                          'validity_4pt': [("Invalid response", 1), ("Somewhat acceptable response", 2),
                                           ("Probably acceptable response", 3), ("Valid response", 4)]}
task_question_dictionary = {'breakdown': 'Select one of the breakdown labels. (required)',
                            'validity_3pt': "Does the final occurrence make sense? (required)",
                            'validity_4pt': "Does the final occurrence make sense? (required)"}
task_warning_dictionary = {
    'breakdown': 'The result may not be approved if it is considered as cheating by checking utterances which consist of Obviously BREAKDOWN and NOT A BREAKDOWN utterances. ',
    "validity_3pt": 'This HIT may not be approved if you make a rating without considering all sentences in the set. For example by rating an obviously valid sentence as invalid, etc. If you appear to be doing this, your HIT will be officially rejected. Please be careful.',
    "validity_4pt": 'This HIT may not be approved if you make a rating without considering all sentences in the set. For example by rating an obviously valid sentence as invalid, etc. If you appear to be doing this, your HIT will be officially rejected. Please be careful.'}
task_window_dictionary = {'breakdown': None,
                          'validity_3pt': 4,
                          'validity_4pt': 4}
task_user_dictionary = {'breakdown': 'user2',
                        'validity_3pt': 'both',
                        'validity_4pt': 'both'}

task_instruction = {'breakdown': './instructions/instruction_test.html',
                        'validity_3pt': './instructions/validity.html',
                        'validity_4pt': './instructions/validity_4pt.html'}
