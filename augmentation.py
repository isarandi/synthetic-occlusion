#!/usr/bin/env python

import xml.etree.ElementTree
import cv2
import PIL.Image
import numpy as np
import random
import os.path
import functools
import matplotlib.pyplot as plt
import skimage.data
import sys

def show_examples():
    path = sys.argv[1]
    # path = 'something/something/VOCtrainval_11-May-2012/VOCdevkit/VOC2012'

    synth_occ = SyntheticOcclusion(pascal_voc_root_path=path)
    original_im = cv2.resize(skimage.data.astronaut(), (256,256))

    fig, axarr = plt.subplots(3,3, figsize=(7,7))
    for ax in axarr.ravel():
        occluded_im = synth_occ.augment_with_objects(original_im)
        ax.imshow(occluded_im, interpolation="none")
        ax.axis('off')

    fig.tight_layout(h_pad=0)
    # plt.savefig('examples.jpg', dpi=150, bbox_inches='tight')
    plt.show()


class SyntheticOcclusion:
    def __init__(self, pascal_voc_root_path):
        self.occluder_image_mask_pairs = []

        annotation_paths = list_filepaths(os.path.join(pascal_voc_root_path, 'Annotations'))
        print('Processing occluders from Pascal VOC dataset...')
        for annotation_path in annotation_paths:
            xml_root = xml.etree.ElementTree.parse(annotation_path).getroot()
            is_segmented = (xml_root.find('segmented').text != '0')

            if not is_segmented:
                continue

            boxes = []
            for i_obj, obj in enumerate(xml_root.findall('object')):
                is_person = (obj.find('name').text == 'person')
                is_difficult = (obj.find('difficult').text != '0')
                is_truncated = (obj.find('truncated').text != '0')
                if not is_person and not is_difficult and not is_truncated:
                    bndbox = obj.find('bndbox')
                    box = [int(bndbox.find(s).text) for s in ['xmin', 'ymin', 'xmax', 'ymax']]
                    boxes.append((i_obj, box))

            if not boxes:
                continue

            im_filename = xml_root.find('filename').text
            seg_filename = im_filename.replace('jpg', 'png')

            im_path = os.path.join(pascal_voc_root_path, 'JPEGImages', im_filename)
            seg_path = os.path.join(pascal_voc_root_path,'SegmentationObject', seg_filename)

            im = np.asarray(PIL.Image.open(im_path))
            labels = np.asarray(PIL.Image.open(seg_path))

            for i_obj, (xmin, ymin, xmax, ymax) in boxes:
                object_mask = (labels[ymin:ymax, xmin:xmax] == i_obj + 1).astype(np.uint8)
                object_image = im[ymin:ymax, xmin:xmax]
                if cv2.countNonZero(object_mask) < 500:
                    # ignore small objects
                    continue

                object_mask = soften_mask_border(object_mask)
                downscale_factor = 0.5
                object_image = resize_by_factor(object_image, downscale_factor)
                object_mask = resize_by_factor(object_mask, downscale_factor)
                self.occluder_image_mask_pairs.append((object_image, object_mask))

        # It makes sense to save `self.occluder_image_mask_pairs` on disk,
        # e.g., using pickle, to avoid recomputing it every time.
        print('Got {} objects after filtering.'.format(len(self.occluder_image_mask_pairs)))


    def augment_with_objects(self, im):
        """Returns an augmented version of `im`, containing occluders from the Pascal VOC dataset."""

        result = im.copy()

        width_height = np.asarray([im.shape[1], im.shape[0]])
        factor = min(width_height) / 256
        count = np.random.randint(1, 8)

        for _ in range(count):
            occ_im, occ_mask = random.choice(self.occluder_image_mask_pairs)

            rescale_factor = np.random.uniform(0.2, 1.0) * factor
            occ_im = resize_by_factor(occ_im, rescale_factor)
            occ_mask = resize_by_factor(occ_mask, rescale_factor)

            center = np.random.uniform([0,0], width_height)
            paste_over(occ_im, result, occ_mask, center)

        return result


def paste_over(im_src, im_dst, alpha, center):
    """Pastes `im_src` onto `im_dst` at a specified position, with alpha blending, in place.

    Locations outside the bounds of `im_dst` are handled as expected (only a part or none of
    `im_src` becomes visible).

    Args:
        im_src: The image to be pasted onto `im_dst`. Its size can be arbitrary.
        im_dst: The target image.
        alpha: A float (0.0-1.0) array of the same size as `im_src` controlling the alpha blending
            at each pixel. Large values mean more visibility for `im_src`.
        center: coordinates in `im_dst` where the center of `im_src` should be placed.
    """

    width_height_src = np.asarray([im_src.shape[1], im_src.shape[0]])
    width_height_dst = np.asarray([im_dst.shape[1], im_dst.shape[0]])

    center = np.round(center).astype(np.int32)
    raw_start_dst = center - width_height_src // 2
    raw_end_dst = raw_start_dst + width_height_src

    start_dst = np.clip(raw_start_dst, 0, width_height_dst)
    end_dst = np.clip(raw_end_dst, 0, width_height_dst)

    region_dst = im_dst[start_dst[1]:end_dst[1], start_dst[0]:end_dst[0]]

    start_src = start_dst - raw_start_dst
    end_src = width_height_src + (end_dst - raw_end_dst)

    alpha = np.expand_dims(alpha, -1)
    alpha = alpha[start_src[1]:end_src[1], start_src[0]:end_src[0]]
    region_src = im_src[start_src[1]:end_src[1], start_src[0]:end_src[0]]

    im_dst[start_dst[1]:end_dst[1], start_dst[0]:end_dst[0]] = (
            alpha * region_src + (1 - alpha) * region_dst)


def resize_by_factor(im, factor):
    """Returns a copy of `im` resized by `factor`, using bilinear interp for up and area interp
    for downscaling.
    """
    new_size = tuple(np.round(np.array([im.shape[1], im.shape[0]]) * factor).astype(int))
    interp = cv2.INTER_LINEAR if factor > 1.0 else cv2.INTER_AREA
    return cv2.resize(im, new_size, fx=factor, fy=factor, interpolation=interp)


def soften_mask_border(mask):
    """Returns a new mask, where the opacity value on an 8 pixel stripe along the mask border
    has 0.75 value.

    This is indended to make blending smoother."""

    eroded = cv2.erode(mask, get_morph_elem())
    result = mask.astype(np.float32)
    result[eroded < result] = 0.75
    return result


@functools.lru_cache()
def get_morph_elem():
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))


def list_filepaths(dirpath):
    names = os.listdir(dirpath)
    paths = [os.path.join(dirpath, name) for name in names]
    return sorted(filter(os.path.isfile, paths))

if __name__=='__main__':
    show_examples()
