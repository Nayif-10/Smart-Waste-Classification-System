import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Data augmentation
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)
val_datagen = ImageDataGenerator(rescale=1.0 / 255.0)

train_generator = train_datagen.flow_from_directory(    
    "dataset_split/train", target_size=(224, 224), batch_size=32, class_mode="binary"
)
val_generator = val_datagen.flow_from_directory(
    "dataset_split/val", target_size=(224, 224), batch_size=32, class_mode="binary"
)


base_model = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3)) 
for layer in base_model.layers:
    layer.trainable = False 

global_pool = GlobalAveragePooling2D()(base_model.output)   
dropout_layer = Dropout(0.5)(global_pool)   
output_layer = Dense(1, activation="sigmoid")(dropout_layer)    
model = Model(inputs=base_model.input, outputs=output_layer)     


model.compile(optimizer=Adam(learning_rate=0.0001), loss="binary_crossentropy", metrics=["accuracy"])   


callbacks = [
    EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),   
    ModelCheckpoint("best_model.h5", save_best_only=True, monitor="val_loss")
]


model.fit( 
    train_generator,
    validation_data=val_generator,
    epochs=20,
    callbacks=callbacks
)

for layer in base_model.layers[-10:]:   
    layer.trainable = True

model.compile(optimizer=Adam(learning_rate=0.00001), loss="binary_crossentropy", metrics=["accuracy"])  
model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10,
    callbacks=callbacks
)

model.save("final_model.h5")
