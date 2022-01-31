import random
import pomegranate as pg
import math

class OneNode:
    def __init__(self, name: str, depends: list, probabilities: dict) -> None:
        self.name = name
        self.depends = depends
        self.probab = probabilities

class RandomGenerator:
    def __init__(self) -> None:
        self.nodes = []
        self.generated = []

    def print_nodes(self) -> None:
        for node in self.nodes:
            print(vars(node))

    def print_generated(self) -> None:
        for generated_one in self.generated:
            print(generated_one)

    def load(self, name: str, depends: list, probabilities: dict) -> None:
        """
        Loads one Bayes node to the network
        name: name of you node
        depends: list of names of nodes that this node depends on (strings)
        probabilities: dictionary of probabilities, key is state of the nodes
        this node depends on (in the order they are declared in "depends") and
        value is the probability of True (assumes False adds up to 1). If this
        node doesn't depend on any, then keys are states of this node (must be
        1 and 0) and values are probabilities of this states taking place"""
        self.nodes.append(OneNode(
            name, depends, probabilities
        ))

    def generate(self, how_many: int, show_status=True) -> None:
        self.generated = []
        for i in range(how_many):
            self.generated.append(self.generate_one())
            if show_status and i % 10 == 0:
                print(' ', str(math.trunc(i*100/how_many)) + '%', end='\r')
        if show_status: print('  100%')

    def generate_one(self) -> dict:
        generated_one = {}
        for node in self.nodes:
            if node.depends == []:
                generated_one[node.name] = random.choices(
                    (0, 1),
                    weights=(node.probab[0], node.probab[1])
                )[0]
            else:
                temp = [generated_one[depend] for depend in node.depends]
                if len(temp) == 1:
                    temp = temp[0]
                else:
                    temp = tuple(temp)
                probab = node.probab[temp]
                generated_one[node.name] = random.choices(
                    (0, 1),
                    weights=(1-probab, probab)
                )[0]
        return generated_one

    def count_generated(self) -> dict:
        my_sum = {}
        for name in self.generated[0].keys():
            my_sum[name] = 0
        for generated_one in self.generated:
            for name, value in generated_one.items():
                my_sum[name] += value
        for name in self.generated[0].keys():
            my_sum[name] /= len(self.generated)
        return my_sum

    def count_probab_of_one(self, one: dict) -> float:
        probab = 0
        for generated_one in self.generated:
            status = True
            for one_name, one_value in one.items():
                if generated_one[one_name] != one_value:
                    status = False
            if status:
                probab += 1
        return probab / len(self.generated)

def count_probab(RG: RandomGenerator, one: dict, lacking: str) -> str:
    one[lacking] = 1
    result_one = RG.count_probab_of_one(one)
    one[lacking] = 0
    result_zero = RG.count_probab_of_one(one)
    return f"0: {result_zero/(result_zero+result_one)}\n1: {result_one/(result_zero+result_one)}"

def predict_pomegranate(args: dict):
    wys = pg.DiscreteDistribution({
        1: 0.66,
        0: 0.33
    })
    waga = pg.DiscreteDistribution({
        1: 0.2,
        0: 0.8
    })
    problem = pg.ConditionalProbabilityTable(
        [[1, 1, 1, 0.9],
        [1, 1, 0, 0.1],
        [1, 0, 1, 0.4],
        [1, 0, 0, 0.6],
        [0, 1, 1, 0.5],
        [0, 1, 0, 0.5],
        [0, 0, 1, 0.1],
        [0, 0, 0, 0.9]],
        [wys, waga]
    )
    zlamanie = pg.ConditionalProbabilityTable(
        [[1, 1, 0.84],
        [1, 0, 1-0.84],
        [0, 1, 0.3],
        [0, 0, 1-0.3]],
        [problem]
    )
    s_wys = pg.State(wys, name='wysoki wzrost')
    s_waga = pg.State(waga, name='duza waga')
    s_problem = pg.State(problem, name='problemy ze stawami')
    s_zlamanie = pg.State(zlamanie, name='zlamanie obojczyka')

    model = pg.BayesianNetwork()
    model.add_states(s_wys, s_waga, s_problem, s_zlamanie)
    model.add_edge(s_wys, s_problem)
    model.add_edge(s_waga, s_problem)
    model.add_edge(s_problem, s_zlamanie)
    model.bake()
    return model.predict_proba(args)

def main():
    RG = RandomGenerator()
    RG.load('wysoki wzrost', [], {
        1: 0.66,
        0: 0.33
    })
    RG.load('duza waga', [], {
        1: 0.2,
        0: 0.8
    })
    RG.load('problemy ze stawami', ['wysoki wzrost', 'duza waga'], {
        (1, 1): 0.9,
        (1, 0): 0.4,
        (0, 1): 0.5,
        (0, 0): 0.1
    })
    RG.load('zlamanie obojczyka', ['problemy ze stawami'], {
        1: 0.84,
        0: 0.3
    })
    RG.generate(10**6)
    RG.print_nodes()
    print('----------')
    # print(RG.count_generated())
    one = {
        'wysoki wzrost': 1,
        'duza waga': 0,
        # 'problemy ze stawami': 1,
        'zlamanie obojczyka': 1,
    }
    print('My results:')
    print(count_probab(RG, one.copy(), 'problemy ze stawami'))
    print('Pomegranate results:')
    print(predict_pomegranate(one))

if __name__ == "__main__":
    main()
