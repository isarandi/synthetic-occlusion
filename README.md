# Synthetic Occlusion Data Augmentation

![Occlusion augmented examples](examples.jpg)

In deep learning for computer vision, augmenting input images with synthetic occluders is an effective regularization method.

This is the implementation we used for our IROS'18 workshop paper [1], and to achieve first place in the 2018 ECCV PoseTrack Challenge on 3D human pose estimation (method description and results can be found in [2]). Consider citing any of the above-mentioned papers if you find the method useful in your research.

Contact: sarandi@vision.rwth-aachen.de

## Usage
0. Make sure you have installed Python 3, the scientific Python stack, OpenCV and Pillow.
1. Clone the repo.
2. Download and extract the Pascal VOC training/validation data (2 GB) from http://host.robots.ox.ac.uk/pascal/VOC/voc2012/#devkit
3. Test if it works.

All this in terminal commands:

```bash
git clone https://github.com/isarandi/synthetic-occlusion.git
cd synthetic-occlusion

wget http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar
tar -xf VOCtrainval_11-May-2012.tar

./augmentation.py "VOCdevkit/VOC2012"
```

4. Use the `SyntheticOcclusion` class as follows:

```python 
synth_occ = SyntheticOcclusion(pascal_voc_root_path=PATH_TO_THE_EXTRACTED_VOC2012_DIR)

# Load your image
original_im = np.random.randint(0,255, size=(256,256,3), dtype=np.uint8)
occluded_im = synth_occ.augment_with_objects(im)
```


## References

[1] I. Sárándi; T. Linder; K. O. Arras; B. Leibe: "[How Robust is 3D Human Pose Estimation to Occlusion?](https://arxiv.org/abs/1808.09316)" Accepted for IEEE/RSJ Int. Conference on Intelligent Robots and Systems (IROS'18) Workshops, to appear (2018) arXiv:1808.09316

```
@inproceedings{Sarandi18IROSW,
  title = {How Robust is 3{D} Human Pose Estimation to Occlusion?},
  author = {Istv\'an S\'ar\'andi and Timm Linder and Kai O. Arras and Bastian Leibe},
  booktitle = {IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) Workshops},
  year = {2018},
  note = {arXiv:1808.09316}
}
```

[2] I. Sárándi; T. Linder; K. O. Arras; B. Leibe: "Synthetic Occlusion Augmentation with Volumetric Heatmaps for the 2018 PoseTrack Challenge on 3D Human Pose Estimation" (2018) arXiv:

```
@article{Sarandi18PoseTrack,
  title = {Synthetic Occlusion Augmentation with Volumetric Heatmaps for the 2018 {P}ose{T}rack {C}hallenge on 3{D} Human Pose Estimation},
  author = {Istv\'an S\'ar\'andi and Timm Linder and Kai O. Arras and Bastian Leibe},
  journal={arXiv:},
  year={2018}
}
```
