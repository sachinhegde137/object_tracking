
import argparse
import cv2
import csv


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Input video and the csv file path')
    parser.add_argument("--video", default='data/Video_BM.mp4',
                        type=str, help="path to video")
    parser.add_argument("--csv", default='data/Video_BM__01.csv',
                        type=str, help="path to csv file")
    parser.add_argument("--tracker", default='kcf',
                        type=str, help="enter one of the following trackers: csrt, kcf, boosting, "
                                       "mil, tld, medianflow, mosse")
    args = parser.parse_args()

    input_path = args.video
    csv_path = args.csv
    tracker_name = args.tracker

# input_path = "Entrance Test/Video_BM.mp4"
# csv_path = "Entrance Test/Video_BM__01.csv"
# delimiter = '\t'
# tracker_name = "kcf"

with open(csv_path) as csv_file:
    csv_f = csv.reader(csv_file)

    # Create two lists containing frame number and the bounding box coordinates. These lists
    # will be used to create a dictionary with frame numbers as keys and bounding box coordinates
    # with their label as values.
    frame_number = []
    bboxes = []

    for row in csv_f:
        if not csv_f.line_num == 1 and not csv_f.line_num == 2:
            # get number of bounding boxes in the frame
            row_filtered = [columns for columns in row if columns != '']
            columns = len(row_filtered)
            frame_number.append(int(row_filtered[0]))
            time_ms = int(row_filtered[1])
            total_bboxes = int((columns-2)/6)

            # create a temporary list containing bounding boxes of the current frame
            bbox = []
            for n in range(total_bboxes):
                bbox.append([int(row[n*6+2]), int(row[n*6+3]), int(row[n*6+4]), int(row[n*6+5]), int(row[n*6+7])])

            # append this temporary list to the main list
            bboxes.append(bbox)

    # once all the rows are read, create the dictionary
    bbox_dict = dict(zip(frame_number, bboxes))
    bboxes.clear()

# A dictionary that maps the object tracking name to its corresponding implementation
OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.legacy.TrackerCSRT_create,
    "kcf": cv2.legacy.TrackerKCF_create,
    "boosting": cv2.legacy.TrackerBoosting_create,
    "mil": cv2.legacy.TrackerMIL_create,
    "tld": cv2.legacy.TrackerTLD_create,
    "medianflow": cv2.legacy.TrackerMedianFlow_create,
    "mosse": cv2.legacy.TrackerMOSSE_create
}

# initialize OpenCV's special multi-object tracker
trackers = cv2.legacy.MultiTracker_create()

cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    raise ValueError("Error opening video stream or file")

frame_count = 0
object_count = 0

# create an empty dictionary to map object labels to different colours
object_dict = {}
colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]
labels = []

while True:
    ret, frame = cap.read()
    # break out of the loop if the video is complete
    if frame is None:
        break;

    # access the bounding box and label of the current frame using the dictionary created earlier
    frame_count = frame_count + 1
    bboxes = (bbox_dict[frame_count])
    total_bboxes = len(bboxes)

    # define label width and height to display
    label_w = 50
    label_h = 50

    # update trackers
    (success, boxes) = trackers.update(frame)

    # loop over number of objects detected in that frame
    for n in range(total_bboxes):
        label_id = str(bboxes[n][4])
        x, y = bboxes[n][0], bboxes[n][1]
        w, h = bboxes[n][2], bboxes[n][3]

        # if the label is not in the dictionary, add it
        if not label_id in object_dict:
            labels.append(label_id)
            object_count = object_count + 1
            tracker = OPENCV_OBJECT_TRACKERS[tracker_name]()
            trackers.add(tracker, frame, (x, y, w, h))
            object_dict[label_id] = colors[object_count]

            # draw bounding box and label
            cv2.rectangle(frame, (x, y), (x + w, y + h), colors[object_count - 1], 2)
            cv2.rectangle(frame, (x, y), (x + label_w, y + label_h), colors[object_count - 1], cv2.FILLED)
            cv2.putText(frame, label_id, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

    if len(boxes) != 0:
        for i, box in enumerate(boxes):
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), colors[i], 2)
            cv2.rectangle(frame, (x, y), (x + label_w, y + label_h), colors[i], cv2.FILLED)
            cv2.putText(frame, labels[i], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

    cv2.imshow("Frame", cv2.resize(frame, (800, 600)))
    k = cv2.waitKey(10)
    if k == 27:
        cv2.destroyAllWindows()
        break

print("The video is complete")


