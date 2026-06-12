# Image processing modules

During the initial stage of the process of the deverlopment we were forcused on moving the stage to capture images and saving the images to the folder. The camera related fuctions such as and there main forcus is list down bellow. 


1. camera_feed_in: Primery objective is to get image frame and display in the UI. The challenge occures when we try to display the camera feedback and save the images in the mean time. To prevent that simple statagy was implimented. Additionaly the class consiste of disply the ref cercle, and selecting the camera input index. 

2. scan_and_capture: This file contains the codes to perform motion inorder to move to locaions and capture the images and saving the position error values in the motion.


## Study of Machine Vision Technologes. 

With the presence of all the basic structures to capture and save images, as well as the necessary requirements to conduct tests, it is a good time to discuss the important features of image processing to move ahead with the project.

At the beginning we used tools provided in OpenCV to capture images and identify circles. However, many other tools are available to facilitate [computer vision](https://www.analyticsvidhya.com/blog/2021/06/everything-happening-in-computer-vision-that-you-should-know/) applications. Due to the versatile [machine vision types](https://easyodm.tech/machine-vision-industry-4-0/) and [highly diversed application](https://easyodm.tech/machine-vision-industry-4-0/) in the industry, many industrial-grade, paid algorithms are available on the market to handle more challenging tasks. 


### Halcon reference
1. Documentation for HALCON [Link](https://www.mvtec.com/products/halcon/work-with-halcon/documentation)
   1. Programmer's guide [Link](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/products/halcon/documentation/halcon/restricted-access/programmers_guide.pdf)
   2. Extension package [Link](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/products/halcon/documentation/halcon/restricted-access/extension_package_programmers_manual.pdf)
2. Halcon libry functions [Link](https://www.mvtec.com/doc/halcon/12/en/index.html)


### Installing Halcon software and Halcon/Python libry 

##### Installatilling HDeverlop software
1. Obtaine Hacon license from representative person and download the "MVTec software manager" from [MVTech website.](https://www.mvtec.com/downloads)
2. Go to the download link and run the software. (Ex: C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\Malith - R&D\2D error mapping\halcon_trial\som-1.5.0.260-x64-win64)
3. The software is run as a local server on the PC and load the app MVTech software installation tool in browser.[ref image](https://github.com/malithjkd/pba_vision_mapping/blob/main/assets/images/halcon_sofware_installer.png)
4. Select Halcon HDeverlop software and other nessery pakages. Its 12GB takes some time to install.
5. After installing clickt the three dots in the top right coner of the HDeverlop software and copy the licance file to the location or go to location and copy the lecence file to the [location](https://github.com/malithjkd/pba_vision_mapping/blob/main/assets/images/Copy_and_try_renameing_.png)
6. Now we can access the software and write program on it.

##### To install the Halcon/python libry
1. The documentation for installing halcon/python from the [link](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/products/halcon/documentation/halcon/restricted-access/programmers_guide.pdf).
2. Create python enviroment with new python above 3.8. [We created conda enviroment "py12" using python 3.12.]
3. Sorce activate the envirment [py312]
4. Install halcon/python libry using [ref image](https://github.com/malithjkd/pba_vision_mapping/blob/main/assets/images/Install_halcon_python.png)
   ```consol
   pip install mvtec-halcon==24050
   ```
5. Create folder and test_program_halcon.py
   ```consol
   mkdir test
   touch test_program_halcon.py
   ```
6. Copy the example provided in the programming guide documentation.  
7. Try to import halcon libry in python enviroment. [ref image](https://github.com/malithjkd/pba_vision_mapping/blob/main/assets/images/Import_halcon_and_setup_path.png)
8. The error can happen due to not setting up parth. To setup parth [ref image]()
   ```consol
   (py312) C:\User\**>set PATH=%HALCONROOT%/bin/x64-win64;%PATH%
   ```

9. Exicute the program using python test_program_halcon.py

10. If not try to setup path using ['System Properties'](https://github.com/malithjkd/pba_vision_mapping/blob/main/assets/images/System_properties.png) -> ['Enviroment Variabls'](https://github.com/malithjkd/pba_vision_mapping/blob/main/assets/images/manual_path_setup.png)