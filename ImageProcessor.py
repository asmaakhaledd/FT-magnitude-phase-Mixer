import numpy as np
import cv2
import logging

# Setup logging configuration
logging.basicConfig(filename='image_processor.log', level=logging.INFO)

# Create ImageProcessor class
class ImageProcessor:
     # Constructor for ImageProcessor class
    def __init__(self):
        self.image = None 
        self.ft = None
        self.ft_shift=None
        self.modeArr = [["Real", "Imaginary"],["Imaginary", "Real"],["Magnitude", "Phase"],["Phase", "Magnitude"],["Uniform Magnitude", "Uniform Phase"],["Uniform Magnitude", "Phase"],["Phase","Uniform Magnitude" ],["Uniform Phase", "Uniform Magnitude"],["Uniform Phase", "Magnitude"],["Magnitude", "Uniform Phase"]];

  # Function to perform Fourier transform
    def perform_fft(self):
        self.ft = np.fft.fft2(self.image)
        self.ft_shift = np.fft.fftshift(self.ft)    

  # Function to open image
    def open_image(self, file) -> bool:
        print(file)
        self.image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        if self.image is None:
            logging.error(f"Failed to open image")
            return False
        logging.info(f"Opened image")
        return True

 # Function to display image
    def display_image(self, component):
        result=self.component_result(component)
        norm = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        retval, buffer = cv2.imencode('.jpg', norm)
        response = buffer.tobytes()
        logging.info(f"Applied transformation on image")
        return response

# Function to get component result
    def component_result(self, component):
        if component == "Magnitude":
            #absolute value of the complex number at each point in the Fourier transformed image. It represents the strength of the corresponding frequency component. 
            #By taking the logarithm of the magnitude, we can obtain a more visually interpretable version of the Fourier spectrum (magnitude spectrum)
            result = np.log(np.abs(self.ft_shift))
        elif component == "Phase":
            #angle of the complex number at each point in the Fourier transformed image. It represents the position of the corresponding frequency component in the image.
            result =  np.angle(self.ft_shift)
        elif component == "Real":
            result =  np.real(self.ft_shift)
        elif component == "Imaginary":
            result =  np.imag(self.ft_shift)
        # elif component == "Uniform Magnitude":
        #     magnitude = np.abs(self.ft_shift)
        #     result = np.ones_like(magnitude)
        # elif component == "Uniform Phase":
        #     phase =  np.angle(self.ft_shift)
        #     result= np.zeros_like(phase)
        elif component == "Uniform Magnitude":
            magnitude = np.abs(self.ft_shift)
            result = np.ones_like(magnitude) 
            
        elif component == "Uniform Phase":
            #Uniform phase refers to a transformation applied to the phase spectrum of an image such that all the phase values become uniformly distributed across the spectrum. This is done to remove any abrupt changes in the phase of the image, which can cause artifacts or distortions in the reconstructed image.
            phase =  np.angle(self.ft_shift)
            # #calculate the uniform phase spectrum by taking the exponential of the angle of the Fourier transform coefficients to create a phase spectrum with a more uniform distribution of values
            # uniform_phase = np.exp(1j * phase)
            # # create a new Fourier transform with a more uniform phase spectrum
            # new_ft_shift=self.ft * uniform_phase
            # #get the angle/phase of the uniform phase new ft
            # result = np.angle(new_ft_shift)
            result = np.zeros_like(phase)
        else:
            logging.warning(f"Invalid component: {component}") # warn the user of an invalid component
            return None
        return result

    # Function to return the Fourier Transform result
    def return_fft(self):
        return self.ft
    
    def return_fft_shift(self):
        return self.ft_shift

    # Function to mix two Fourier Transform components based on given ratios
    def mix_components(self, component1, component2, component1obj, component2obj, str_ratioI, str_ratioII):
        ratioI = int(str_ratioI)
        ratioII = int(str_ratioII)
        # total = ratioI + ratioII
        ratio1 = ratioI / 100
        ratio2 = ratioII / 100
        
        comp1pt1 = component1obj.component_result(component1)
        comp1pt2 = component1obj.component_result(component2)
        comp2pt1 = component2obj.component_result(component1)
        comp2pt2 = component2obj.component_result(component2)

        if component1 == "Magnitude":
            comp1pt1 = np.abs(component1obj.return_fft_shift())
        elif component2 == "Magnitude":
            comp2pt1 = np.abs(component2obj.return_fft_shift())
        #ORIGINAL
        # #good mag,phase but same img fliped in mixing 2 diff images
        # mixedpt1 = (1-ratio1) * comp1pt1 + (ratio2) * comp2pt1 
        # mixedpt2 = (ratio1) * comp1pt2 + (1-ratio2) * comp2pt2

        # #real,img fliped in mixing 2 diff images
        # mixedpt1 = (ratio1) * comp1pt1 +  (1-ratio2) * comp2pt1
        # mixedpt2 =  (1-ratio1) * comp1pt2 + (ratio2) * comp2pt2

        # # mag,phase not much if same image but if diff images it shows phases and standalone pics if one of sliders is 100%, same happens with img,real but flips if both not same ratio nor 100% nor 0%
        # mixedpt1 = (1-ratio1) * comp1pt1 + (ratio1) * comp2pt1 
        # mixedpt2 = (ratio2) * comp1pt2 + (1-ratio2) * comp2pt2

        #mag and phase not bad unexplainable tbh
        #shows img,real standalone pics if one of sliders is 100%, same happens with img,real but flips if both not same ratio nor 100% nor 0%
        mixedpt1 = (ratio1) * comp1pt1 + (1-ratio1) * comp2pt1
        mixedpt2 = (ratio2) * comp2pt2 + (1-ratio2) * comp1pt2


        # if ratio2 < 0.01:
        #     mixedpt1 = ratio1 * comp1pt1 + (1 - ratio1) * comp2pt1
        #     mixedpt2 = np.flip(comp2pt2)
        # else:
        #     mixedpt1 = ratio1 * comp1pt1 + ratio2 * comp2pt1
        #     mixedpt2 = ratio1 * comp1pt2 + ratio2 * comp2pt2

        try:
            index = self.modeArr.index([component1, component2])
            combined = np.multiply(mixedpt1, np.exp(1j * mixedpt2))
            if index == 0 or index == 1:
                combined = mixedpt1 + mixedpt2 * 1j
                
            ft_shift = np.fft.fftshift(combined)
            mixInverse = np.real(np.fft.ifft2(ft_shift))
            normalized = cv2.normalize(mixInverse, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            retval, buffer = cv2.imencode('.jpg', normalized)
            response = buffer.tobytes()
            logging.info("Applied transformation on image")
            return response
        except ValueError:
            logging.error("Invalid Fourier components")
            return None