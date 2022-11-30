from epistemic_logic.predicates.predicate import Predicate


class Knows:
    def __init__(self, agent, info, pointing_w):
        self.agent = agent
        self.info = info
        self.pointing_w = pointing_w
        self.ref_knowledge = []

    def add_next_knowledge(self, k):
        self.ref_knowledge.append(k)

    def __str__(self):
        infos_str = ''
        for i, ors in enumerate(self.info):
            infos_str += '('
            for j, predicate in enumerate(ors):
                infos_str += str(predicate)
                if j + 1 < len(ors):
                    infos_str += ' OR '
            infos_str += ')'
            if i + 1 < len(self.info):
                infos_str += ' AND '
        return 'K_{}({})'.format(self.agent, infos_str)

    def stringify(self):
        '''
        creates recursively knowledge of the state of worlds and beliefs of other agents.
        '''
        if len(self.ref_knowledge) > 0:
            current_k = self.__str__()
            tmp = []
            for k in self.ref_knowledge:
                k_values = k.stringify()
                for i in k_values:
                    k_string = 'K_{}({})'.format(self.agent, i)
                    tmp.append(k_string)
            output = [current_k]
            output.extend(tmp)
            return output
        return [self.__str__()]
