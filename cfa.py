from graphviz import Digraph

# Tạo đối tượng đồ thị
dot = Digraph(format='png')
dot.attr(rankdir='LR', size='10')

# Các node (biến tiềm ẩn)
dot.node('EB', 'Environmental beliefs', shape='ellipse', style='filled', fillcolor='#b3e2cd')
dot.node('EK', 'Environmental knowledge', shape='ellipse', style='filled', fillcolor='#cbd5e8')
dot.node('EC', 'Environmental concern', shape='ellipse', style='filled', fillcolor='#fddaec')
dot.node('GBI', 'Green brand image', shape='ellipse', style='filled', fillcolor='#fed9a6')
dot.node('BL', 'Brand loyalty', shape='ellipse', style='filled', fillcolor='#fbb4ae')

# Các mối quan hệ giữa các biến (các mũi tên)
dot.edge('EB', 'EC', label='H1: .72***')
dot.edge('EK', 'EC', label='H2: .06**')
dot.edge('EC', 'GBI', label='H3: –.26***')
dot.edge('GBI', 'BL', label='H4: .52***')

# Mối quan hệ gián tiếp thông qua GBI: EC → GBI → BL
dot.attr(label='Figure: Structural Equation Model', fontsize='20')

# Xuất ra
dot.render('sem_diagram', view=True)
