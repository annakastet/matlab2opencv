# Transform MatLab .csv to OpenCV trainer input
This repository contains a simple Python script that can be used to transform the image dataset you've labeled in MatLab into the input format required by OpenCV trainers.

1. Use the Matlab Training Image Labeler to label your images
2. When you're done, click *Export ROIs*.
3. In the MatLab command window, enter: `writetable(YourLabels, 'yourfilename.csv')`

## Assumed file structure
```
MatlabToOpenCV
  |
  |
  transform_matlab_data.py
  frames/   <-- folder with your images
  matlabLabels/   <-- folder with .csv files from MatLab

```

## Output
The Python script will create a new folder `dataset/` (if it does not already exist) containing a folder with the images and text files on the following format:

```
images/img1.jpg  1  140 100 45 45
images/img2.jpg  2  100 200 50 50   50 30 25 25
...
```
