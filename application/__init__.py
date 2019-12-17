from flask import Flask
from config import Config
import tensorflow as tf

tf.compat.v1.enable_eager_execution()
app = Flask(__name__)
app.config.from_object(Config)
from application import route
