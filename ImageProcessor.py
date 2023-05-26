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
        self.modeArr = [["Real", "Imaginary"],["Imaginary", "Real"],["Uniform Magnitude", "Uniform Phase"],["Uniform Magnitude", "Phase"],["Phase","Uniform Magnitude" ],["Uniform Phase", "Uniform Magnitude"],["Uniform Phase", "Magnitude"],["Magnitude", "Uniform Phase"],["Magnitude", "Phase"],["Phase", "Magnitude"]];
        # self.modeArr = [["Real", "Imaginary"],["Imaginary", "Real"]];
        self.inverse_fourier = None


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

    def apply_uniform_mode(self,uniform_value, original_value, ratio):
            return (uniform_value * ratio) + (original_value * (1 - ratio))
    # Function to mix two Fourier Transform components based on given ratios
    
    # def mix_components(self, component1obj: 'ImageProcessor', component2obj: 'ImageProcessor', str_ratioI: float, str_ratioII: float):

    #     # Get Fourier parameters for each image
    #     Fourier_components = {
    #         "Magnitude": [component1obj.component_result("Magnitude"), component2obj.component_result("Magnitude")],
    #         "Phase": [component1obj.component_result("Phase"), component2obj.component_result("Phase")],
    #         "Real": [component1obj.component_result("Real"), component2obj.component_result("Real")],
    #         "Imaginary": [component1obj.component_result("Imaginary"), component2obj.component_result("Imaginary")],
    #     }

    #     # Mix the Fourier parameters based on the given ratios
    #     mixed_Fourier_components = {
    #         "Magnitude": self.apply_uniform_mode(Fourier_components["Magnitude"][0], Fourier_components["Magnitude"][1], str_ratioI),
    #         "Phase": self.apply_uniform_mode(Fourier_components["Phase"][0], Fourier_components["Phase"][1], str_ratioII),
    #         "Real": self.apply_uniform_mode(Fourier_components["Real"][0], Fourier_components["Real"][1], str_ratioI),
    #         "Imaginary": self.apply_uniform_mode(Fourier_components["Imaginary"][0], Fourier_components["Imaginary"][1], str_ratioII),
    #     }

    #     # Combine the mixed Fourier parameters into a single Fourier transform
    #     mixed_Fourier = mixed_Fourier_components["Magnitude"] * np.exp(1j * mixed_Fourier_components["Phase"])
    #     mixed_Fourier = mixed_Fourier + (mixed_Fourier_components["Real"] + 1j * mixed_Fourier_components["Imaginary"])

    #     # Perform inverse Fourier transform on the mixed Fourier transform
    #     mixed_image = np.fft.ifft2(mixed_Fourier)
    #     mixed_image = np.abs(mixed_image)

    #     return mixed_image
     
    def inverse_fourier_transform(self, component):
        # Perform inverse Fourier transform on the mixed Fourier transform
        mixed_image = np.fft.ifft2(component)
        mixed_image = np.abs(mixed_image)
        return mixed_image
    

    # def inverse_fourier_transform(self, image):
    #     # Compute the inverse Fourier transform of the image
    #     image = np.fft.ifftshift(image)
    #     image = ifft2(image)
    #     image = np.abs(image)
    #     image = np.uint8(image)
    #     return image
    
    def mix_components(self,component_image_1, component_image_2 ,component1obj: 'ImageProcessor', component2obj: 'ImageProcessor', str_ratioI: float, str_ratioII: float):
        """
        Mixes two images by combining their Fourier domain components based on user-specified ratios and components.

        Parameters:
        component1obj (Images): The first image object.
        component2obj (Images): The second image object.
        str_ratioI (float): The ratio of the first image component to mix.
        str_ratioII (float): The ratio of the second image component to mix.

        Returns:
        Mixed_img (np.ndarray): The mixed image as a numpy array.
        """

        # self.modeArr = [["Real", "Imaginary"], ["Imaginary", "Real"], ["Uniform Magnitude", "Uniform Phase"],
        #                 ["Uniform Magnitude", "Phase"], ["Phase", "Uniform Magnitude"], ["Uniform Phase", "Uniform Magnitude"],
        #                 ["Uniform Phase", "Magnitude"], ["Magnitude", "Uniform Phase"], ["Magnitude", "Phase"], ["Phase", "Magnitude"]]

        for mode in self.modeArr:
            component_image_1, component_image_2 = mode

            # Get Fourier parameters for each image
            Fourier_components = {
                "Magnitude": [component1obj.component_result("Magnitude"), component2obj.component_result("Magnitude")],
                "Phase": [component1obj.component_result("Phase"), component2obj.component_result("Phase")],
                "Real": [component1obj.component_result("Real"), component2obj.component_result("Real")],
                "Imaginary": [component1obj.component_result("Imaginary"), component2obj.component_result("Imaginary")],
                "Uniform phase": [component1obj.component_result("Uniform phase"), component2obj.component_result("Uniform phase")],
                "Uniform magnitude": [component1obj.component_result("Uniform magnitude"), component2obj.component_result("Uniform magnitude")]
            }

            str_ratioI = float(str_ratioI) / 100
            str_ratioII = float(str_ratioII) / 100


            # Mix the components based on user-specified ratios and components
            if (component_image_1 in ["Real"] and component_image_2 in ["Imaginary"]) or (component_image_1 in ["Imaginary"] and component_image_2 in ["Real"]):
                New_real = Fourier_components[component_image_1][0] * str_ratioI + Fourier_components[component_image_1][1] * (1 - str_ratioI)
                New_Imag = Fourier_components[component_image_2][1] * str_ratioII + Fourier_components[component_image_2][0] * (1 - str_ratioII)
                ratio_tuples = [New_real, New_Imag] if component_image_1 == "Real" else [New_Imag, New_real]
                Mixed_FT = ratio_tuples[0] + 1j * ratio_tuples[1]

            elif (component_image_1 in ["Magnitude", "Uniform magnitude"] and component_image_2 in ["Phase", "Uniform phase"]) or (component_image_1 in ["Phase", "Uniform phase"] and component_image_2 in ["Magnitude", "Uniform magnitude"]):
                ratio_tuples = ["Magnitude", "Phase"] if component_image_1 in ["Magnitude", "Uniform magnitude"] else ["Phase", "Magnitude"]
                Mixed_Mag = Fourier_components[component_image_1][0] * str_ratioI + Fourier_components[ratio_tuples[0]][1] * (1 - str_ratioI)

                Mixed_Phase = Fourier_components[component_image_2][1] * str_ratioII + Fourier_components[ratio_tuples[1]][0] * (1 - str_ratioII)
                ratio_tupless = [Mixed_Mag, Mixed_Phase] if component_image_1 in ["Magnitude", "Uniform magnitude"] else [Mixed_Phase, Mixed_Mag]
                Mixed_FT = np.multiply(ratio_tupless[0], np.exp(1j * ratio_tupless[1]))

            else:
                continue

            Image_combined = self.inverse_fourier_transform(Mixed_FT)
            Image_combined = cv2.normalize(Image_combined, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            retval, buffer = cv2.imencode('.jpg', Image_combined)
            response = buffer.tobytes()
            logging.info("Applied transformation on image")
            return response
            