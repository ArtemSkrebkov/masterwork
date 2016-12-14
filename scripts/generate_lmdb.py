import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--dataset_dir', type=str, default="/")
parser.add_argument('--caffe_tools', type=str, default="/home/artem/workspace/build/caffe/tools")
parser.add_argument('--lmdb_dir', type=str, default="/home/artem/workspace/datasets/kitti_stixel_net/lmdb")
parser.add_argument('--labels_filename', type=str, default="/home/artem/workspace/datasets/kitti_stixel_net/train.txt")
#parser.add_argument('--width', type=int, default=24)
#parser.add_argument('--height', type=int, default=370)
args = parser.parse_args()

command = "GLOG_logtostderr=1 %s/convert_imageset --shuffle " % (args.caffe_tools)
command += "%s %s %s" % (args.dataset_dir, args.labels_filename, args.lmdb_dir)
os.system(command)
