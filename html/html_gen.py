import os, sys
import argparse
from task_dictionaries import *

def generate_dialogue_old(n, window=None):
    """
    Generate the dialogue for the question
    :param n: max turn
    :param window: window for question
    :return:
    """
    if window is None:
        window = n
    elif window > n:
        window = n

    dialogue = f'<p class="well">U{1 if (n - window + 1)%2 == 1 else 2}' +': ${TURN_' + f'{n - window + 1}' +'}<br />'

    for i in range(n - window + 2, n + 1):
        if i % 2 == 0:
            dialogue += '\nU2: ${TURN_' + f'{i}' + '}<br />'
        else:
            dialogue += '\nU1: ${TURN_' + f'{i}' + '}<br />'

    dialogue = dialogue[:-5] + '/p>\n'

    return dialogue

def generate_dialogue(n, window):
    """
    Generate the dialogue for the question
    :param n: the number of the dialogue
    :param window: number of turns in the dialogue
    :return:
    """
    dialogue = f'<p class="well" id="dialog_{n}">U1' +': ${DIALOG_' + f'{n}_{1}' +'}<br />'

    for i in range(2, window + 1):
        if i % 2 == 0:
            dialogue += '\nU2: ${DIALOG_' + f'{n}_{i}' + '}<br />'
        else:
            dialogue += '\nU1: ${DIALOG_' + f'{n}_{i}' + '}<br />'

    dialogue = dialogue[:-5] + '/p>\n'

    return dialogue


def generate_dialogue_filled(dialog):
    """
    Generates a dialog filled for python launched script
    :param dialog: list of turns ending by the turn to annotate
    :return: str of html formatted dialog
    """
    dialogue = f'<p class="well">U1: {dialog[0]} <br />'

    for i in range(1, len(dialog)):
        if i % 2 == 1:
            dialogue += f'\nU2: {dialog[i]}<br />'
        else:
            dialogue += f'\nU1: {dialog[i]}<br />'

    dialogue = dialogue[:-5] + '/p>\n'

    return dialogue

def generate_question(instruction, question, answer, name, dialogue):
    """
    Generate one block of question for the html
    :param instruction: str containing the instruction (example : Read the text below paying close attention to detail, especially to the last utterance:)
    :param dialogue: str containing the html mechanical turk formatted dialogue, output of the generate_dialogue (example : <p class="well">S: ${TURN_1}<br />
U: ${TURN_2}<br />
S: ${TURN_3}</p>)
    :param question: str containing the question (example : Select one of the breakdown labels. (required))
    :param answer: list of the possible answers (example : ['BREAKDOWN', 'POSSIBLE BREAKDOWN', 'NOT A BREAKDOWN'])
    :param name: str containing the number of the turn to be annotated (example : "_02" )
    :return: the html div containing the question/answer block
    """
    question_html = f'<div class="panel panel-default" id="{name}">\n'
    question_html += f'<div class="panel-body"><label>{instruction}</label>\n'
    question_html += '\n' + dialogue
    question_html += question

    for a in answer:
        question_html += '\n' + f'<div class="radio" id="{name}"><label><input name="{name}" required="true" type="radio" value="{a[1]}" />{a[0]} </label></div>\n'

    question_html += '</div>\n</div>\n'

    return question_html

def generate_n_question_old(instruction, question, answer, n, warning, window=None, user="both"):
    """
    Generates the survey body
    :param instruction: str containing the instruction (example : Read the text below paying close attention to detail, especially to the last utterance:)
    :param question: str containing the question (example : Select one of the breakdown labels. (required))
    :param answer: list of the possible answers (example : ['BREAKDOWN', 'POSSIBLE BREAKDOWN', 'NOT A BREAKDOWN'])
    :param n: max turn
    :param warning: str containing the warning message about cheating
    :return: the full body of the survey
    """

    questions_html = '<div class="row" id="workContent" name="Bot001_044">\n<div class="col-sm-8 col-sm-offset-2">\n'
    questions_html += f'<p style="margin-bottom: 15px; font-size: 16px; line-height: 1.72222; color: rgb(52, 73, 94); font-family: Lato, Helvetica, Arial, sans-serif;"><span style="color: rgb(209, 72, 65);">{warning} </span></p>\n'

    # Which users we want to annotate
    if user == "both":
        beg = 1
        step = 1
    elif user == 'user1':
        beg = 1
        step = 2
    else:
        beg = 2
        step = 2

    for i in range(beg, n+1, step):
        q = generate_question(instruction, question, answer, f"_{i:02d}", generate_dialogue(i, window=window))
        questions_html += q

    questions_html += '</div>\n</div>\n'

    return questions_html


def generate_n_question(instruction, question, answer, n, warning, window, user="both"):
    """
        Generates the survey body
        :param instruction: str containing the instruction (example : Read the text below paying close attention to detail, especially to the last utterance:)
        :param question: str containing the question (example : Select one of the breakdown labels. (required))
        :param answer: list of the possible answers (example : ['BREAKDOWN', 'POSSIBLE BREAKDOWN', 'NOT A BREAKDOWN'])
        :param n: max turn
        :param warning: str containing the warning message about cheating
        :return: the full body of the survey
    """
    questions_html = '<div class="row" id="workContent" name="Bot001_044">\n<div class="col-sm-8 col-sm-offset-2">\n'
    questions_html += f'<p style="margin-bottom: 15px; font-size: 16px; line-height: 1.72222; color: rgb(52, 73, 94); font-family: Lato, Helvetica, Arial, sans-serif;"><span style="color: rgb(209, 72, 65);">{warning} </span></p>\n'

    for i in range(1, n+1):
        q = generate_question(instruction, question, answer, f"ANSWER_{i}", generate_dialogue(i, window=window))
        questions_html += q

    questions_html += '</div>\n</div>\n'

    return questions_html

def generate_n_questions_filled(instruction, question, answer, dialogs, warning):
    questions_html = '<div class="row" id="workContent" name="Bot001_044">\n<div class="col-sm-8 col-sm-offset-2">\n'
    questions_html += f'<p style="margin-bottom: 15px; font-size: 16px; line-height: 1.72222; color: rgb(52, 73, 94); font-family: Lato, Helvetica, Arial, sans-serif;"><span style="color: rgb(209, 72, 65);">{warning} </span></p>\n'

    for i in range(1, len(dialogs) + 1):
        q = generate_question(instruction, question, answer, f"ANSWER_{i}", generate_dialogue_filled(dialogs[i-1][1]))
        questions_html += q

    questions_html += '</div>\n</div>\n'

    return questions_html


def generate_instructions(path_instructions):
    """
    generates the div associated with the instructions from the html body of instructions
    :param path_instructions: path from which to read the instructions
    :return: the html formated <div> containing the instructions
    """
    f = open(path_instructions, 'r')
    inst = f.read()
    f.close()

    inst_html = '<div class="col-xs-12 col-md-12">\n'
    inst_html += '<div class="panel panel-primary">\n'
    inst_html += '<div class="panel-heading"><strong>Instructions</strong></div>\n'
    inst_html += '<div class="panel-body" id="instructionBody">\n'

    inst_html += inst + '\n'

    inst_html += '</div>\n</div>\n</div>\n</div>\n'

    return inst_html

def generate_html_filled(path_instructions, generated_questions, dialogs):
    html = """
        <HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
        <HTMLContent><![CDATA[
        <!DOCTYPE html>
        <html>
        <!-- Bootstrap v3.0.3 -->
        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
        <script src='https://s3.amazonaws.com/mturk-public/externalHIT_v1.js' type='text/javascript'></script>
        """

    html += """<!-- HIT template: Survey-v3.0 --><!-- The following snippet enables the 'responsive' behavior on smaller screens -->
        <meta content="width=device-width,initial-scale=1" name="viewport" />
        <section class="container" id="Survey"><!-- Instructions -->
        """

    html += generate_instructions(path_instructions)
    html += """
    <form name='mturk_form' method='post' id='mturk_form' action='https://workersandbox.mturk.com/mturk/externalSubmit'>
    <input type='hidden' value='' name='assignmentId' id='assignmentId'/>
    <!-- This is where you define your question(s) --> 
    """
    for i in range(1, len(dialogs)+1):
        html += f'<input id="NUMBER_{i}" name="NUMBER_{i}" type="hidden" value="{dialogs[i-1][0]}" />\n'
    html += generated_questions

    html += '<!-- End Survey Layout -->\n'
    html += '<!-- Please note that Bootstrap CSS/JS and JQuery are 3rd party libraries that may update their url/code at any time. Amazon Mechanical Turk (MTurk) is including these libraries as a default option for you, but is not responsible for any changes to the external libraries --><!-- External CSS references -->\n'
    html += '<link crossorigin="anonymous" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css" integrity="sha384-IS73LIqjtYesmURkDE9MXKbXqYA8rvKEp/ghicjem7Vc3mGRdQRptJSz60tvrB6+" rel="stylesheet" />\n'

    """
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates/stylesheet.html'), 'r')
    style = f.read()
    f.close()
    html += style
    """
    html += '<!-- External JS references --><script src="https://code.jquery.com/jquery-3.1.0.min.js" integrity="sha256-cCueBR6CsyA4/9szpPfrX3s49M9vUU5BgtiJj06wt/s=" crossorigin="anonymous"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.0.3/js/bootstrap.min.js" integrity="sha384-s1ITto93iSMDxlp/79qhWHi+LsIi9Gx6yL+cOKDuymvihkfol83TYbLbOw+W/wv4" crossorigin="anonymous"></script>\n'

    """
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates/scripts.html'), 'r')
    scripts = f.read()
    f.close()
    html += scripts
    """
    html += '<p>Please provide any comments you may have below, we appreciate your input!</p>\n'
    html += '<p><textarea cols="80" name="comment" rows="3">None?</textarea></p>\n'
    html += "<p><input type='submit' id='submitButton' value='Submit' /></p></form></section>\n"
    html += " <script language='Javascript'>turkSetAssignmentID();</script>\n"

    html += '</html>'
    html += """]]>
        </HTMLContent>
        <FrameHeight>600</FrameHeight>
        </HTMLQuestion>"""
    return html

def generate_full_html(path_instructions, generated_questions):
    """
    generates full html from instruction file and generated questions
    :param path_instructions: path of instruction file
    :param generated_questions: output of generate_n_question
    :return: the html string
    """
    html = """
    <HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
    <HTMLContent><![CDATA[
    <!DOCTYPE html>
    <html>
    <!-- Bootstrap v3.0.3 -->
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
    <input id="NUMBER_1" name="NUMBER_1" type="hidden" value="${NUMBER_1}" />
    <input id="NUMBER_2" name="NUMBER_2" type="hidden" value="${NUMBER_2}" />
    <input id="NUMBER_3" name="NUMBER_3" type="hidden" value="${NUMBER_3}" /><!-- HIT template: Survey-v3.0 --><!-- The following snippet enables the 'responsive' behavior on smaller screens -->
    <meta content="width=device-width,initial-scale=1" name="viewport" />
    <section class="container" id="Survey"><!-- Instructions -->
    """

    html += generate_instructions(path_instructions)
    html += generated_questions

    html += '<!-- End Survey Layout --></section>\n'
    html += '<!-- Please note that Bootstrap CSS/JS and JQuery are 3rd party libraries that may update their url/code at any time. Amazon Mechanical Turk (MTurk) is including these libraries as a default option for you, but is not responsible for any changes to the external libraries --><!-- External CSS references -->\n'
    html += '<link crossorigin="anonymous" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css" integrity="sha384-IS73LIqjtYesmURkDE9MXKbXqYA8rvKEp/ghicjem7Vc3mGRdQRptJSz60tvrB6+" rel="stylesheet" />\n'

    """
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates/stylesheet.html'), 'r')
    style = f.read()
    f.close()
    html += style
    """
    html += '<!-- External JS references --><script src="https://code.jquery.com/jquery-3.1.0.min.js" integrity="sha256-cCueBR6CsyA4/9szpPfrX3s49M9vUU5BgtiJj06wt/s=" crossorigin="anonymous"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.0.3/js/bootstrap.min.js" integrity="sha384-s1ITto93iSMDxlp/79qhWHi+LsIi9Gx6yL+cOKDuymvihkfol83TYbLbOw+W/wv4" crossorigin="anonymous"></script>\n'

    """
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates/scripts.html'), 'r')
    scripts = f.read()
    f.close()
    html += scripts
    """
    html += '<p>Please provide any comments you may have below, we appreciate your input!</p>\n'
    html += '<p><textarea cols="80" name="comment" rows="3">None?</textarea></p>\n'

    html += '</html>'
    html += """]]>
    </HTMLContent>
    <FrameHeight>600</FrameHeight>
    </HTMLQuestion>"""
    return html



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('instructions', type=str, help="Path to the file of html format instructions.")
    parser.add_argument('task', type=str, help="Task name. If the task name doesn't exist, you may add support by modifying the dictionaries of the python file.")
    parser.add_argument('-n', type=int, default=3, help="Max turn number (default 15).")
    parser.add_argument('--out_dir', type=str, default='./hits')
    args = parser.parse_args()


    if args.task not in task_answer_dictionary:
        print(f"Task : {args.task} not supported.")
        exit(1)

    h = generate_full_html(args.instructions,
                           generate_n_question('read to last utterance',
                                               task_question_dictionary[args.task],
                                               task_answer_dictionary[args.task],
                                               args.n,
                                               task_warning_dictionary[args.task],
                                               task_window_dictionary[args.task],
                                               task_user_dictionary[args.task]))

    #print(h)
    if not os.path.exists(args.out_dir):
        os.mkdir(args.out_dir)
    f = open(os.path.join(args.out_dir, f'{args.task}_{args.n}.html'), 'w')
    f.write(h)
    f.close()
