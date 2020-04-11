import numpy as np
from grad_compress.compressor import Compressor

# gradient_list: type  list
# gradient_list[0]: type  numpy.ndarray

class GDropUpdate(Compressor):
    def __init__(self, threshold=0.005):
        self.delta_gradient_list = []
        self.threshold = threshold
        super(GDropUpdate, self).__init__()

    def GradientCompress(self, gradient_list):
        if len(self.delta_gradient_list)==0:
            for i in range(len(gradient_list)):
                self.delta_gradient_list.append(gradient_list[i]*0)
        compressed_gradient_list = []
        element_num = 0
        compressed_element_num = 0
        for i in range(len(gradient_list)):
            gradient = gradient_list[i]
            element_num += np.size(gradient)
            gradient += self.delta_gradient_list[i]
            sign_gradient = np.sign((np.abs(gradient)/self.threshold).astype(np.int32))
            compressed_element_num += np.sum(sign_gradient)
            compressed_gradient = gradient*sign_gradient
            compressed_gradient_list.append(compressed_gradient)
            self.delta_gradient_list[i] = gradient - compressed_gradient

        #print(compressed_element_num/element_num)
        return compressed_gradient_list, element_num * 32,  compressed_element_num*32


grad_drop_updater = GDropUpdate(0.005)

