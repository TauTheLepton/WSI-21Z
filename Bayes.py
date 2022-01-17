import bnlearn as bn
from pgmpy.factors.discrete import TabularCPD

edge = [('flue', 'fever')]

flu = TabularCPD(values=[[0.95],[0.05]], variable='flu', variable_card=2)

fever = TabularCPD(values=[[0.8, 0.1], [0.2, 0.9]], evidence=['flu'], variable_card=2, variable='fever', evidence_card=[2])

DAG = bn.make_DAG(edge)
model = bn.make_DAG(DAG, CPD=[flu, fever])

bn.inference.fit(model, variables=['flu'], evidence={'fever': 1})
