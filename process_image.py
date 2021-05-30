import utilities as util
from read_lsm import read_lsm_image
from matplotlib import pyplot as plt
import numpy as np
from skimage import measure, exposure
import skimage.feature
from matplotlib.widgets import Slider

# Adds Fiji colour map
util.register_fiji_cmap_red('imageJ-red-black')
util.register_fiji_cmap_green('imageJ-green-black')

# Read LSM image
folder_name = '4275'
image_name = 'image 21.lsm'

raw_image_data_red = read_lsm_image(folder_name, image_name, stack=0, channel=0)
raw_image_data_green = read_lsm_image(folder_name, image_name, stack=0, channel=1)

# Put pixel values into the range 0 to 256
image_data_red = (raw_image_data_red / np.max(raw_image_data_red)) * 256
image_data_green = (raw_image_data_green / np.max(raw_image_data_green)) * 256

# image_data = image_data_red

# Open UI to adjust mixing
util.mix_images(image_data_red, image_data_green)
# plt.figure()
# plt.imshow(image_data_red, cmap='imageJ-red-black')
# plt.show()
# plt.figure()
# plt.imshow(image_data_green, cmap='imageJ-green-black')
# plt.show()

# plt.figure()
# plt.imshow(np.abs(image_data_red - image_data_green), cmap='imageJ-green-black')
# plt.show()

fact = 1
image_data = image_data_red - (image_data_green * fact)

# plt.figure()
# plt.hist(image_data.flatten(), bins=100)
# plt.show()

# Open UI to adjust image properties
# util.adjustable_image(image_data)

# Run edge detection on corrected image
# util.adjustable_detector(image_data)

# Set image values & adjust image
brightness = 47
mask = 22
contrast = 1.33
image_adjusted = np.clip(util.adjust_contrast(image_data * (image_data >= mask), contrast=contrast)
                         + brightness, 0, 256)

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
