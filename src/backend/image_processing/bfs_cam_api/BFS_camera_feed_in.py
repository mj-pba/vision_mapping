# coding=utf-8
# adapted from spinnaker example code spinnaker_python-4.2.0.83-cp310-cp310-win_amd64/Examples/Python3/Acquisition.py

import sys
import PySpin
import platform
import cv2

class camera_frame_update_BFS:
    STREAM_MODE_TELEDYNE_GIGE_VISION = 0
    STREAM_MODE_PGRLWF = 1
    STREAM_MODE_SOCKET = 2

    def __init__(self, index):
        self.cam_id_select = index
        self.capture_frame_activation = 1
        self.cam = None
        self.system = PySpin.System.GetInstance()
        self.cam_list = self.system.GetCameras()
        self.CHOSEN_STREAMMODE = self._determine_stream_mode()
        num_cameras = self.cam_list.GetSize()

        print('Number of cameras detected: %d' % num_cameras)

    def _determine_stream_mode(self):
        system = platform.system()
        if system == "Windows":
            print("Using Stream mode STREAM_MODE_TELEDYNE_GIGE_VISION",self.STREAM_MODE_TELEDYNE_GIGE_VISION)
            return self.STREAM_MODE_TELEDYNE_GIGE_VISION
        elif system in ["Linux", "Darwin"]:
            print("Using Stream mode STREAM_MODE_SOCKET")
            return self.STREAM_MODE_SOCKET
        else:
            print("OS Unknown; Using Stream mode STREAM_MODE_SOCKET")
            return self.STREAM_MODE_SOCKET

    def configure_exposure_and_gain(self):
        try:
            if self.cam.ExposureAuto.GetAccessMode() != PySpin.RW:
                print('Unable to disable automatic exposure. Aborting...')
                sys.exit()
                return False

            self.cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)
            print('Automatic exposure disabled...')
            if self.cam.ExposureTime.GetAccessMode() != PySpin.RW:
                print('Unable to set exposure time. Aborting...')
                sys.exit()
                return False
            exposure_time_to_set = 70 #400 #300 #5000.0 # change if too bright/dark. value is in microsecs (us)
            exposure_time_to_set = min(self.cam.ExposureTime.GetMax(), exposure_time_to_set) # make sure value is within range
            self.cam.ExposureTime.SetValue(exposure_time_to_set)
            print('Shutter time set to %s us...\n' % exposure_time_to_set)

            nodemap = self.cam.GetNodeMap()
            node_gain_auto = PySpin.CEnumerationPtr(nodemap.GetNode('GainAuto'))
            if not PySpin.IsAvailable(node_gain_auto) or not PySpin.IsWritable(node_gain_auto):
                print('Unable to get {} ({} {} retrieval failed.)'.format('node', 'GainAuto', 'node'))
                print('The {} may not be available on all camera models...'.format('node'))
                print('Please try a Blackfly S camera.')
                sys.exit()
                return False

            gain_auto_off = node_gain_auto.GetEntryByName('Off')
            if not PySpin.IsAvailable(gain_auto_off) or not PySpin.IsReadable(gain_auto_off):
                print('Unable to get {} ({} {} retrieval failed.)'.format('entry', 'GainAuto Off', 'entry'))
                print('The {} may not be available on all camera models...'.format('entry'))
                print('Please try a Blackfly S camera.')
                sys.exit()
                return False

            node_gain_auto.SetIntValue(gain_auto_off.GetValue())

            print('Automatic gain disabled...')
        except PySpin.SpinnakerException as ex:
            print('Error when configuring exposure/gain: %s' % ex)

        return True


    def set_stream_mode(self):
        stream_mode_map = {
            self.STREAM_MODE_TELEDYNE_GIGE_VISION: "TeledyneGigeVision",
            self.STREAM_MODE_PGRLWF: "LWF",
            self.STREAM_MODE_SOCKET: "Socket",
        }

        stream_mode = stream_mode_map.get(self.CHOSEN_STREAMMODE, "Socket")

        nodemap_tlstream = self.cam.GetTLStreamNodeMap()
        node_stream_mode = PySpin.CEnumerationPtr(nodemap_tlstream.GetNode('StreamMode'))

        if not PySpin.IsReadable(node_stream_mode) or not PySpin.IsWritable(node_stream_mode):
            return True

        node_stream_mode_custom = PySpin.CEnumEntryPtr(node_stream_mode.GetEntryByName(stream_mode))
        if not PySpin.IsReadable(node_stream_mode_custom):
            print(f'Stream mode {stream_mode} not available. Aborting...')
            return False

        stream_mode_custom = node_stream_mode_custom.GetValue()
        node_stream_mode.SetIntValue(stream_mode_custom)
        print(f'Stream Mode set to {node_stream_mode.GetCurrentEntry().GetSymbolic()}...')
        
        return True
    
    def setup_node(self):
        # print('*** IMAGE ACQUISITION ***\n')

        nodemap = self.cam.GetNodeMap()

        node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
        if not PySpin.IsReadable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
            print('Unable to set acquisition mode to continuous. Aborting...')
            return False

        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        if not PySpin.IsReadable(node_acquisition_mode_continuous):
            print('Unable to set acquisition mode to continuous. Aborting...')
            return False

        acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
        node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
        # print('Acquisition mode set to continuous...')
    
        # set buffer handling mode to manual, set buffer count to 1
        BUFFER_COUNT = 1
        s_node_map = self.cam.GetTLStreamNodeMap()
        
        # Retrieve Buffer Handling Mode Information
        handling_mode = PySpin.CEnumerationPtr(s_node_map.GetNode('StreamBufferHandlingMode'))
        if not PySpin.IsAvailable(handling_mode) or not PySpin.IsWritable(handling_mode):
            print('Unable to set Buffer Handling mode (node retrieval). Aborting...\n')
            return False

        handling_mode_entry = PySpin.CEnumEntryPtr(handling_mode.GetCurrentEntry())
        if not PySpin.IsAvailable(handling_mode_entry) or not PySpin.IsReadable(handling_mode_entry):
            print('Unable to set Buffer Handling mode (Entry retrieval). Aborting...\n')
            return False

        # Set stream buffer Count Mode to manual
        stream_buffer_count_mode = PySpin.CEnumerationPtr(s_node_map.GetNode('StreamBufferCountMode'))
        if not PySpin.IsAvailable(stream_buffer_count_mode) or not PySpin.IsWritable(stream_buffer_count_mode):
            print('Unable to set Buffer Count Mode (node retrieval). Aborting...\n')
            return False

        stream_buffer_count_mode_manual = PySpin.CEnumEntryPtr(stream_buffer_count_mode.GetEntryByName('Manual'))
        if not PySpin.IsAvailable(stream_buffer_count_mode_manual) or not PySpin.IsReadable(stream_buffer_count_mode_manual):
            print('Unable to set Buffer Count Mode entry (Entry retrieval). Aborting...\n')
            return False

        stream_buffer_count_mode.SetIntValue(stream_buffer_count_mode_manual.GetValue())
        print('Stream Buffer Count Mode set to manual...')

        # Retrieve and modify Stream Buffer Count
        buffer_count = PySpin.CIntegerPtr(s_node_map.GetNode('StreamBufferCountManual'))
        if not PySpin.IsAvailable(buffer_count) or not PySpin.IsWritable(buffer_count):
            print('Unable to set Buffer Count (Integer node retrieval). Aborting...\n')
            return False

        # Display Buffer Info for debugging
        # print('\nDefault Buffer Handling Mode: %s' % handling_mode_entry.GetDisplayName())
        # print('Default Buffer Count: %d' % buffer_count.GetValue())
        # print('Maximum Buffer Count: %d' % buffer_count.GetMax())

        buffer_count.SetValue(BUFFER_COUNT)

        handling_mode_entry = handling_mode.GetEntryByName('NewestOnly')
        handling_mode.SetIntValue(handling_mode_entry.GetValue())
        print('\n\nBuffer Handling Mode has been set to %s' % handling_mode_entry.GetDisplayName())
        # print(buffer_count.GetValue()) # check current buffer count

        self.cam.BeginAcquisition()
        # print('Acquiring images...')

        processor = PySpin.ImageProcessor()
        processor.SetColorProcessing(PySpin.SPINNAKER_COLOR_PROCESSING_ALGORITHM_HQ_LINEAR)
        return True
    
    def connect_camera(self):
        try:
            self.cam = self.cam_list[self.cam_id_select - 1]
            self.cam.Init()
            # print("Camera connected and initialized.")
            if not self.configure_exposure_and_gain():
                print("Failed to configure exposure.")
                return False
            if not self.set_stream_mode():
                print("Failed to set stream mode.")
                return False
            if not self.setup_node():
                print("Failed to set up node.")
                return False
            else:
                return True
        except Exception as e:
            print(f"Error connecting to BFS camera: {e}")
            sys.exit()
            return False

    def capture_frame(self):
        """
        Captures a single frame from the BFS camera and returns it as a NumPy array.
        """
        try:
            # get next image from camera
            image_result = self.cam.GetNextImage(10)  # timeout of 500ms. same as in save_frame

            if image_result.IsIncomplete():
                print(f"Image incomplete with image status {image_result.GetImageStatus()}...")
                return False, None

            # image dimensions
            width = image_result.GetWidth()
            height = image_result.GetHeight()

            im_cv2_format = image_result.GetData().reshape(height, width)
            # print(f"Captured frame: width={width}, height={height}")

            # release image buffer
            image_result.Release()
            frame = cv2.cvtColor(im_cv2_format, cv2.COLOR_BAYER_BG2BGR)
            return True, frame

        except PySpin.SpinnakerException as ex:
            print(f"Error capturing frame: {ex}")
            return False, None

    def save_frame(self, full_file_path):
        print(full_file_path)

        image_result = self.cam.GetNextImage(10) # timeout of 100ms. same as in capture_frame
        if image_result.IsIncomplete():
            print(f'Image incomplete with image status {image_result.GetImageStatus()}...')
            return False
        else:
            width = image_result.GetWidth()
            height = image_result.GetHeight()
            im_cv2_format = image_result.GetData().reshape(height, width)
            cv2.imwrite(full_file_path, im_cv2_format)
            print(f'Frame saved at {full_file_path}')
            image_result.Release()
            return True

    def relese_camera(self):
        self.cam.EndAcquisition()
        if self.cam:
            self.cam.DeInit()
            del self.cam
            self.cam = None
        self.cam_list.Clear()
        self.system.ReleaseInstance()
        print("Camera released.")


# test cases
if __name__ == "__main__":
    camera = camera_frame_update_BFS(index=0)
    if camera.connect_camera():
        camera.set_stream_mode()
        camera.acquire_images()
        camera.release_camera()