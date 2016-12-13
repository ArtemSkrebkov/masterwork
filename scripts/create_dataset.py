import cv2
import numpy as np
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--base_dir', type=str, default="/home/artem/workspace/datasets/kitti_raw")
parser.add_argument('--dataset_dir', type=str, default="/home/artem/workspace/datasets/kitti_stixel_net")
parser.add_argument('--gt_filename', type=str, default="/home/artem/workspace/diploma/stixelnet/BMVC15_StixelDataset/StixelsGroundTruth.txt")
parser.add_argument('--stripe_width', type=int, default=24)
parser.add_argument('--stripe_height', type=int, default=370)
args = parser.parse_args()

base_dir = args.base_dir
dataset_dir = args.dataset_dir 
gt_filename = args.gt_filename 
stripe_width = args.stripe_width
stripe_height = args.stripe_height
train_filename = "%s/train.txt" % dataset_dir
test_filename = "%s/test.txt" % dataset_dir
N = 50
h_min = 140
step = (stripe_height - h_min) / N
bins = np.arange(h_min, stripe_height, step)

ground_truth = open(gt_filename)
train = open(train_filename, 'w')
test = open(test_filename, 'w')
img_filename = "empty"
for line in ground_truth:
    data = line.split('\t')
    date = data[0]
    series_id = int(data[1])
    frame_id = int(data[2])
    x = int(data[3])
    y = int(data[4])
    data_type = data[5].strip('\n')    
    cur_img_filename = "%s/2011_%s/2011_%s_drive_%04d_sync/image_02/data/%010d.png" % (base_dir, date, date, series_id, frame_id)
    if img_filename != cur_img_filename:
        img = cv2.imread(cur_img_filename)
        if img is None:
            print("Image %s aren't exist" % (cur_img_filename))
            break
        img_filename = cur_img_filename
        print("Processing: %s %d %d" % (date, series_id, frame_id))
    range_x = range(x - stripe_width / 2, x + stripe_width / 2)
    range_y = range(0, stripe_height)
    stripe = img[0:stripe_height,(x - stripe_width / 2):(x+stripe_width/2)]
    stripe_filename = "%s/%s/2011_%s_drive_%04d_sync_frame_%010d_%04d_%04d.png" % (dataset_dir, data_type, date, series_id, frame_id, x, y)
    cv2.imwrite(stripe_filename, stripe)
    c = 0 
    for i in range(0, len(bins) - 1):
        if bins[i] <= y and y < bins[i+1]:
            c = i
            break
    if data_type == 'Train':
        train.write("%s %d\n" % (stripe_filename, c))
    elif data_type == 'Test':
        test.write("%s %d\n" % (stripe_filename, c))
ground_truth.close()
train.close()
test.close()
