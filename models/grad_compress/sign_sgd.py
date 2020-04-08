import numpy as np
import pickle

from utils.logger import Logger

logger = Logger().get_logger()

class SignSGDUpdate:

    def GradientCompress(self, gradient_list):
        # with open('grad_list.pkl', 'wb') as f:
        #     pickle.dump(gradient_list, f)
        compressed_gradient_list = []
        element_num = 0
        for gradient in gradient_list:
            # logger.info("gradiant = {}".format(type(gradient)))
            # continue
            element_num += np.size(gradient)
            compressed_gradient_list.append(np.sign(gradient))

        return compressed_gradient_list, element_num * 32,  element_num
    
    def MajorityVote(self, gradient_list):
        compressed_gradient_list = []
        for gradient in gradient_list:
            compressed_gradient_list.append(np.sign(gradient))

        return compressed_gradient_list

sign_sgd_updater = SignSGDUpdate()