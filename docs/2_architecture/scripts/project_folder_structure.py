from graphviz import Digraph

dot = Digraph(comment='Project Folder Structure', format='png')
dot.attr(rankdir='LR')

# Root
dot.node('A', '2D_optical_vision_mapping/\nProject Root')

# Top-level folders
dot.node('A1', 'assets/\nImages, logos, icons for UI', shape='folder')
dot.node('A2', 'docs/\nDocumentation', shape='folder')
dot.node('A3', 'src/\nSource code', shape='folder')
dot.node('A4', 'tests/\nTest scripts and data', shape='folder')

dot.edges([('A', 'A1'), ('A', 'A2'), ('A', 'A3'), ('A', 'A4')])

# src subfolders
dot.node('A3a', 'frontend/\nUI code (Qt .ui, .py)', shape='folder')
dot.node('A3b', 'backend/\nBackend logic', shape='folder')
dot.edge('A3', 'A3a')
dot.edge('A3', 'A3b')

# backend subfolders
dot.node('A3b1', 'controllers/\nUI controller logic', shape='folder')
dot.node('A3b2', 'image_processing/\nImage processing, vision', shape='folder')
dot.node('A3b3', 'motor_control/\nMotor control logic', shape='folder')
dot.node('A3b4', 'services/\nData processing, plotting', shape='folder')
dot.edges([('A3b', 'A3b1'), ('A3b', 'A3b2'), ('A3b', 'A3b3'), ('A3b', 'A3b4')])

# image_processing subfolders
dot.node('A3b2a', 'dahua_cam_api/\nDahua camera SDK/API', shape='folder')
dot.node('A3b2b', 'algorithms/\nCustom vision algorithms', shape='folder')
dot.edge('A3b2', 'A3b2a')
dot.edge('A3b2', 'A3b2b')

dot.render('project_folder_structure', view=True)