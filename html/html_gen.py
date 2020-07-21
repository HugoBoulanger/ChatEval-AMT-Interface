import os, sys
import argparse

def generate_dialogue(n):
    dialogue = '<p class="well">S: ${TURN_1}<br />'
    for i in range(2, n+2):
        if i%2 == 0:
            dialogue += '\nU: ${TURN_' + f'{i}' + '}<br />'
        else:
            dialogue += '\nS: ${TURN_' + f'{i}' + '}<br />'

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
    question_html = '<div class="panel panel-default">\n'
    question_html += f'<div class="panel-body"><label>{instruction}</label>\n'
    question_html += '\n' + dialogue
    question_html += question

    for a in answer:
        question_html += '\n' + f'<div class="radio"><label><input name="{name}" required="true" type="radio" value="{a}" />{a} </label></div>\n'

    question_html += '</div>\n</div>\n'

    return question_html

def generate_n_question(instruction, question, answer, n, warning):
    """
    Generates the survey body
    :param instruction: str containing the instruction (example : Read the text below paying close attention to detail, especially to the last utterance:)
    :param question: str containing the question (example : Select one of the breakdown labels. (required))
    :param answer: list of the possible answers (example : ['BREAKDOWN', 'POSSIBLE BREAKDOWN', 'NOT A BREAKDOWN'])
    :param n:
    :param warning: str containing the warning message about cheating
    :return: the full body of the survey
    """

    questions_html = '<div class="row" id="workContent" name="Bot001_044">\n<div class="col-sm-8 col-sm-offset-2">\n'
    questions_html += f'<p style="margin-bottom: 15px; font-size: 16px; line-height: 1.72222; color: rgb(52, 73, 94); font-family: Lato, Helvetica, Arial, sans-serif;"><span style="color: rgb(209, 72, 65);">{warning} </span></p>\n'

    for i in range(1, n+1):
        q = generate_question(instruction, question, answer, f"_{2*i:02d}", generate_dialogue(2*i))
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

    inst_html = '<div class="row">\n'
    inst_html += '<div class="col-xs-12 col-md-12">\n'
    inst_html += '<div class="panel panel-primary"><!-- WARNING: the ids "collapseTrigger" and "instructionBody" are being used to enable expand/collapse feature --><a class="panel-heading" href="javascript:void(0);" id="collapseTrigger"><strong>Instructions</strong> <span class="collapse-text">(Click to Collapse)</span> </a>\n'
    inst_html += '<div class="panel-body" id="instructionBody">\n'

    inst_html += inst + '\n'

    inst_html += '</div>\n</div>\n</div>\n</div>\n'

    return inst_html


def generate_full_html(path_instructions, generated_questions):
    """
    generates full html from instruction file and generated questions
    :param path_instructions: path of instruction file
    :param generated_questions: output of generate_n_question
    :return: the html string
    """
    html = """
    <!DOCTYPE html>
    <html>
    <title></title>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" /><script type='text/javascript' src='https://s3.amazonaws.com/mturk-public/externalHIT_v1.js'></script>
    <form action="https://www.mturk.com/mturk/externalSubmit" id="mturk_form" method="post" name="mturk_form"><input id="assignmentId" name="assignmentId" type="hidden" value="" /><!-- HIT template: Survey-v3.0 --><!-- The following snippet enables the 'responsive' behavior on smaller screens --></form>
    <meta content="width=device-width,initial-scale=1" name="viewport" />
    <section class="container" id="Survey"><!-- Instructions -->
    """

    html += generate_instructions(path_instructions)
    html += generated_questions

    html += '<!-- End Survey Layout --></section>\n'
    html += '<!-- Please note that Bootstrap CSS/JS and JQuery are 3rd party libraries that may update their url/code at any time. Amazon Mechanical Turk (MTurk) is including these libraries as a default option for you, but is not responsible for any changes to the external libraries --><!-- External CSS references -->\n'
    html += '<link crossorigin="anonymous" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css" integrity="sha384-IS73LIqjtYesmURkDE9MXKbXqYA8rvKEp/ghicjem7Vc3mGRdQRptJSz60tvrB6+" rel="stylesheet" />\n'

    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates/stylesheet.html'), 'r')
    style = f.read()
    f.close()
    html += style

    html += '<!-- External JS references --><script src="https://code.jquery.com/jquery-3.1.0.min.js" integrity="sha256-cCueBR6CsyA4/9szpPfrX3s49M9vUU5BgtiJj06wt/s=" crossorigin="anonymous"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.0.3/js/bootstrap.min.js" integrity="sha384-s1ITto93iSMDxlp/79qhWHi+LsIi9Gx6yL+cOKDuymvihkfol83TYbLbOw+W/wv4" crossorigin="anonymous"></script>\n'

    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates/scripts.html'), 'r')
    scripts = f.read()
    f.close()
    html += scripts

    html += '<p class="text-center"><input class="btn btn-primary" id="submitButton" type="submit" value="Submit" /></p>\n'
    html += '<script language="Javascript">turkSetAssignmentID();</script>\n'
    html += '</html>'
    return html



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('instructions', type=str)
    parser.add_argument('task', type=str)
    parser.add_argument('-n', type=int, default=5)
    parser.add_argument('--out_dir', type=str, default='./hits')
    args = parser.parse_args()

    task_answer_dictionary = {'breakdown': ['BREAKDOWN', 'POSSIBLE BREAKDOWN', 'NOT A BREAKDOWN']}
    task_question_dictionary = {'breakdown': 'Select one of the breakdown labels. (required)'}
    task_warning_dictionary = {'breakdown': 'The result may not be approved if it is considered as cheating by checking utterances which consist of Obviously BREAKDOWN and NOT A BREAKDOWN utterances. '}

    h = generate_full_html(args.instructions, generate_n_question('read to last utterance', task_question_dictionary[args.task], task_answer_dictionary[args.task], args.n, task_warning_dictionary[args.task]))
    #print(h)
    f = open(os.path.join(args.out_dir, f'{args.task}_{args.n}.html'), 'w')
    f.write(h)
    f.close()
