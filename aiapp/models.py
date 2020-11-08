import io, base64

from django.db import models
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from PIL import Image


graph = tf.compat.v1.get_default_graph()

class Photo(models.Model):
    image = models.ImageField(upload_to='photos')

    IMAGE_SIZE = 224
    MODEL_FILE_PATH = './aiapp/mlmodels/vgg16_transfer.h5'
    classes = ["我妻善逸", "胡蝶しのぶ", "炭治郎", "禰豆子", "冨岡義勇"]
    num_classes = len(classes)

    def predict(self):
        model = None
        global graph
        with graph.as_default():
            model = load_model(self.MODEL_FILE_PATH)

            img_data = self.image.read()
            img_bin = io.BytesIO(img_data)

            image = Image.open(img_bin)
            image = image.convert('RGB')
            image = image.resize((self.IMAGE_SIZE, self.IMAGE_SIZE))
            data = np.asarray(image) / 255.0
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0]

            pdata_list = []
            for i in range(len(result)):
                per = int(result[i] * 100)
                pdata = [self.classes[i], per]
                pdata_list.append(pdata)

            max_predicted = result.argmax()
            percentage = int(result[max_predicted] * 100)
            max_pdata = [self.classes[max_predicted], percentage]

            return pdata_list, max_pdata

    def image_src(self):
        with self.image.open() as img:
            base64_img = base64.b64encode(img.read()).decode()

            return 'data:' + img.file.content_type + ';base64,' + base64_img
