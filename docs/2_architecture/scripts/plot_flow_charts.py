#from graphviz import Digraph
#
#dot = Digraph(comment='Flowchart calculation error_mapping_for_acs.py')
#
## Set the size to A4
## dot.attr(size='11.69,8.27')  # A4 size in inches (width, height)
#
## Set the DPI for higher resolution
#dot.attr(dpi='300')
#
## Define nodes
#dot.node('A', 'Start: calculate_actual_dot_seperation')
#dot.node('B', 'open_location_file(varible_pitch_file_location)')
#dot.node('C', 'varible_pitch_array',shape='box')    # output shape
#dot.node('D', 'open_file_pandas_convert_numpy(file_path)')
#dot.node('P', 'log_file_1d_error_mapping_test',shape='box')   # output shape
#dot.node('E', 'calculate_one_pixel_size')
#dot.node('F', 'calculate_x_axis_error')
#dot.node('G', 'add_column_to_numpy_array')
#dot.node('H', 'log_file_1d_error_mapping_test_with_x_axis_error',shape='box')   # output shape
#dot.node('I', 'open_file_pandas_convert_numpy(file_path)')
#dot.node('J', 'laser_numpy_array',shape='box') # output shape
#dot.node('K', 'create_full_file_path')  
#dot.node('L', 'calculate_actual_dot_seperation_using_laser_and_vision_system')   # output shape
#dot.node('M', 'esitimate_dot_location_array',shape='box')  # output shape
#dot.node('N', 'plot_gpahs')
#dot.node('Q', 'plot_encoder_values_vs_calculated_encoder_values')
#dot.node('O', 'End')
#dot.node('S', 'End')
#
## Define edges with data used
#dot.edge('A', 'B', label='varible_pitch_file_location')
#dot.edge('B', 'C', label='')
#dot.edge('D', 'P', label='')
#dot.edge('A', 'D', label='log_file_1d_error_mapping_test')
#dot.edge('P', 'E', label='')
#dot.edge('A', 'E', label='actual_radius_mm, radius_column')
#dot.edge('P', 'F', label='')
#dot.edge('E', 'F', label='one_pixel_in_um')
#dot.edge('A', 'F', label='x_axis_column_of_log_file')
#dot.edge('F', 'G', label='axis_x_position_error_um_column')
#dot.edge('G', 'H', label='create new array')
#dot.edge('P', 'G', label='')
#dot.edge('A', 'I', label='laser_file_location')
#dot.edge('I', 'J', label='')
#dot.edge('A', 'K', label='laser_file_location, end_file_name.csv')
#dot.edge('J', 'L', label='laser_numpy_array')
#dot.edge('H', 'L', label='log_file_1d_error_mapping_test_with_x_axis_error')
#dot.edge('K', 'L', label='file_save_location_path_name')
#dot.edge('A', 'L', label='test_cycle_count')
#dot.edge('L', 'M', label='') # output shape
#dot.edge('M', 'N', label='esitimate_dot_location_array') # output shape
#dot.edge('N', 'O', label='')
#dot.edge('P', 'Q', label='')
#dot.edge('C', 'Q', label='')
#dot.edge('Q', 'S', label='')
#
## Render the graph
#dot.render('flowchart_diagram', format='png', view=False)
#

from graphviz import Digraph

dot = Digraph(comment='Flowchart calculation error_mapping_for_acs.py')

# Set the DPI for higher resolution
dot.attr(dpi='300')

# Define nodes
dot.node('A', 'Start: calculate_actual_dot_seperation')
dot.node('B', 'open_location_file(varible_pitch_file_location)')
dot.node('C', 'varible_pitch_array', shape='box')  # output shape
dot.node('D', 'open_file_pandas_convert_numpy(file_path)')
dot.node('P', 'log_file_1d_error_mapping_test', shape='box')  # output shape
dot.node('E', 'calculate_one_pixel_size')
dot.node('F', 'calculate_x_axis_error')
dot.node('G', 'add_column_to_numpy_array')
dot.node('H', 'log_file_1d_error_mapping_test_with_x_axis_error', shape='box')  # output shape
dot.node('I', 'open_file_pandas_convert_numpy(file_path)')
dot.node('J', 'laser_numpy_array', shape='box')  # output shape
dot.node('K', 'create_full_file_path')
dot.node('L', 'calculate_actual_dot_seperation_using_laser_and_vision_system')  # output shape
dot.node('M', 'estimate_dot_location_array', shape='box')  # output shape
dot.node('N', 'plot_graphs')
dot.node('Q', 'plot_encoder_values_vs_calculated_encoder_values')
dot.node('O', 'End')
dot.node('S', 'End')

# Define edges with data used
dot.edge('A', 'B', label='varible_pitch_file_location')
dot.edge('B', 'C', label='')
dot.edge('D', 'P', label='')
dot.edge('A', 'D', label='log_file_1d_error_mapping_test')
dot.edge('P', 'E', label='')
dot.edge('A', 'E', label='actual_radius_mm, radius_column')
dot.edge('P', 'F', label='')
dot.edge('E', 'F', label='one_pixel_in_um')
dot.edge('A', 'F', label='x_axis_column_of_log_file')
dot.edge('F', 'G', label='axis_x_position_error_um_column')
dot.edge('G', 'H', label='create new array')
dot.edge('P', 'G', label='')
dot.edge('A', 'I', label='laser_file_location')
dot.edge('I', 'J', label='')
dot.edge('A', 'K', label='laser_file_location, end_file_name.csv')
dot.edge('J', 'L', label='laser_numpy_array')
dot.edge('H', 'L', label='log_file_1d_error_mapping_test_with_x_axis_error')
dot.edge('K', 'L', label='file_save_location_path_name')
dot.edge('A', 'L', label='test_cycle_count')
dot.edge('L', 'M', label='')  # output shape
dot.edge('M', 'N', label='estimate_dot_location_array')  # output shape
dot.edge('N', 'O', label='')
dot.edge('P', 'Q', label='')
dot.edge('C', 'Q', label='')
dot.edge('Q', 'S', label='')

# Render the graph
dot.render('flowchart_diagram_1', format='png', view=False)