import tensorflow as tf
import numpy as np
import json

f = open('test.json')
data = json.load(f)

x_train = []
y_train = []
for i in range(len(data['images'])):
    img = np.asarray(data['images'][i], dtype=np.float64)
    x_train.append(img)
    lbl = np.asarray(data['representations'][i])
    y_train.append(lbl)


print(y_train[0].shape)
train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train))
print(train_ds)

buffer_size = 25
batch_size = 1

train_ds = (train_ds
                  .shuffle(buffer_size=buffer_size)
                  .batch(batch_size=batch_size, drop_remainder=True))
                  

def residual_block(img_input, filters, rescale=False, b_name='1'):
    
    ch_axis = -1 # defualt (channel_last)
    stride = 1
    w_init = 'he_uniform'
    n = '_'+b_name

    skip_connection = img_input

    if rescale == True:
      stride = 2
      skip_connection = tf.keras.layers.Conv2D(filters, (1,1), 
                                               strides=(stride,stride),
                                               kernel_initializer=w_init,
                                               name='skip_conv'+n)(skip_connection)
      skip_connection = tf.keras.layers.BatchNormalization(axis=ch_axis,
                                                           name='skip_bn'+n)(skip_connection)

    y = tf.keras.layers.Conv2D(filters, (3,3), padding ='same', 
                               strides=(stride,stride),
                               kernel_initializer=w_init,
                               name='conv_1'+n)(img_input)
    y = tf.keras.layers.BatchNormalization(axis=ch_axis, name='bn_1'+n)(y)
    y = tf.keras.layers.Activation('relu', name='act_1'+n)(y)
    y = tf.keras.layers.Conv2D(filters, (3,3), padding = 'same', 
                               kernel_initializer=w_init, name='conv_2'+n)(y)
    y = tf.keras.layers.BatchNormalization(axis=ch_axis, name='bn_2'+n)(y)

    y = tf.keras.layers.Add()([y, skip_connection])     
    output = tf.keras.layers.Activation('relu', name='act_block'+n)(y)

    model = tf.keras.Model(img_input, output, name='residual_block'+n)

    return model

def get_Model(input_shape, no_of_classes):

    x = tf.keras.Input(shape=input_shape, name='x')
    
    y = tf.keras.layers.Conv2D(filters=5, kernel_size=3, padding='same')(x)
    y = tf.keras.layers.BatchNormalization()(y)
    y = tf.keras.layers.Activation('relu')(y)

    x_in_1 = tf.keras.Input(shape=y.shape[1:])
    base_model_1 = residual_block(x_in_1, 5, rescale=False, b_name='1')
    y = base_model_1(y, training=True)
    
    x_in_2 = tf.keras.Input(shape=y.shape[1:])
    base_model_2 = residual_block(x_in_2, 10, rescale=True, b_name='2')
    y = base_model_2(y, training=True)
    
    y = tf.keras.layers.GlobalAveragePooling2D()(y)
    y =  tf.keras.layers.Dense(10)(y)
    outputs = tf.keras.layers.Dense(no_of_classes, activation='softmax' )(y)
    
    model = tf.keras.Model(x, outputs, name='simple_res_net')

    return model
    
model_to_train = get_Model((32,32,3), 512)

model_to_train.summary()

model_to_train.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4, beta_1=0.9, beta_2=0.999, amsgrad=False),
    loss='sparse_categorical_crossentropy', 
    metrics=['accuracy']
  )
model_to_train.fit(train_ds, epochs=30, batch_size=None)
