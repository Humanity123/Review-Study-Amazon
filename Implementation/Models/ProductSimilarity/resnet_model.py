import os, random, pdb
import matplotlib.pyplot as plt

from cntk import constant, use_default_device, cross_entropy_with_softmax, classification_error
from cntk import load_model, Trainer, UnitType
from cntk.io import MinibatchSource, ImageDeserializer, StreamDefs, StreamDef
import cntk.io.transforms as xforms
from cntk.layers import placeholder, GlobalAveragePooling, Dropout, Dense
from cntk.learners import momentum_sgd, learning_rate_schedule, momentum_schedule
from cntk.logging import log_number_of_parameters, ProgressPrinter, graph
from cntk.logging.graph import find_by_name
from cntk.ops import input_variable, combine
from cntk.ops.functions import CloneMethod

random.seed(0)

# Creates the network model for transfer learning
def create_model(base_model_file, input_features, num_classes,  dropout_rate = 0.5, freeze_weights = False):
    # Load the pretrained classification net and find nodes
    base_model   = load_model(base_model_file)
    feature_node = find_by_name(base_model, 'features')
    beforePooling_node = find_by_name(base_model, "z.x.x.r")
    #graph.plot(base_model, filename="base_model.pdf") # Write graph visualization

    # Clone model until right before the pooling layer, ie. until including z.x.x.r
    modelCloned = combine([beforePooling_node.owner]).clone(
        CloneMethod.freeze if freeze_weights else CloneMethod.clone,
        {feature_node: placeholder(name='features')})

    # Center the input around zero and set model input.
    # Do this early, to avoid CNTK bug with wrongly estimated layer shapes
    feat_norm = input_features - constant(114)
    model = modelCloned(feat_norm)

    # Pool over all spatial dimensions and add dropout layer
    avgPool = GlobalAveragePooling(name = "poolingLayer")(model)
    if dropout_rate > 0:
        avgPoolDrop = Dropout(dropout_rate)(avgPool)
    else:
        avgPoolDrop = avgPool

    # Add new dense layer for class prediction
    finalModel = Dense(num_classes, activation=None, name="prediction") (avgPoolDrop)
    return finalModel
