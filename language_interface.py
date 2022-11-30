from pyswip import Prolog


class LanguageInterface:
    def __init__(self):
        self.prolog_language = Prolog()
        self.prolog_language.consult('BB1/del.pl')

    def parse_sentence(self, s: str):
        query = 'holeSemantics(' + s + ',F)'
        for solution in self.prolog_language.query(query):
            return solution["F"][0].value

    def parse_to_cnf(self, formula: str):
        query = 'holeCNF(' + formula + ' ,F)'
        for solution in self.prolog_language.query(query):
            result = []
            for clause in solution["F"]:
                ors = []
                for predicate in clause:
                    ors.append(predicate.value)
                result.append(ors)
            return result

    def extractPN(self, s: str):
        query = 'extractPN(' + s + ', R)'
        result = []
        for solutions in self.prolog_language.query(query):
            for solution in solutions["R"]:
                result.append(solution.value)
            # checking only first loop since we can have arrays [annie, sally] and [sally,annie]
            return result

    def agent_belief(self, s: str):
        query = 'belief('+s+', A, F)'
        agent = None
        question = None
        for solutions in self.prolog_language.query(query):
            agent = solutions['A']
        return agent
