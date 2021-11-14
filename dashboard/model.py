import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Flatten, Conv1D, MaxPooling1D, LSTM

try:
    gpu_devices = tf.config.experimental.list_physical_devices('GPU')
    for device in gpu_devices: tf.config.experimental.set_memory_growth(device, True)
except:
    pass


class Actor_Model:
    def __init__(self, input_shape=(100,4), action_space=3):
        X_input = Input(input_shape)
        self.action_space = action_space
        X = Conv1D(filters=32, kernel_size=3, padding="same", activation="tanh")(X_input)
        X = MaxPooling1D(pool_size=2)(X)
        X = LSTM(32)(X)
        X = Flatten()(X)
        A = Dense(32, activation="relu")(X)
        output = Dense(self.action_space, activation="softmax")(A)

        self.Actor = Model(inputs=X_input, outputs=output)
