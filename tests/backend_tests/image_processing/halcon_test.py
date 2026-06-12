
import halcon as ha

class method5:
    def __init__(self,image_path):
        self.image_path = image_path # dummy variable
        #self.image = ha.read_image(r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2D_optical_vision_mapping\assets\logos\PBA_logo.png")
        self.image = ha.read_image(r"C:\Users\mj.j\AppData\Roaming\MVTec\HALCON-24.05-Progress\examples\images\Pic_2024_05_30_144018_1")

    def calculate_reagens(self):
        region = ha.threshold(self.image_path, 0, 122)
        num_regions = ha.count_obj(ha.connection(region))
        print(f'Number of Regions: {num_regions}')

    def calculate_center(self):
        self.width,self.height=ha.get_image_size_s(self.image)
        print(self.width,self.height)

        # define the dot location
        Define_Circle_Row = 100     
        Define_Circle_Column = 2100
        ha.gen_cross_contour_xld ( Define_Circle_Row, Define_Circle_Column, 30, 0.785398)
        CircleInitRadius = 90
        CircleRadiusTolerance = 20

        MetrologyHandle = ha.create_metrology_model()
        ha.set_metrology_model_image_size (MetrologyHandle, self.width, self.height)
        # MetrologyCircleIndices = ha.add_metrology_object_circle_measure (MetrologyHandle, Define_Circle_Row , Define_Circle_Column, CircleInitRadius, CircleRadiusTolerance, Thichness_of_the_box, sigma, measure_threshold, ['measure_distance'], [50] )
        MetrologyCircleIndices = ha.add_metrology_object_circle_measure (MetrologyHandle, Define_Circle_Row , Define_Circle_Column, CircleInitRadius, CircleRadiusTolerance, 20, 0.5, 1.8, ['measure_distance'], [50] )
        ha.set_metrology_object_param (MetrologyHandle, MetrologyCircleIndices, 'measure_transition', 'uniform')
        ha.apply_metrology_model (self.image, MetrologyHandle)
        CircleParameter = ha.get_metrology_object_result(MetrologyHandle, MetrologyCircleIndices, 'all', 'result_type', 'all_param')
        print(CircleParameter)

if __name__ == '__main__':
    #img = ha.read_image('pcb')
    img = "test"
    calculator = method5(img)
    #calculator.calculate_reagens() 
    calculator.calculate_center()

