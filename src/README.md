# Notes

Main.md file is the start point of the application and start UI, backend / UI_controller and timer to start update_parameters function in backend/UI_controller.

## Folder stucture 

2D_optical_vision_mapping/
│
├── docs/                 		        # Documentation files
│   └── introduction.md    	            # Project introduction document
│
├── src/                  		        # Source code files
│   ├── frontend/          		        # Frontend code
│   │   ├── main_window.ui              # Qt UI files (.ui) to edit using QT UI designer 
│   │   └── main_window_ui.py           # Python file created by UI complier
│   │
│   ├── backend/           		        # Backend code
│   │   ├── image_processing/           # Image processing logic
│   │   │   └── algorithms/             # Custom algorithms
│   │   │
│   │   ├── controllers/     	        # UI controller logic
│   │   │   └── controller.py           # Contains UI controller logic
|   |   | 
│   │   ├── motor_control/              # Motor control logic
│   │   |   └── acs_python_modules.py   # Python commands to control external motor controller
│   │   
│   ├── main.py 			            # Main application entry point
│   │       
│   └── utils/             		        # Utility functions and modules
│   
├── tests/                 		        # Test files
│   ├── frontend_tests/    		        # Frontend tests
│   ├── backend_tests/     		        # Backend tests
|   |   ├── image_processing/
|   |   ├── modules/
|   |   ├── motor_controller/
|   |   └── main.py
│   └── integration_tests/ 		        # Integration tests
│       
├── data/                  		        # Data files (optional)
│       
├── assets/                		        # Image assets, icons, etc. for UI (optional)
│       
├── dist/                  		        # Distribution files (generated executables, etc.)
│       
├── .gitignore             		        # Git ignore file
├── README.md              		        # Project README file
└── requirements.txt       		        # Python dependencies file




pip install PySide6
pyside6-uic .\main_window.ui -o .\main_window.py