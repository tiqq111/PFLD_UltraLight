# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

import os
import argparse
from torch.autograd import Variable
import torch

from models.PFLD import PFLD
from models.PFLD_Ghost import PFLD_Ghost
from models.PFLD_Ghost_Slim import PFLD_Ghost_Slim

parser = argparse.ArgumentParser(description='pytorch2onnx')
parser.add_argument('--model_type', default='PFLD_Ultralight', type=str)
parser.add_argument('--input_size', default=112, type=int)
parser.add_argument('--width_factor', default=1, type=float)
parser.add_argument('--landmark_number', default=98, type=int)
parser.add_argument('--model_path', default="./checkpoint/models/PFLD_Ultralight_1_112_2020-08-29-08-49/pfld_ultralight_best.pth")
args = parser.parse_args()

print("=====> load pytorch checkpoint...")
checkpoint = torch.load(args.model_path, map_location=torch.device('cpu'))
MODEL_DICT = {'PFLD': PFLD,
              'PFLD_Ghost': PFLD_Ghost,
              'PFLD_Ghost_Slim': PFLD_Ghost_Slim,
              }
MODEL_TYPE = args.model_type
WIDTH_FACTOR = args.width_factor
INPUT_SIZE = args.input_size
LANDMARK_NUMBER = args.landmark_number
model = MODEL_DICT[MODEL_TYPE](WIDTH_FACTOR, INPUT_SIZE, LANDMARK_NUMBER)
model.load_state_dict(checkpoint)

print("=====> convert pytorch model to onnx...")
dummy_input = Variable(torch.randn(1, 3, INPUT_SIZE, INPUT_SIZE))
input_names = ["input"]
output_names = ["output"]
torch.onnx.export(model, dummy_input, "{}_{}_{}.onnx".format(MODEL_TYPE, INPUT_SIZE, WIDTH_FACTOR), verbose=False, input_names=input_names, output_names=output_names)
