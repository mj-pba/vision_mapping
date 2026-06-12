# 1D expantion X axis or 1D expantion Y axis plot with laser 

# command to plot chart 
# python plot_flow_chart_1D_explantion_test_plot.py

from graphviz import Digraph

dot = Digraph(comment='1D error map - Glass scale self centering test with laser traking position Plot repetability graph calculate_actual_dot_seperation.py')

# Set the DPI for higher resolution
dot.attr(dpi='300')

# Define nodes
dot.node('A', 'Start: Calculate actual dot seperation(varible_pitch_file_location,laser_file_location,log_file_1d_error_mapping_test)')
dot.node('B1', 'Number of axis = 3',shape = 'parallelogram')
dot.node('B', 'open_location_file',shape = 'box') 
dot.node('C', 'varible_pitch_array', shape = 'parallelogram')

dot.node('D', 'open_file_pandas_convert_numpy', shape = 'box')
dot.node('E', 'log_file_1d_error_mapping_test_numpy_array', shape='parallelogram')

dot.node('F1', 'actual_radius_mm = 0.25', shape = 'parallelogram') 
dot.node('F2', 'radius_column = 13', shape = 'parallelogram') 

dot.node('F', 'calculate_one_pixel_size',shape = 'box')
dot.node('F3', 'one_pixel_in_um', shape = 'parallelogram')

dot.node('G1', 'dot_location_center_vision_x_axis_column = 12', shape = 'parallelogram')
dot.node('G', 'calculate_x_axis_error', shape = 'box')
dot.node('H', 'axis_x_position_error_um', shape='parallelogram') 

dot.node('I', 'add_column_to_numpy_array', shape='box')
dot.node('J', 'log_file_1d_error_mapping_test_with_x_axis_error', shape='parallelogram') 

dot.node('K1', 'log_file_1d_error_mapping_test_with_x_axis_error.csv', shape='parallelogram')
dot.node('K', 'create_full_file_path', shape='box')

dot.node('L', 'save_file_to_csv', shape='box')

dot.node('M', 'open_file_pandas_convert_numpy', shape = 'box')
dot.node('N', 'laser_numpy_array', shape = 'parallelogram')
dot.node('O', 'get_number_of_cycles', shape = 'box')
dot.node('O1', 'test_cycle_count', shape = 'parallelogram')
dot.node('P', 'calculate_actual_dot_seperation_using_laser_and_vision_system', shape = 'box')

dot.node('R', 'laser_and_vision_based_esitimate_dot_location_array.csv', shape = 'parallelogram')
dot.node('Q', 'create_full_file_path', shape = 'box')
dot.node('S', 'file_save_location_path_name', shape = 'parallelogram')   


#dot.node('L', 'calculate_actual_dot_seperation_using_laser_and_vision_system')

#dot.node('S', 'End')

# Define edges with data used
dot.edge('A', 'B', label='varible_pitch_file_location')
dot.edge('B1', 'B', label='')
dot.edge('B', 'C', label='')

dot.edge('A', 'D', label='log_file_1d_error_mapping_test')
dot.edge('D', 'E', label='')

dot.edge('F1', 'F', label='')
dot.edge('F2', 'F', label='')
dot.edge('E', 'F', label='')
dot.edge('F', 'F3', label='')

dot.edge('E', 'G', label='')
dot.edge('G1', 'G', label='')
dot.edge('F3', 'G', label='')
dot.edge('G', 'H', label='')

dot.edge('E', 'I', label='')
dot.edge('H', 'I', label='')
dot.edge('I', 'J', label='')

dot.edge('A', 'K', label='log_file_1d_error_mapping_test')
dot.edge('K1', 'K', label='')

dot.edge('K', 'L', label='full file parth')
dot.edge('J', 'L', label='save array to csv')

dot.edge('A', 'M', label='laser_file_location')
dot.edge('M', 'N', label='')
dot.edge('N', 'O', label='laser_numpy_array.shape[1]')
dot.edge('O', 'O1', label='')

dot.edge('N', 'P', label='')
dot.edge('J', 'P', label='')
dot.edge('O1', 'P', label='')
dot.edge('S', 'P', label='')

dot.edge('A', 'Q', label='laser_file_location')
dot.edge('R', 'Q', label='')
dot.edge('Q', 'S', label='')

#dot.edge('G', 'H', label='create new array')
#dot.edge('P', 'G', label='')
#dot.edge('A', 'I', label='laser_file_location')



# Render the graph
dot.render('flowchart_diagram_1D_expantion_plot', format='png', view=False)