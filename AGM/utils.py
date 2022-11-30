import math
from sympy import to_cnf
from typing import List, Union
from AGM.clause import Clause
import sys

sys.setrecursionlimit(10000)


def DPLL(kb: List):
    try:
        unit_clauses = get_unit_clauses(kb)
        while unit_clauses:
            for clause in unit_clauses:
                kb = simplify(kb, clause)

                if kb == False:  # contradiction was found
                    return False
                elif len(kb) == 0:  # all terms were removed
                    return True

            unit_clauses = get_unit_clauses(kb)

        shortest_clause = ""
        shortest_clause_terms = math.inf

        for clause in kb:
            terms = clause.count('|')
            if terms < shortest_clause_terms:
                shortest_clause = clause
                shortest_clause_terms = terms

        term = shortest_clause.split(' |')[0]

        if DPLL([term] + kb):
            return True
        else:
            neg_term = str(to_cnf(f"~({term})"))
            return DPLL([neg_term] + kb)
    except:
        # hit recursion limit. Assume there is no solution then.A
        return False


def get_unit_clauses(kb: List) -> List:
    unit_clauses = []
    for clause in kb:
        # if unit clause
        if '|' not in clause:
            unit_clauses.append(clause)

    return unit_clauses


def simplify(kb: List, unit: str) -> Union[List, bool]:
    neg_unit = str(to_cnf(f"~({unit})"))
    space_unit = f" {unit}"

    new_kb = []
    for clause in kb:
        # if we look for the unit 'p' in the sentence 'r | ~p' it is found
        # therefore we will look for the string ' p', to ensure it has no negation
        if clause == unit or space_unit in clause:
            continue

        if neg_unit in clause:
            if '|' not in clause:  # unit clause of neg_unit implies a contradiction in kb
                return False

            # remove the negated unit from clauses
            if f"{neg_unit} | " in clause:
                new_kb.append(clause.replace(f"{neg_unit} | ", ""))
            else:
                new_kb.append(clause.replace(f" | {neg_unit}", ""))

        else:
            new_kb.append(clause)
    return new_kb


def get_units_from_clauses(kb: List[Clause]):
    all_units = []
    for clauses in kb:
        clause_copy = clauses.value.replace(" ", "")
        units = clause_copy.split("|")
        for unit in units:
            all_units.append(unit)

    return all_units


def sentence_to_clauses(sentence: str) -> List[str]:
    try:
        cnf = to_cnf(sentence)
        clauses = str(cnf).split('&')

    except SyntaxError:
        raise Exception('Formula provided has wrong format.')

    for i, clause in enumerate(clauses):
        clauses[i] = clause.replace('(', '').replace(')', '').strip()
    # TODO: Replace with map function
    return clauses


def split_sentence_by_first_OR(sentence: str) -> List[str]:
    #sentence = sentence[1:-1]
    parenthesis = 0
    splitters = []
    sentences = []
    for idx, c in enumerate(sentence):
        if c == '(':
            parenthesis += 1
        if c == ')':
            parenthesis -= 1
        if c == '|' and parenthesis == 0:
            splitters.append(idx)
    # if no splitters then we convert sentence to a List
    if len(splitters) == 0:
        sentences.append(sentence)
        return sentences
    start_split = 0
    for split in splitters:
        sentences.append(sentence[start_split:split])
        start_split = split + 1
    return sentences

