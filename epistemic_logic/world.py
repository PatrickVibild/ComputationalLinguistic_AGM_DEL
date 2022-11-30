from AGM.BeliefBase import BeliefBase
from epistemic_logic.predicates.predicate import *


class World:
    """
    Represents the nodes of Kripke and it extends the graph to Kripke
    Structure by assigning a subset of propositional variables to each world.
    """

    def __init__(self, name, assignment):
        self.name = name
        self.assignment = assignment
        self.copy_of = None

    def __eq__(self, other):
        return self.name == other.name and self.assignment == other.assignment

    def __str__(self):
        return "(" + self.name + ',' + str(self.assignment) + ')'

    def rename(self, name):
        self.copy_of = self.name
        self.name = name

    def update_world(self, predicates):
        belief = BeliefBase()
        fol_predicate_mapping = {}
        predicate_fol_mapping = {}
        variable = 'a'
        # create beliefs.
        for i, clause in enumerate(self.assignment):
            clause_str = ''
            for j, predicate in enumerate(clause):
                predicate_str = predicate.string()
                if predicate_str not in fol_predicate_mapping:
                    fol_predicate_mapping[predicate_str] = variable
                    predicate_fol_mapping[variable] = predicate_str
                    variable = chr(ord(variable) + 1)
                if isinstance(predicate, NoPredicate):
                    clause_str += '~'
                clause_str += fol_predicate_mapping[predicate_str]
                if j+1 < len(clause):
                    clause_str += ' | '
            belief.expansion(clause_str)
        # contract and expansion of new predicates.

        for i, clause in enumerate(predicates):
            clause_str = ''
            for j, predicate in enumerate(clause):
                predicate_str = predicate.string()
                if predicate_str not in fol_predicate_mapping:
                    fol_predicate_mapping[predicate_str] = variable
                    predicate_fol_mapping[variable] = predicate_str
                    variable = chr(ord(variable) + 1)
                if isinstance(predicate, NoPredicate):
                    clause_str += '~'
                clause_str += fol_predicate_mapping[predicate_str]
                if j+1 < len(clause):
                    clause_str += ' | '
            belief.revision(clause_str)

        current_belief = belief.get_knowledge_base()
        assignments = []
        for clause in current_belief:
            clauses = []
            for predicate in clause.split('|'):
                predicate = predicate.strip()
                if predicate[0] == '~':
                    clauses.append(NoPredicate(predicate_fol_mapping[predicate[1:]]))
                else:
                    clauses.append(Predicate(predicate_fol_mapping[predicate]))
            assignments.append(clauses)
        self.assignment = assignments

        # # mapping from AGM format to previous sentences.
        # for predicate in predicates:
        #     if isinstance(predicate, NoPredicate):
        #         negated = predicate.negate()
        #         if negated in self.assignment:
        #             self.assignment.remove(negated)
        #     else:
        #         if not (predicate in self.assignment):
        #             self.assignment.append(predicate)
