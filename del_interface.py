from AGM.BeliefBase import BeliefBase
from epistemic_logic.dynamic_epistemic_logic import DEL
from epistemic_logic.predicates.predicate import NoPredicate


def DEL_reset():
    DEL.reset()


def DEl_sees(pair):
    DEL.update_vision([pair])


def DEL_remove_sees(pair):
    DEL.remove_vision([pair])


def DEL_action(agent, formula):
    DEL.update(agent, formula)

    DEL.crunch_worlds()
    agent_knowledge = DEL.knowledge(DEL.world_nr + 1)
    output = {}
    for knowledge in agent_knowledge:
        output[knowledge.agent] = knowledge.stringify()
    strinfy_predicate = ''
    for i, ors in enumerate(DEL.current_world.assignment):
        strinfy_predicate += '('
        for j, predicate in enumerate(ors):
            strinfy_predicate += str(predicate)
            if j + 1 < len(ors):
                strinfy_predicate += ' OR '
        strinfy_predicate += ')'
        if i + 1 < len(DEL.current_world.assignment):
            strinfy_predicate += ' AND '
    output["world"] = strinfy_predicate
    return output


def DEL_question_agent(agent, question):
    answer = False
    agent_knowledge = DEL.knowledge(DEL.world_nr + 1)
    belief_engine = BeliefBase()
    for knowledge in agent_knowledge:
        if knowledge.agent == agent:
            # generate agents belief's
            fol_predicate_mapping = {}
            predicate_fol_mapping = {}
            variable = 'a'
            for i, clause in enumerate(knowledge.info):
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
                    if j + 1 < len(clause):
                        clause_str += ' | '
                belief_engine.expansion(clause_str)

            # check if question can be infer in the agent belief's
            clause_str = ''
            for i, clause in enumerate(question):
                clause_str += '('
                for j, predicate in enumerate(clause):
                    if predicate[:3] == 'not':
                        clause_str += '~'
                        predicate = predicate[4:-1]
                    if predicate not in fol_predicate_mapping:
                        fol_predicate_mapping[predicate] = variable
                        predicate_fol_mapping[variable] = predicate
                        variable = chr(ord(variable) + 1)
                    clause_str += fol_predicate_mapping[predicate]
                    if j + 1 < len(clause):
                        clause_str += ' | '
                clause_str += ')'
                if i+1 < len(question):
                    clause_str += ' & '

            answer = belief_engine.check_entailment(clause_str)

    return answer


def DEL_question_world(question):
    answer = False
    agent_knowledge = DEL.knowledge(DEL.world_nr + 1)
    belief_engine = BeliefBase()

    # generate agents belief's
    fol_predicate_mapping = {}
    predicate_fol_mapping = {}
    variable = 'a'
    for i, clause in enumerate(DEL.current_world.assignment):
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
            if j + 1 < len(clause):
                clause_str += ' | '
        belief_engine.expansion(clause_str)

    # check if question can be infer in the agent belief's
    clause_str = ''
    for i, clause in enumerate(question):
        clause_str += '('
        for j, predicate in enumerate(clause):
            if predicate[:3] == 'not':
                clause_str += '~'
                predicate = predicate[4:-1]
            if predicate not in fol_predicate_mapping:
                fol_predicate_mapping[predicate] = variable
                predicate_fol_mapping[variable] = predicate
                variable = chr(ord(variable) + 1)
            clause_str += fol_predicate_mapping[predicate]
            if j + 1 < len(clause):
                clause_str += ' | '
        clause_str += ')'
        if i+1 < len(question):
            clause_str += ' & '

    answer = belief_engine.check_entailment(clause_str)

    return answer
