from graphviz import Digraph

def create_camera_architecture_diagram():
    dot = Digraph(comment='Camera Architecture - Teaching vs Runtime Modes', format='png')
    dot.attr(rankdir='TB', size='12,10')
    
    # Main title
    dot.attr('node', shape='box', style='filled', fillcolor='lightblue')
    dot.node('title', 'Camera System Architecture\nTeaching vs Runtime Modes', fontsize='16', fontweight='bold')
    
    # Current Implementation
    dot.attr('node', shape='box', style='filled', fillcolor='lightcoral')
    dot.node('current', 'Current Implementation\n(Performance Issues)', fontsize='14', fontweight='bold')
    
    # Camera Types
    dot.attr('node', shape='box', style='filled', fillcolor='lightyellow')
    dot.node('webcam', 'Web Camera\n(cam_id=0)')
    dot.node('dahua', 'Dahua Industrial\n(cam_id=1)')
    dot.node('bfs', 'BFS Camera\n(cam_id=1)')
    
    # Current Flow
    dot.attr('node', shape='ellipse', style='filled', fillcolor='lightgray')
    dot.node('continuous', 'Continuous Frame\nGrabbing')
    dot.node('ui_update', 'UI Update Loop\ncollec_frame_from_camer_send_to_UI()')
    dot.node('performance', 'Performance Issues\n• High CPU usage\n• Memory consumption\n• .exe lag')
    
    # Proposed Solution - Teaching Mode
    dot.attr('node', shape='box', style='filled', fillcolor='lightgreen')
    dot.node('teaching', 'TEACHING MODE\n(Live Preview)', fontsize='14', fontweight='bold')
    dot.node('teach_features', 'Features:\n• Continuous streaming\n• Real-time UI updates\n• Circle overlay drawing\n• Positioning assistance')
    
    # Proposed Solution - Runtime Mode  
    dot.attr('node', shape='box', style='filled', fillcolor='lightblue')
    dot.node('runtime', 'RUNTIME MODE\n(Capture on Demand)', fontsize='14', fontweight='bold')
    dot.node('runtime_features', 'Features:\n• Single frame capture\n• Flash-based imaging\n• RAM storage\n• On-demand UI update')
    
    # Implementation Components
    dot.attr('node', shape='diamond', style='filled', fillcolor='wheat')
    dot.node('mode_switch', 'Mode Selector\nUI Control')
    dot.node('camera_manager', 'Camera Manager\nBFS/Dahua/WebCam')
    dot.node('frame_processor', 'Frame Processor\nCircle overlay, scaling')
    
    # Data Flow
    dot.attr('node', shape='parallelogram', style='filled', fillcolor='lavender')
    dot.node('live_stream', 'Live Stream\nBuffer')
    dot.node('single_capture', 'Single Capture\nRAM Storage')
    dot.node('ui_display', 'UI Display\nQLabel Widget')
    
    # Connections - Current Implementation
    dot.edge('title', 'current')
    dot.edge('current', 'webcam')
    dot.edge('current', 'dahua') 
    dot.edge('current', 'bfs')
    dot.edge('webcam', 'continuous')
    dot.edge('dahua', 'continuous')
    dot.edge('bfs', 'continuous')
    dot.edge('continuous', 'ui_update')
    dot.edge('ui_update', 'performance')
    
    # Connections - Proposed Solution
    dot.edge('title', 'mode_switch')
    dot.edge('mode_switch', 'teaching')
    dot.edge('mode_switch', 'runtime')
    
    # Teaching Mode Flow
    dot.edge('teaching', 'teach_features')
    dot.edge('teaching', 'camera_manager')
    dot.edge('camera_manager', 'live_stream')
    dot.edge('live_stream', 'frame_processor')
    dot.edge('frame_processor', 'ui_display')
    
    # Runtime Mode Flow
    dot.edge('runtime', 'runtime_features')
    dot.edge('runtime', 'camera_manager')
    dot.edge('camera_manager', 'single_capture')
    dot.edge('single_capture', 'frame_processor')
    dot.edge('frame_processor', 'ui_display')
    
    # Class Structure
    with dot.subgraph(name='cluster_classes') as c:
        c.attr(label='Current Class Structure', style='dashed', color='blue')
        c.node('controller', 'UIController\n• camera_frame_update_activation\n• collec_frame_from_camer_send_to_UI()\n• camera_start_button()\n• camera_stop_button()')
        c.node('bfs_class', 'camera_frame_update_BFS\n• connect_camera()\n• capture_frame()\n• save_frame()\n• relese_camera()')
        c.edge('controller', 'bfs_class')
    
    # Proposed Class Structure
    with dot.subgraph(name='cluster_proposed') as c:
        c.attr(label='Proposed Enhanced Structure', style='dashed', color='green')
        c.node('enhanced_controller', 'Enhanced UIController\n• teaching_mode_active\n• runtime_mode_active\n• switch_camera_mode()\n• capture_on_demand()')
        c.node('camera_interface', 'Camera Interface\n• start_teaching_mode()\n• stop_teaching_mode()\n• capture_single_frame()\n• set_flash_settings()')
        c.edge('enhanced_controller', 'camera_interface')
    
    dot.render('camera_architecture_teaching_runtime', view=True)
    print("Camera architecture diagram generated: camera_architecture_teaching_runtime.png")

def create_detailed_flow_diagram():
    dot = Digraph(comment='Detailed Camera Flow - Teaching vs Runtime', format='png')
    dot.attr(rankdir='LR', size='14,10')
    
    # Teaching Mode Flow
    with dot.subgraph(name='cluster_teaching') as c:
        c.attr(label='TEACHING MODE FLOW', style='filled', color='lightgreen', fillcolor='lightgreen')
        c.node('t_start', 'User Clicks\n"Teaching Mode"', shape='ellipse')
        c.node('t_init', 'Initialize Camera\nContinuous Stream', shape='box')
        c.node('t_loop', 'Frame Update Loop\n60 FPS', shape='diamond')
        c.node('t_process', 'Process Frame:\n• Circle overlay\n• Scale to UI', shape='box')
        c.node('t_display', 'Update QLabel\nReal-time Preview', shape='box')
        c.node('t_stop', 'User Stops\nTeaching Mode', shape='ellipse')
        
        c.edge('t_start', 't_init')
        c.edge('t_init', 't_loop')
        c.edge('t_loop', 't_process')
        c.edge('t_process', 't_display')
        c.edge('t_display', 't_loop', label='continuous')
        c.edge('t_loop', 't_stop', label='stop signal')
    
    # Runtime Mode Flow  
    with dot.subgraph(name='cluster_runtime') as c:
        c.attr(label='RUNTIME MODE FLOW', style='filled', color='lightblue', fillcolor='lightblue')
        c.node('r_start', 'User Clicks\n"Capture"', shape='ellipse')
        c.node('r_flash', 'Trigger Flash\n(if enabled)', shape='box')
        c.node('r_capture', 'Single Frame\nCapture', shape='diamond')
        c.node('r_store', 'Store in RAM\nBuffer', shape='box')
        c.node('r_process', 'Process Frame:\n• Analysis ready\n• Scale for UI', shape='box')
        c.node('r_display', 'Update QLabel\nStatic Display', shape='box')
        c.node('r_save', 'Save to Disk\n(optional)', shape='box')
        
        c.edge('r_start', 'r_flash')
        c.edge('r_flash', 'r_capture')
        c.edge('r_capture', 'r_store')
        c.edge('r_store', 'r_process')
        c.edge('r_process', 'r_display')
        c.edge('r_process', 'r_save')
    
    # Decision Point
    dot.node('mode_decision', 'Camera Mode\nSelection', shape='diamond', style='filled', fillcolor='yellow')
    dot.edge('mode_decision', 't_start', label='Teaching')
    dot.edge('mode_decision', 'r_start', label='Runtime')
    
    # Performance Comparison
    with dot.subgraph(name='cluster_performance') as c:
        c.attr(label='PERFORMANCE COMPARISON', style='dashed', color='red')
        c.node('current_perf', 'Current:\n• 100% CPU during idle\n• Continuous memory usage\n• UI lag in .exe', 
               shape='box', style='filled', fillcolor='lightcoral')
        c.node('new_perf', 'Proposed:\n• 0% CPU during runtime\n• Memory efficient\n• Smooth .exe operation', 
               shape='box', style='filled', fillcolor='lightgreen')
    
    dot.render('detailed_camera_flow_teaching_runtime', view=True)
    print("Detailed flow diagram generated: detailed_camera_flow_teaching_runtime.png")

def create_implementation_roadmap():
    dot = Digraph(comment='Implementation Roadmap', format='png')
    dot.attr(rankdir='TB', size='10,12')
    
    # Phase 1
    with dot.subgraph(name='cluster_phase1') as c:
        c.attr(label='PHASE 1: Core Mode Implementation', style='filled', fillcolor='lightblue')
        c.node('p1_1', '1. Add mode selection UI\n(Radio buttons/Toggle)', shape='box')
        c.node('p1_2', '2. Modify UIController class\n• Add mode state variables\n• Update camera control logic', shape='box')
        c.node('p1_3', '3. Enhance camera classes\n• Add single capture methods\n• Optimize initialization', shape='box')
        
        c.edge('p1_1', 'p1_2')
        c.edge('p1_2', 'p1_3')
    
    # Phase 2  
    with dot.subgraph(name='cluster_phase2') as c:
        c.attr(label='PHASE 2: Performance Optimization', style='filled', fillcolor='lightgreen')
        c.node('p2_1', '4. Implement frame buffering\n• RAM storage for runtime\n• Efficient memory management', shape='box')
        c.node('p2_2', '5. Add flash control\n• Hardware integration\n• Timing synchronization', shape='box')
        c.node('p2_3', '6. Optimize UI updates\n• Conditional rendering\n• Reduce update frequency', shape='box')
        
        c.edge('p2_1', 'p2_2')
        c.edge('p2_2', 'p2_3')
    
    # Phase 3
    with dot.subgraph(name='cluster_phase3') as c:
        c.attr(label='PHASE 3: Testing & Validation', style='filled', fillcolor='lightyellow')
        c.node('p3_1', '7. Performance testing\n• CPU/Memory profiling\n• .exe validation', shape='box')
        c.node('p3_2', '8. User experience testing\n• Mode switching smoothness\n• Capture quality validation', shape='box')
        c.node('p3_3', '9. Documentation update\n• User manual\n• Technical specifications', shape='box')
        
        c.edge('p3_1', 'p3_2')
        c.edge('p3_2', 'p3_3')
    
    # Connect phases
    dot.edge('p1_3', 'p2_1', style='dashed', color='blue')
    dot.edge('p2_3', 'p3_1', style='dashed', color='blue')
    
    dot.render('camera_implementation_roadmap', view=True)
    print("Implementation roadmap generated: camera_implementation_roadmap.png")

if __name__ == "__main__":
    create_camera_architecture_diagram()
    create_detailed_flow_diagram() 
    create_implementation_roadmap()
    print("\nAll camera architecture diagrams have been generated!")
    print("Files created:")
    print("1. camera_architecture_teaching_runtime.png - Overall architecture")
    print("2. detailed_camera_flow_teaching_runtime.png - Detailed flow comparison") 
    print("3. camera_implementation_roadmap.png - Implementation phases")