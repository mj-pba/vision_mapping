from graphviz import Digraph

dot = Digraph(comment='Project Architecture', format='png')
dot.attr(rankdir='LR')

dot.node('F', 'Frontend\n(UI)')
dot.node('A', 'Application\n(Controllers)')
dot.node('D', 'Domain\n(Business Logic)')
dot.node('I', 'Infrastructure\n(Hardware APIs)')
dot.node('S', 'Assets & Docs', shape='folder')
dot.node('T', 'Tests', shape='folder')
dot.node('G', 'Data/Dist', shape='folder')

dot.edges([('F', 'A'), ('A', 'D'), ('D', 'I')])

dot.render('project_architecture', view=True)