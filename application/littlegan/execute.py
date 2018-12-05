from os import path
import tensorflow as tf
from .model import Adjuster, Discriminator, Decoder, Encoder, Generator
from .. import app
from flask import json


class Arg:

    def __init__(self, config_file):

        if path.isfile(config_file):
            with open(config_file) as f:
                args_dict = json.load(f)
        else:
            raise AttributeError("No Model Config File")
        for item in args_dict:
            self.__setattr__(item, args_dict[item])
        self.attr_dim = len(self.attr)


args = Arg(path.join(app.root_path, "..", "data", "model.config.json"))
decoder = Decoder(args)
encoder = Encoder(args)
generator = Generator(args, decoder)
discriminator = Discriminator(args, encoder)
adjuster = Adjuster(args, discriminator, generator)

test_image = tf.random.uniform([1, args.image_dim, args.image_dim, args.image_channel], 0, 1)
test_cond = tf.random.uniform([1, args.attr_dim], 0, 1)
test_noise = tf.random_normal([1, args.noise_dim])
discriminator(test_image)
generator([test_noise, test_cond])
adjuster([test_image, test_cond])

checkpoint = tf.train.Checkpoint(discriminator=discriminator, generator=generator, adjuster=adjuster)
if path.isfile(path.join(app.root_path, "..", "data", "checkpoint")):
    checkpoint.restore(tf.train.latest_checkpoint(path.join(app.root_path, "..", "data")))
else:
    raise AttributeError("No Checkpoint Data")
