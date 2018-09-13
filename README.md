# Synthetic Occlusion Data Augmentation

![Occlusion augmented examples](examples.jpg)

In deep learning for computer vision, augmenting input images with synthetic occluders is an effective regularization method.

This is the implementation we used for our IROS'18 workshop paper [1], and to achieve first place in the 2018 ECCV PoseTrack Challenge on 3D human pose estimation (method description and results can be found in [2]). Consider citing any of the above-mentioned papers if you find the method useful in your research.

Contact: sarandi@vision.rwth-aachen.de

## Usage
0. Make sure Python 3, Numpy, OpenCV 3 and Pillow are installed.
1. Download and extract the Pascal VOC training/validation data from http://host.robots.ox.ac.uk/pascal/VOC/voc2012/#devkit
2. Use the `SyntheticOcclusion` class as in the `augmentation.show_examples` function. In short:

```python

original_im = cv2.resize(skimage.data.astronaut(), (256,256))

synth_occ = SyntheticOcclusion(pascal_voc_root_path=PATH_TO_THE_EXTRACTED_VOC2012_DIR)
occluded_im = synth_occ.augment_with_objects(original_im)
```

## References

[1] I. Sárándi; T. Linder; K. O. Arras; B. Leibe: "How Robust is 3D Human Pose Estimation to Occlusion?" Accepted for IEEE/RSJ Int. Conference on Intelligent Robots and Systems (IROS'18) Workshops, to appear (2018) Arxiv:

```
@inproceedings{Sarandi18IROSW,
  title = {How Robust is 3{D} Human Pose Estimation to Occlusion?},
  author = {Istv\'an S\'ar\'andi and Timm Linder and Kai O. Arras and Bastian Leibe},
  booktitle = {IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) Workshops},
  year = {2018},
  note = {arXiv:1808.09316}
}
```

[2] I. Sárándi; T. Linder; K. O. Arras; B. Leibe: "Synthetic Occlusion Augmentation with Volumetric Heatmaps for the 2018 PoseTrack Challenge on 3D Human Pose Estimation" (2018) Arxiv:

```
@article{Sarandi18arxiv,
  title = {Synthetic Occlusion Augmentation with Volumetric Heatmaps for the 2018 {P}ose{T}rack {C}hallenge on 3{D} Human Pose Estimation},
  author = {Istv\'an S\'ar\'andi and Timm Linder and Kai O. Arras and Bastian Leibe},
  journal={arXiv:},
  year={2018}
}
```
