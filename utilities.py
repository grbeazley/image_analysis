from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from matplotlib.widgets import Slider
from skimage import measure, exposure
import skimage.feature


def register_fiji_cmap_red(name):
    # Create a color map to match Fiji/ImageJ
    cdict = {'red':   ((0.0,  0.0, 0.0),
                       (0.5,  0.5, 0.5),
                       (1.0,  1.0, 1.0)),

             'green': ((0.0,  0.0, 0.0),
                       (0.5,  0.0, 0.0),
                       (1.0,  0.0, 0.0)),

             'blue':  ((0.0,  0.0, 0.0),
                       (0.5,  0.0, 0.0),
                       (1.0,  0.0, 0.0))}

    test_red_black = LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=test_red_black)


def register_fiji_cmap_green(name):
    cdict = {'red':   ((0.0,  0.0, 0.0),
                       (0.5,  0.0, 0.0),
                       (1.0,  1.0, 1.0)),

             'green': ((0.0,  0.0, 0.0),
                       (0.5,  0.5, 0.5),
                       (1.0,  1.0, 1.0)),

             'blue':  ((0.0,  0.0, 0.0),
                       (0.5,  0.0, 0.0),
                       (1.0,  0.0, 0.0))}

    test_green_black = LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=test_green_black)


def adjust_contrast(image, contrast=1):
    mid = (np.max(image) + np.min(image)) / 2
    return ((image - mid) * contrast) + mid


def mix_images(image_red, image_green):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.subplots_adjust(bottom=0.25)
    fact = 1

    # image = ((image_red - image_green) + 256) / 2
    image = np.where(image_red - (image_green) < 0, 0, image_red - (image_green))
    im1 = ax.imshow(image, cmap='imageJ-red-black')
    fig.colorbar(im1)

    axcolor = 'lightgoldenrodyellow'
    axfact = fig.add_axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

    sfact = Slider(axfact, 'Factor', 0, 2, valinit=fact, valstep=0.01)

    def _update(val):
        print(sfact.val)
        update_im = np.where(image_red - (image_green * sfact.val) < 0, 0, image_red - (image_green * sfact.val))
        # update_im = np.clip(image_red - (image_green * sfact.val), a_min=0, a_max=256)
        im1.set_data(update_im)
        fig.canvas.draw()

    sfact.on_changed(_update)
    plt.show()

#
# def adjustable_image(image):
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     fig.subplots_adjust(bottom=0.25)
#     min0 = 1
#     max0 = 0
#     brg0 = 0
#
#     im1 = ax.imshow(image, cmap='imageJ-red-black')
#     fig.colorbar(im1)
#
#     axcolor = 'lightgoldenrodyellow'
#     axmin = fig.add_axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
#     axmax = fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
#     axbrg = fig.add_axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
#
#     smin = Slider(axmin, 'Contrast', 0, 2, valinit=min0, valstep=0.01)
#     smax = Slider(axmax, 'Mask', 0, 256, valinit=max0, valstep=1)
#     sbrg = Slider(axbrg, 'Brightness', -128, 128, valinit=brg0, valstep=1)
#
#
#
#
#     smin.on_changed(_update)
#     smax.on_changed(_update)
#     sbrg.on_changed(_update)
#     plt.show()


def adjustable_detector(image):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.subplots_adjust(bottom=0.35)
    sig0 = 3
    size0 = 25

    min0 = 1
    max0 = 0
    brg0 = 0

    im1 = ax.imshow(image, cmap='imageJ-red-black')
    edges0 = skimage.feature.canny(image=image, sigma=sig0)
    segs0 = measure.regionprops(measure.label(edges0))
    all_coords = np.zeros([1, 2])
    for seg in segs0:
        if seg.convex_area > size0:
            all_coords = np.concatenate([seg.coords, all_coords])

    outlines = ax.scatter(all_coords[:, 1], all_coords[:, 0], 0.1)

    axcolor = 'lightgoldenrodyellow'
    axsig = fig.add_axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
    axsize = fig.add_axes([0.25, 0.3, 0.65, 0.03], facecolor=axcolor)

    axmin = fig.add_axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    axmax = fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
    axbrg = fig.add_axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)

    ssig = Slider(axsig, 'Sigma', 0.1, 10, valinit=sig0, valstep=0.1)
    ssize = Slider(axsize, 'Size', 0, 100, valinit=size0, valstep=1)

    smin = Slider(axmin, 'Contrast', 0, 2, valinit=min0, valstep=0.01)
    smax = Slider(axmax, 'Mask', 0, 256, valinit=max0, valstep=1)
    sbrg = Slider(axbrg, 'Brightness', -128, 128, valinit=brg0, valstep=1)

    def _update(val):
        update_im = np.clip(adjust_contrast(image * (image >= smax.val), contrast=smin.val) + sbrg.val, 0, 256)
        edges = skimage.feature.canny(image=image, sigma=ssig.val)
        segs = measure.regionprops(measure.label(edges))
        all_coords = np.zeros([1, 2])
        for seg in segs:
            if seg.convex_area > ssize.val:
                all_coords = np.concatenate([seg.coords, all_coords])

        outlines.set_offsets(np.flip(all_coords))
        im1.set_data(update_im)
        fig.canvas.draw()


    ssig.on_changed(_update)
    ssize.on_changed(_update)
    smin.on_changed(_update)
    smax.on_changed(_update)
    sbrg.on_changed(_update)
    plt.show()

