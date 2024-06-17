[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/) [![PyPI-Server](https://img.shields.io/pypi/v/breast-cancer-toolkit.svg)](https://pypi.org/project/breast-cancer-toolkit/)
<!-- These are examples of badges you might also want to add to your README. Update the URLs accordingly.
[![Built Status](https://api.cirrus-ci.com/github/<USER>/breast-cancer-toolkit.svg?branch=main)](https://cirrus-ci.com/github/<USER>/breast-cancer-toolkit)
[![ReadTheDocs](https://readthedocs.org/projects/breast-cancer-toolkit/badge/?version=latest)](https://breast-cancer-toolkit.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/breast-cancer-toolkit/main.svg)](https://coveralls.io/r/<USER>/breast-cancer-toolkit)
[![PyPI-Server](https://img.shields.io/pypi/v/breast-cancer-toolkit.svg)](https://pypi.org/project/breast-cancer-toolkit/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/breast-cancer-toolkit.svg)](https://anaconda.org/conda-forge/breast-cancer-toolkit)
[![Monthly Downloads](https://pepy.tech/badge/breast-cancer-toolkit/month)](https://pepy.tech/project/breast-cancer-toolkit)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/breast-cancer-toolkit)
-->

# BCT

> Machine learning toolkit designed to support data scientists in breast cancer detection, classification and analysis.

## Installation

Install the package with:

```bash
pip install breast-cancer-toolkit
```

## Usage as CLI

### Convert the DCM files into TIFF format recursively with the same basename.
```bash
parallel bct convert {} {.}.tiff ::: **/*.dcm
```


## Usage as library

## Models

### Remove background with instance segmentation

| Model | Training data | Resolution | # of samples seen | IoU | Accuracy |
|-------|---------------|------------|-------------------|-----|----------|
|       |               |            |                   |     |          |

## Data sources

| Source          | Argument                                 | Type         | Notes                                                                                     |
|-----------------|------------------------------------------|--------------|-------------------------------------------------------------------------------------------|
| image           | 'image.jpg'                              | str or Path  | Single image file. Format supported: jgp, png, dcm, tiff                                  |
| URL             | 'https://ultralytics.com/images/bus.jpg' | str          | URL to an image.                                                                          |
| screenshot      | 'screen'                                 | str          | Capture a screenshot.                                                                     |
| PIL             | Image.open('im.jpg')                     | PIL.Image    | HWC format with RGB channels.                                                             |
| OpenCV          | cv2.imread('im.jpg')                     | np.ndarray   | HWC format with BGR channels `uint8 (0-255)`.                                             |
| numpy           | np.zeros((640,1280,3))                   | np.ndarray   | HWC format with BGR channels `uint8 (0-255)`.                                             |
| torch           | torch.zeros(16,3,320,640)                | torch.Tensor | BCHW format with RGB channels `float32 (0.0-1.0)`.                                        |
| CSV, json, xlsx | 'sources.csv'                            | str or Path  | CSV file containing paths to images, videos, or directories.                              |
| video           | 'video.mp4'                              | str or Path  | Video file in formats like MP4, AVI, etc.                                                 |
| directory       | 'path/'                                  | str or Path  | Path to a directory containing images or videos.                                          |
| glob            | 'path/*.jpg'                             | str          | Glob pattern to match multiple files. Use the `*` character as a wildcard.                |
| YouTube         | 'https://youtu.be/LNwODJXcvt4'           | str          | URL to a YouTube video.                                                                   |
| stream          | 'rtsp://example.com/media.mp4'           | str          | URL for streaming protocols such as RTSP, RTMP, TCP, or an IP address.                    |
| multi-stream    | 'list.streams'                           | str or Path  | *.streams text file with one stream URL per row, i.e. 8 streams will run at batch-size 8. |

## Note

This project has been set up using [PyScaffold] 4.5 and the [dsproject extension] 0.0.post1.dev166+g2aaddf7.d20240514.

[conda]: https://docs.conda.io/

[pre-commit]: https://pre-commit.com/

[Jupyter]: https://jupyter.org/

[nbstripout]: https://github.com/kynan/nbstripout

[Google style]: http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings

[PyScaffold]: https://pyscaffold.org/

[dsproject extension]: https://github.com/pyscaffold/pyscaffoldext-dsproject
