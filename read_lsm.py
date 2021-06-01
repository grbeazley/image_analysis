import lsmreader
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from skimage import measure, exposure
import skimage.feature
import skimage.viewer
import cv2


def read_lsm_image(folder, filename, **kwargs):
    """
    Reads an image of .lsm file type
    :param folder: name of the folder
    :param filename: name of file in the folder directory
    :param kwargs: specify kwargs to pass to the get_image() function
    :return: image file as a numpy array
    """

    if filename[-4:] == '.lsm':
        image_file = lsmreader.Lsmimage(f'{folder}//{filename}')
        image_file.open()
        return image_file.get_image(**kwargs)

    elif filename[-4:] == '.jpg':
        return cv2.imread(f'{folder}//{filename}', 0)


# from PIL import Image, ImageEnhance
#
# import sys
# from scipy import ndimage
#
#
# # imageData_2 = imageFile.get_image(stack=0, channel=1)
# # imageData_3 = imageFile.get_image(stack=0, channel=2)
#
# # imageData_1 = np.clip((imageData_1_raw / 2**7) * 2, None, 256)
# # imageData_1 = imageData_1_raw / 2**7
#
# # Remove highest intensity values? and scale to 0 -> 256
# # imageData_1 = (np.clip(imageData_1_raw, 0, 10000) / 10000) * 256
#
# # compute_area = 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))
#
#
#
# # im = Image.fromarray(imageData_1)
# # enhancer = ImageEnhance.Contrast(im)
#
# # plt.hist(imageData_1.flatten())
#
#
# # im.save('testImage.png')
# plt.figure()
# plt.imshow(imageData_1_adj, 'imageJ-red-black')
# plt.title('Raw (ish)')
#
# # plt.figure()
# # plt.imshow(imageData_2)
# #
# # plt.figure()
# # plt.imshow(imageData_3)
#
# plt.figure()
# plt.hist(imageData_1.flatten(), bins=100)
#
# # plt.figure()
# # lowpass = ndimage.gaussian_filter(imageData_1, 3)
# # gauss_highpass = imageData_1 - lowpass
# # plt.imshow(gauss_highpass, 'test_red_black')
# #
# # plt.show()
#
# sigma = 3.0
# low_threshold = 0.01
# high_threshold = 1.0
#
# sigmas = [0.1, 0.5, 1, 2, 3, 5, 8, 10, 15]
# low_thresholds = [0, 0.5, 1]
# high_thresholds = [0.5, 1, 1.5]
#
# fig, axs = plt.subplots(3, 3)
#
# for idx, sigma in enumerate(sigmas):
#
#     edges = skimage.feature.canny(
#         image=imageData_1,
#         sigma=sigma,
#         low_threshold=low_threshold,
#         high_threshold=high_threshold,
#     )
#     # plt.figure()
#     axs[idx // 3, idx % 3].imshow(edges)
#     # plt.imshow(edges)
#     axs[idx // 3, idx % 3].set_title(r'Edge Detection $\sigma = $' + str(sigma))
#
#
# for ax in axs.flat:
#     ax.label_outer()
#
# fig, axs = plt.subplots(3, 3)
# idx = 0
# for low_thresh in low_thresholds:
#     for high_thresh in high_thresholds:
#         edges = skimage.feature.canny(
#             image=imageData_1,
#             sigma=9
#         )
#         # plt.figure()
#         axs[idx // 3, idx % 3].imshow(edges)
#         # plt.imshow(edges)
#         axs[idx // 3, idx % 3].set_title(r'Edge Detection Low Thresh ' + str(low_thresh) + ' , High Thresh ' + str(high_thresh))
#         idx += 1
#
# edges = skimage.feature.canny(
#     image=imageData_1,
#     sigma=3,
#     low_threshold=low_threshold,
#     high_threshold=high_threshold,
# )
#
# # props = measure.regionprops(edges)
# x = measure.regionprops(measure.label(edges))
#
# # x[26].convex_area
# # x[26].filled_area
# # x[26].area
#
# plt.figure()
# plt.imshow(edges)
# plt.scatter(x[1].coords[:, 1], x[1].coords[:, 0])
#
# plt.figure()
# plt.imshow(imageData_1_adj, 'test_red_black')
# plt.imshow(edges, alpha=0.3)
# # measure.regionprops(measure.label(edges))
#
# plt.figure()
# imageData_1_adj_thresh = imageData_1_adj
# imageData_1_adj_thresh[imageData_1_adj <= 200] = 0
# plt.imshow(imageData_1_adj_thresh, 'test_red_black')
#
# edges = skimage.feature.canny(
#     image=imageData_1_adj_thresh,
#     sigma=3.5,
# )
#
# plt.figure()
# plt.imshow(imageData_1_adj, 'test_red_black')
# plt.imshow(edges, alpha=0.3)

