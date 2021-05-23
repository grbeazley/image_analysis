import utilities as util
from read_lsm import read_lsm_image
from matplotlib import pyplot as plt
import numpy as np
from skimage import measure, exposure
import skimage.feature
from matplotlib.widgets import Slider

# Adds Fiji colour map
util.register_fiji_cmap('imageJ-red-black')

# Read LSM image
raw_image_data = read_lsm_image('4273', 'image 23.lsm', stack=0, channel=0)

# Put pixel values into the range 0 to 256
image_data = (raw_image_data / np.max(raw_image_data)) * 256

# Open UI to adjust image properties
util.adjustable_image(image_data)

# Set image values & adjust image
brightness = 0
mask = 34
contrast = 1.01
image_adjusted = np.clip(util.adjust_contrast(image_data * (image_data >= mask), contrast=contrast)
                         + brightness, 0, 256)

# Run edge detection on corrected image
#util.adjustable_detector(image_adjusted)

sigma = 3
area = 25

edges0 = skimage.feature.canny(image=image_adjusted, sigma=sigma)
segs0 = measure.regionprops(measure.label(edges0))
qualified_segments = []
all_coords = np.zeros([1, 2])
for seg in segs0:
    if seg.convex_area > area:
        qualified_segments.append(seg)

# areas = [s.convex_area for s in qualified_segments]
# plt.figure()
# plt.hist(areas, bins=100)
# plt.title('Distribution of vessel area')