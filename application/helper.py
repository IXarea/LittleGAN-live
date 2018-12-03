import numpy as np
import tensorflow as tf
from .littlegan.execute import generator, discriminator, args
from .littlegan.utils import save_image
from os import path
from application import app


def get_hash(data):
    filename1 = str(data['seed']).zfill(6)
    for i in data['attr']:
        filename1 += str(i).zfill(3)
    filename1 = format(int(filename1), 'x')
    filename2 = ""
    if data['rate'] > 0:
        filename2 = str(data['rate']).zfill(3)
        filename2 += str(data['seed2']).zfill(6)
        filename2 = "_" + format(int(filename2), 'x')
    return filename1 + filename2


def norm_input(data):
    new_data = {}
    if "seed" not in data or not isinstance(data['seed'], int):
        new_data['seed'] = np.random.randint(0, 999999, None, int)
    else:
        new_data['seed'] = int(np.clip(data['seed'], 0, 999999))
    # todo: 更多检查
    if "attr" not in data or not len(data["attr"]) == args.attr_dim:
        new_data['attr'] = np.random.randint(0, 100, [args.attr_dim], int).tolist()
    else:
        new_data['attr'] = np.clip(data['attr'], 0, 100).astype(int).tolist()

    if "rate" not in data or not isinstance(data['rate'], int):
        new_data['rate'] = 0
    else:
        new_data['rate'] = int(np.clip(data['rate'], 0, 100))

    if new_data['rate'] > 0:
        if "seed2" not in data or not isinstance(data['seed2'], int):
            new_data['seed2'] = np.random.randint(0, 999999, None, int)
        else:
            new_data['seed2'] = int(np.clip(data['seed2'], 0, 999999))
    else:
        new_data['seed2'] = None
    print(data)
    print(new_data)
    return new_data


def model_generate(data):
    file_name = "generate/%s.jpg" % get_hash(data)
    local_path = path.join(app.static_folder, file_name)
    if not path.isfile(local_path):

        attr = np.array(data['attr']).reshape([1, args.attr_dim]).astype(np.float32) / 100

        noise = tf.random.normal([1, args.noise_dim], mean=0., stddev=1., seed=data['seed'])
        if data['rate'] > 0:
            rate = np.array(data['rate']).astype(np.float32) / 100
            noise2 = tf.random.normal([1, args.noise_dim], mean=0., stddev=rate, seed=data['seed2'])
            noise = noise - noise2
        image_vec = generator([noise, attr])
        save_image(image_vec, local_path)
    return file_name
