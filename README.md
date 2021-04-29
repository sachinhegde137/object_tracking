# Object tracking
The task given is implemented using Pycharm IDE. With the help of OpenCV
python package, a script is written to visualize the contents of the csv file and track
the objects. The key idea is to track the object in the video once it has been detected.
Thus a dictionary is created which matches the frame numbers to the number of
objects present in that frame and also the bounding box coordinates. If the object
is found out to be a new one, then the bounding box is drawn manually. Otherwise,
the trackers will provide the bounding box details for the next frame.

The experiment can be carried out to test 7 in-built object trackers in OpenCV
package: csrt, kcf, boosting, mil, tld, medianflow, mosse. By default, the implementation uses kcf tracker. However, this can be changed by passing the required
tracker name as the argument in the argument parser.

## Dependencies
+ Python 3.6.6
+ opencv-contrib-python 4.5.1

## Usage
Place the csv file and the video in the project folder. Run the python script tracker.py like this. The script runs fine even without arguments as input. 
The program takes the video and the csv file present in the folder as default and tracks with kcf tracker by default.
```
python tracker.py --video <path-to-video> --csv <path-to-csv-file> --tracker <name of tracker>
```
