<p align="center">
  <img src="https://img.shields.io/badge/YOLO-v3%20Tiny-00D9FF?style=for-the-badge" />
  <img src="https://img.shields.io/badge/OpenCV-DNN-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.6+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</p>

<h1 align="center">Custom Object Detection with YOLO</h1>
<p align="center">
  <strong>Train YOLO to detect custom objects in real-time</strong>
</p>
<p align="center">
  A complete pipeline for training and deploying YOLOv3-Tiny to detect the Volkswagen logo—extensible to any custom object.
</p>

---

## ✨ Overview

This project demonstrates **custom object detection** using YOLO (You Only Look Once), a state-of-the-art real-time object detection algorithm. It includes everything needed to train a model from scratch and run inference on images—from dataset preparation to deployment.

### What You'll Achieve

| Goal | Description |
|------|-------------|
| 🎯 **Accurate Logo Detection** | Model learns to distinguish the target object (Volkswagen logo) from backgrounds and similar objects |
| ⚡ **Real-Time Performance** | YOLO's efficiency enables fast inference suitable for video streams and live applications |
| 🔧 **Fully Customizable** | Pipeline designed to adapt to any object class—logos, products, or custom categories |

### Use Cases

- **Automated Image Analysis** — Identify vehicles or branded assets in large image/video collections
- **Augmented Reality** — Overlay information or interactive content on detected logos
- **Brand Monitoring** — Track logo appearance in user-generated content or media
- **Quality Control** — Detect specific parts or markings in manufacturing pipelines

---

## 📸 Sample Predictions

<p align="center">
  <img src="predicitions/Screenshot%20from%202019-10-12%2022-02-42.png" width="45%" alt="Detection Example 1" />
  <img src="predicitions/Screenshot%20from%202019-10-13%2017-09-18.png" width="45%" alt="Detection Example 2" />
</p>

---

## 📁 Project Structure

```
Custom-Object-Detection-YOLO/
├── run_img.py              # Inference script (OpenCV DNN)
├── custom/
│   ├── yolov3-tiny-custom.cfg   # Model config (1 class)
│   ├── objects.names            # Class labels
│   ├── trainer.data             # Training config
│   ├── train.txt / test.txt     # Dataset splits
│   └── *.weights                # Trained weights (after training)
├── data/
│   ├── images/                  # Training images
│   │   └── parsefiles.py        # Generate train.txt paths
│   └── labels/                  # YOLO format annotations (.txt)
├── predicitions/                # Output samples
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.6+** with OpenCV (`opencv-python` + `opencv-contrib-python`)
- Trained weights (or train your own—see below)
- Linux recommended; Windows supported

### Run Detection on an Image

```bash
python run_img.py -i path/to/your/image.jpg
```

Optional arguments:

| Flag | Default | Description |
|------|---------|-------------|
| `-c` / `--config` | `custom/yolov3-tiny-custom.cfg` | YOLO config file |
| `-w` / `--weights` | `custom/yolov3-tiny-custom_30000.weights` | Trained weights |
| `-cl` / `--classes` | `custom/objects.names` | Class names file |

---

## 🛠️ Setup & Training

### 1. Install Darknet (YOLO Backend)

**Linux:**

```bash
git clone https://github.com/pjreddie/darknet
cd darknet

sudo apt-get update && sudo apt-get upgrade
sudo apt-get install build-essential cmake git libgtk2.0-dev pkg-config
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libopencv-dev

make
```

**Verify installation:**
```bash
wget https://pjreddie.com/media/files/yolov3.weights
./darknet detect cfg/yolov3.cfg yolov3.weights data/dog.jpg
```

**Windows:** See [this video guide](https://www.youtube.com/watch?v=-HtiYHpqnBs) for setup.

#### Optional: GPU + OpenCV

Edit `Makefile` in the darknet folder:
- Set `opencv=1` and `gpu=1`

Then:
```bash
sudo apt install g++-5 gcc-5
sudo apt update && sudo apt upgrade
make
```

---

### 2. Create Your Dataset

**Label images** with [labelImg](https://github.com/tzutalin/labelImg) (generates XML/Pascal VOC format).

**Convert to YOLO format** using [XmlToTxt](https://github.com/Isabek/XmlToTxt).  
- Add your class names to `classes.txt` before conversion.

**Directory layout:**
```
dataset/
├── images/       # .jpg images
└── labels/       # .txt files (YOLO format: class_id x_center y_center width height, normalized)
```

---

### 3. Configure for Training

**Create `custom/` with:**

| File | Purpose |
|------|---------|
| `objects.names` | One class name per line |
| `trainer.data` | Paths to train.txt, test.txt, names |
| `train.txt` | Absolute paths to training images |
| `test.txt` | Absolute paths to validation images (e.g., 3 images) |
| `yolov3-tiny-custom.cfg` | Copy from `darknet/cfg/yolov3-tiny.cfg` and edit |

**Generate `train.txt` with `parsefiles.py`:**

```python
# Edit img_path in data/images/parsefiles.py, then run from data/images/:
python parsefiles.py
# Move train.txt to custom/
```

**Edit `yolov3-tiny-custom.cfg`** (for 1 class):

| Location | Parameter | Value |
|----------|-----------|-------|
| Line 3 | `batch` | 24 |
| Line 4 | `subdivisions` | 8 |
| Line 127 | `filters` | 18 `(=(classes+5)*3)` |
| Line 135 | `classes` | 1 |
| Line 171 | `filters` | 18 |
| Line 177 | `classes` | 1 |

Formula: `filters = (classes + 5) * 3` (num=6 for tiny, 9 for full YOLOv3)

---

### 4. Train the Model

**Download pretrained backbone:**
```bash
wget https://pjreddie.com/media/files/darknet53.conv.74
# Place in darknet folder
```

**Start training:**
```bash
cd darknet
./darknet detector train custom/trainer.data custom/yolov3-tiny-custom.cfg darknet53.conv.74
```

- Weights save every 100 iterations (first 1000), then every 10,000
- Run for at least **30,000 iterations** for decent results

**Test trained model:**
```bash
./darknet detector test custom/trainer.data custom/yolov3-tiny-custom.cfg yolov3-tiny-custom_30000.weights dataset/01.jpg
```

---

### 5. Run Python Inference

After training, use `run_img.py` with your weights:

```bash
python run_img.py -i your_image.jpg -w custom/yolov3-tiny-custom_30000.weights
```

---

## 📦 Dependencies

```bash
pip install opencv-python opencv-contrib-python numpy
```

---

## 📄 License

This project is open source. Feel free to use, modify, and extend for your own detection tasks.

---

<p align="center">
  <strong>Train once. Detect anywhere.</strong>
</p>
