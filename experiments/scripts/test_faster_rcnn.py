from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths

from model.config import cfg, cfg_from_list, cfg_from_file
from frcnn_test import frcnn_test

from sacred import Experiment

import os
import os.path as osp

ex = Experiment()

frcnn_test = ex.capture(frcnn_test)

@ex.config
def default():
	score_thresh = 0.05
	clip_bbox = False
	max_per_image = 100

	# Added so that sacred doesn't throw a key error
	description = ""
	timestamp = ""
	imdbval_name = ""
	weights = ""
	network = ""

# Dataset configs
@ex.named_config
def small_mot():
	imdbtest_name = "mot_2017_small_val"

@ex.named_config
def mot():
	imdbtest_name = "mot_2017_all"

@ex.named_config
def mot_test():
	imdbtest_name = "mot_2017_test"

@ex.named_config
def mot_train():
	imdbtest_name = "mot_2017_train"


@ex.automain
def my_main(imdb_name, imdbtest_name, cfg_file, set_cfgs, tag, max_iters, clip_bbox, _config):

	# Clip bboxes after bbox reg to image boundary
	cfg_from_list(['TEST.BBOX_CLIP', str(clip_bbox)])

	# Already set everything here, so the path can be determined correctly
	if cfg_file:
		cfg_from_file(cfg_file)
	if set_cfgs:
		cfg_from_list(set_cfgs)

	model_dir = osp.abspath(osp.join(cfg.ROOT_DIR, 'output', 'frcnn', cfg.EXP_DIR,
		imdb_name, tag))
	model = osp.join(model_dir, cfg.TRAIN.SNAPSHOT_PREFIX + '_iter_{:d}'.format(max_iters) + '.pth')
	output_dir = osp.join(model_dir, imdbtest_name)
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	print('Called with args:')
	print(_config)

	frcnn_test(model=model, output_dir=output_dir)