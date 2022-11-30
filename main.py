from del_interface import *
from experiments import experiments
from language_interface import LanguageInterface


def is_sees_formula(formula: str) -> (bool, bool):
    sees = ['see', 'know']
    splitted = formula.split('(')
    if sees.__contains__(splitted[0]):
        return True, True
    elif splitted[0] == 'not' and sees.__contains__(splitted[1]):
        return True, False
    return False, False


def sentence_to_array(s: str):
    s = s.lower()
    format_s = s.split()
    format_s = str(format_s).replace("'", "").replace(' ', '')
    return format_s

def pick_experiment():
    print('Input experiment to run (1 to {}):'.format(str(len(experiments))))
    for idx, e in enumerate(experiments):
        print('{}.  {}.'.format(str(idx+1), e))
    i = int(input())
    option = experiments.keys()
    option = list(option)[i-1]
    return experiments[option]


if __name__ == '__main__':
    engine = LanguageInterface()
    DEL_reset()

    experiment = pick_experiment()
    for sentence in experiment:
        array_sentence = sentence_to_array(sentence)
        b_agent = engine.agent_belief(array_sentence)
        if b_agent:
            sentence = sentence.split(' ', 3)
            sentence = sentence[3]
            array_sentence = sentence_to_array(sentence)

        formula = engine.parse_sentence(array_sentence)
        is_sees, pol = is_sees_formula(formula)
        agents = engine.extractPN(array_sentence)
        if is_sees:
            if pol:
                DEl_sees(agents)
                print('Added sees: {} sees {}'.format(agents[0], agents[1]))
            else:
                DEL_remove_sees(agents)
                print('Delete sees: {} do not see {}'.format(agents[0], agents[1]))
        elif b_agent:
            # here make question and return.
            cnf = engine.parse_to_cnf(array_sentence)
            agent_beliefs = DEL_question_agent(b_agent, cnf)
            is_real = DEL_question_world(cnf)
            if agent_beliefs:
                print('{}: beliefs in - {}'.format(b_agent, sentence))
            else:
                print('{}: do not believe in - {}'.format(b_agent, sentence))
            if not is_real:
                print('{}: has a false believe in - {}'.format(b_agent, sentence))

        else:
            # big assumption. First PN is the agent who does the action.
            cnf = engine.parse_to_cnf(array_sentence)
            agent_knowledge = DEL_action(agents[0], cnf)
            print("{} -> {}".format(agents[0], sentence))


