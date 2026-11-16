"""A basic introduction to Open CV

Instructions
------------

Implement the functions below based on their docstrings.

Notice some docstrings include references to third-party documentation
Some docstrings **require** you to add references to third-party documentation.

Make sure you read the docstrings C.A.R.E.F.U.L.Y (yes, I took the L to check that you are awake!)
"""

# imports - add all required imports here
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import pytesseract

# Absolute path to TesseractOCR executable (tesseract.exe)
TESS_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESS_PATH

VID_PATH = Path("resources/tesseract_test.mp4")
OUT_PATH = Path("resources/images/")

class CodingVideo:
    capture: cv2.VideoCapture


    def __init__(self, video: Path | str):
        self.capture = cv2.VideoCapture(video) # You complete me!
        if not self.capture.isOpened():
            raise ValueError(f"Cannot open {video}")

        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.frame_count = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.duration = round(self.frame_count / self.fps)


    def __str__(self) -> str:
        """Displays key metadata from the video

        Specifically, the following information is shown:
            FPS - Number of frames per second rounded to two decimal points
            FRAME COUNT - The total number of frames in the video
            DURATION (minutes) - Calculated total duration of the video given FPS and FRAME COUNT

        Reference
        ----------
        https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
        """
        duration_string = str(round(self.duration / 60, 2)).replace(".", ":")
        return (f"Total Frames: {int(self.frame_count)}, " +
                f"FPS: {round(self.fps)}, " +
                f"Duration(mm:ss): {duration_string}")

    def get_frame_number_at_time(self, seconds: int) -> int:
        """Given a time in seconds, returns the value of the nearest frame"""
        return round(seconds * self.fps)


    def get_frame_rgb_array(self, frame_number: int) -> np.ndarray:
        """Returns a numpy N-dimensional array (ndarray)

        The array represents the RGB values of each pixel in a given frame

        Note: cv2 defaults to BGR format, so this function converts the color space to RGB

        Reference
        ---------
        # TODO: Find a tutorial on OpenCV that demonstrates color space conversion

        """
        # set capture cursor position to requested frame
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        # read frame data
        success, frame_data = self.capture.read()
        # convert frame data to rgb array
        frame_rgb_data = cv2.cvtColor(frame_data, cv2.COLOR_BGR2RGB)
        return frame_rgb_data

    def get_image_as_bytes(self, seconds: int) -> bytes:
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.get_frame_number_at_time(seconds))
        ok, frame = self.capture.read()
        if not ok or frame is None:
            raise ValueError("Invalid frame in target location")
        ok, buf = cv2.imencode(".png", frame)
        if not ok:
            raise ValueError("Failed to encode frame")
        return buf.tobytes()

    def save_as_image(self, seconds: int, output_path: Path | str = 'output.png') -> None:
        """
        Saves the given frame as a png image
        Parameters
        ----------
        seconds: int
        output_path: Path | str

        Returns
        -------
        None
        """
        if isinstance(output_path, str):
            output_path = f"{OUT_PATH}{output_path}"

        frame_rgb_array = self.get_frame_rgb_array(self.get_frame_number_at_time(seconds))
        frame_bgr_data = self.rgb_to_bgr(frame_rgb_array)
        try:
            # use OpenCV to write BGR data to image file in output directory
            cv2.imwrite(str(output_path), frame_bgr_data)
        except Exception as e:
            raise e

    def get_frame_text(self, seconds: int) -> str:
        """
        Gets the text from the frame at a given video timestamp (in seconds).
        Returns the text of the nearest frame.

        Parameters
        ----------
        seconds: int

        Returns
        -------
        frame_text: str
        """
        frame_time = self.get_frame_number_at_time(seconds)
        frame_data = self.get_frame_rgb_array(frame_time)
        try: # try to get text from image
            frame_text = pytesseract.image_to_string(frame_data, lang="eng")
            return frame_text
        except Exception as e: # if e
            raise e


    @staticmethod
    def rgb_to_bgr(rgb_data):
        return cv2.cvtColor(rgb_data, cv2.COLOR_RGB2BGR)

    @staticmethod
    def bgr_to_rgb(self, brg_data):
        return cv2.cvtColor(brg_data, cv2.COLOR_BGR2RGB)

def test():
    """Try out your class here"""
    tess_test = CodingVideo("resources/tesseract_test.mp4")
    print(tess_test)
    tess_test.save_as_image(3)

if __name__ == '__main__':
    test()
