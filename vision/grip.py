import cv2
import numpy
import math
from enum import Enum

class RedPipeline:
    """
    An OpenCV pipeline generated by GRIP.
    """
    
    def __init__(self):
        """initializes all values to presets or None if need to be set
        """

        self.__resize_image_width = 400.0
        self.__resize_image_height = 200.0
        self.__resize_image_interpolation = cv2.INTER_CUBIC

        self.resize_image_output = None

        self.__hsv_threshold_input = self.resize_image_output
        self.__hsv_threshold_hue = [0.0, 18.03056027164685]
        self.__hsv_threshold_saturation = [155.93525179856115, 255.0]
        self.__hsv_threshold_value = [204.09172661870502, 255.0]

        self.hsv_threshold_output = None

        self.__cv_erode_src = self.hsv_threshold_output
        self.__cv_erode_kernel = None
        self.__cv_erode_anchor = (-1, -1)
        self.__cv_erode_iterations = 1.0
        self.__cv_erode_bordertype = cv2.BORDER_CONSTANT
        self.__cv_erode_bordervalue = (-1)

        self.cv_erode_output = None

        self.__find_lines_input = self.cv_erode_output

        self.find_lines_output = None

        self.__filter_lines_lines = self.find_lines_output
        self.__filter_lines_min_length = 2.0
        self.__filter_lines_angle = [171.58273381294964, 198.03056027164686]

        self.filter_lines_output = None


    def process(self, source0):
        """
        Runs the pipeline and sets all outputs to new values.
        """
        # Step Resize_Image0:
        self.__resize_image_input = source0
        (self.resize_image_output) = self.__resize_image(self.__resize_image_input, self.__resize_image_width, self.__resize_image_height, self.__resize_image_interpolation)

        # Step HSV_Threshold0:
        self.__hsv_threshold_input = self.resize_image_output
        (self.hsv_threshold_output) = self.__hsv_threshold(self.__hsv_threshold_input, self.__hsv_threshold_hue, self.__hsv_threshold_saturation, self.__hsv_threshold_value)

        # Step CV_erode0:
        self.__cv_erode_src = self.hsv_threshold_output
        (self.cv_erode_output) = self.__cv_erode(self.__cv_erode_src, self.__cv_erode_kernel, self.__cv_erode_anchor, self.__cv_erode_iterations, self.__cv_erode_bordertype, self.__cv_erode_bordervalue)

        # Step Find_Lines0:
        self.__find_lines_input = self.cv_erode_output
        (self.find_lines_output) = self.__find_lines(self.__find_lines_input)

        # Step Filter_Lines0:
        self.__filter_lines_lines = self.find_lines_output
        (self.filter_lines_output) = self.__filter_lines(self.__filter_lines_lines, self.__filter_lines_min_length, self.__filter_lines_angle)

        return self.filter_lines_output


    @staticmethod
    def __resize_image(input, width, height, interpolation):
        """Scales and image to an exact size.
        Args:
            input: A numpy.ndarray.
            Width: The desired width in pixels.
            Height: The desired height in pixels.
            interpolation: Opencv enum for the type fo interpolation.
        Returns:
            A numpy.ndarray of the new size.
        """
        return cv2.resize(input, ((int)(width), (int)(height)), 0, 0, interpolation)

    @staticmethod
    def __hsv_threshold(input, hue, sat, val):
        """Segment an image based on hue, saturation, and value ranges.
        Args:
            input: A BGR numpy.ndarray.
            hue: A list of two numbers the are the min and max hue.
            sat: A list of two numbers the are the min and max saturation.
            lum: A list of two numbers the are the min and max value.
        Returns:
            A black and white numpy.ndarray.
        """
        out = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)
        return cv2.inRange(out, (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))

    @staticmethod
    def __cv_erode(src, kernel, anchor, iterations, border_type, border_value):
        """Expands area of lower value in an image.
        Args:
           src: A numpy.ndarray.
           kernel: The kernel for erosion. A numpy.ndarray.
           iterations: the number of times to erode.
           border_type: Opencv enum that represents a border type.
           border_value: value to be used for a constant border.
        Returns:
            A numpy.ndarray after erosion.
        """
        return cv2.erode(src, kernel, anchor, iterations = (int) (iterations +0.5),
                            borderType = border_type, borderValue = border_value)

    class Line:

        def __init__(self, x1, y1, x2, y2):
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2

        def length(self):
            return numpy.sqrt(pow(self.x2 - self.x1, 2) + pow(self.y2 - self.y1, 2))

        def angle(self):
            return math.degrees(math.atan2(self.y2 - self.y1, self.x2 - self.x1))
    @staticmethod
    def __find_lines(input):
        """Finds all line segments in an image.
        Args:
            input: A numpy.ndarray.
        Returns:
            A filtered list of Lines.
        """
        detector = cv2.createLineSegmentDetector()
        if (len(input.shape) == 2 or input.shape[2] == 1):
            lines = detector.detect(input)
        else:
            tmp = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
            lines = detector.detect(tmp)
        output = []
        if len(lines) != 0:
            for i in range(1, len(lines[0])):
                tmp = RedPipeline.Line(lines[0][i, 0][0], lines[0][i, 0][1],
                                lines[0][i, 0][2], lines[0][i, 0][3])
                output.append(tmp)
        return output

    @staticmethod
    def __filter_lines(inputs, min_length, angle):
        """Filters out lines that do not meet certain criteria.
        Args:
            inputs: A list of Lines.
            min_Lenght: The minimum lenght that will be kept.
            angle: The minimum and maximum angles in degrees as a list of two numbers.
        Returns:
            A filtered list of Lines.
        """
        outputs = []
        for line in inputs:
            if (line.length() > min_length):
                if ((line.angle() >= angle[0] and line.angle() <= angle[1]) or
                        (line.angle() + 180.0 >= angle[0] and line.angle() + 180.0 <= angle[1])):
                    outputs.append(line)
        return outputs



class BluePipeline:
    """
    An OpenCV pipeline generated by GRIP.
    """
    
    def __init__(self):
        """initializes all values to presets or None if need to be set
        """

        self.__resize_image_width = 400.0
        self.__resize_image_height = 200.0
        self.__resize_image_interpolation = cv2.INTER_CUBIC

        self.resize_image_output = None

        self.__hsv_threshold_input = self.resize_image_output
        self.__hsv_threshold_hue = [76.07913669064747, 130.79066155976753]
        self.__hsv_threshold_saturation = [98.60611510791367, 255.0]
        self.__hsv_threshold_value = [61.915467625899275, 255.0]

        self.hsv_threshold_output = None

        self.__cv_erode_src = self.hsv_threshold_output
        self.__cv_erode_kernel = None
        self.__cv_erode_anchor = (-1, -1)
        self.__cv_erode_iterations = 1.0
        self.__cv_erode_bordertype = cv2.BORDER_CONSTANT
        self.__cv_erode_bordervalue = (-1)

        self.cv_erode_output = None

        self.__find_lines_input = self.cv_erode_output

        self.find_lines_output = None

        self.__filter_lines_lines = self.find_lines_output
        self.__filter_lines_min_length = 2.0
        self.__filter_lines_angle = [171.58273381294964, 191.918505942275]

        self.filter_lines_output = None


    def process(self, source0):
        """
        Runs the pipeline and sets all outputs to new values.
        """
        # Step Resize_Image0:
        self.__resize_image_input = source0
        (self.resize_image_output) = self.__resize_image(self.__resize_image_input, self.__resize_image_width, self.__resize_image_height, self.__resize_image_interpolation)

        # Step HSV_Threshold0:
        self.__hsv_threshold_input = self.resize_image_output
        (self.hsv_threshold_output) = self.__hsv_threshold(self.__hsv_threshold_input, self.__hsv_threshold_hue, self.__hsv_threshold_saturation, self.__hsv_threshold_value)

        # Step CV_erode0:
        self.__cv_erode_src = self.hsv_threshold_output
        (self.cv_erode_output) = self.__cv_erode(self.__cv_erode_src, self.__cv_erode_kernel, self.__cv_erode_anchor, self.__cv_erode_iterations, self.__cv_erode_bordertype, self.__cv_erode_bordervalue)

        # Step Find_Lines0:
        self.__find_lines_input = self.cv_erode_output
        (self.find_lines_output) = self.__find_lines(self.__find_lines_input)

        # Step Filter_Lines0:
        self.__filter_lines_lines = self.find_lines_output
        (self.filter_lines_output) = self.__filter_lines(self.__filter_lines_lines, self.__filter_lines_min_length, self.__filter_lines_angle)

        return self.filter_lines_output


    @staticmethod
    def __resize_image(input, width, height, interpolation):
        """Scales and image to an exact size.
        Args:
            input: A numpy.ndarray.
            Width: The desired width in pixels.
            Height: The desired height in pixels.
            interpolation: Opencv enum for the type fo interpolation.
        Returns:
            A numpy.ndarray of the new size.
        """
        return cv2.resize(input, ((int)(width), (int)(height)), 0, 0, interpolation)

    @staticmethod
    def __hsv_threshold(input, hue, sat, val):
        """Segment an image based on hue, saturation, and value ranges.
        Args:
            input: A BGR numpy.ndarray.
            hue: A list of two numbers the are the min and max hue.
            sat: A list of two numbers the are the min and max saturation.
            lum: A list of two numbers the are the min and max value.
        Returns:
            A black and white numpy.ndarray.
        """
        out = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)
        return cv2.inRange(out, (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))

    @staticmethod
    def __cv_erode(src, kernel, anchor, iterations, border_type, border_value):
        """Expands area of lower value in an image.
        Args:
           src: A numpy.ndarray.
           kernel: The kernel for erosion. A numpy.ndarray.
           iterations: the number of times to erode.
           border_type: Opencv enum that represents a border type.
           border_value: value to be used for a constant border.
        Returns:
            A numpy.ndarray after erosion.
        """
        return cv2.erode(src, kernel, anchor, iterations = (int) (iterations +0.5),
                            borderType = border_type, borderValue = border_value)

    class Line:

        def __init__(self, x1, y1, x2, y2):
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2

        def length(self):
            return numpy.sqrt(pow(self.x2 - self.x1, 2) + pow(self.y2 - self.y1, 2))

        def angle(self):
            return math.degrees(math.atan2(self.y2 - self.y1, self.x2 - self.x1))
    @staticmethod
    def __find_lines(input):
        """Finds all line segments in an image.
        Args:
            input: A numpy.ndarray.
        Returns:
            A filtered list of Lines.
        """
        detector = cv2.createLineSegmentDetector()
        if (len(input.shape) == 2 or input.shape[2] == 1):
            lines = detector.detect(input)
        else:
            tmp = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
            lines = detector.detect(tmp)
        output = []
        if len(lines) != 0:
            for i in range(1, len(lines[0])):
                tmp = BluePipeline.Line(lines[0][i, 0][0], lines[0][i, 0][1],
                                lines[0][i, 0][2], lines[0][i, 0][3])
                output.append(tmp)
        return output

    @staticmethod
    def __filter_lines(inputs, min_length, angle):
        """Filters out lines that do not meet certain criteria.
        Args:
            inputs: A list of Lines.
            min_Lenght: The minimum lenght that will be kept.
            angle: The minimum and maximum angles in degrees as a list of two numbers.
        Returns:
            A filtered list of Lines.
        """
        outputs = []
        for line in inputs:
            if (line.length() > min_length):
                if ((line.angle() >= angle[0] and line.angle() <= angle[1]) or
                        (line.angle() + 180.0 >= angle[0] and line.angle() + 180.0 <= angle[1])):
                    outputs.append(line)
        return outputs



