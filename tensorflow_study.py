import tensorflow as tf
import numpy as np
from Game import *
from pathlib import Path
from pickle import load

# load data
data:list[tuple[Game, tuple[Interaction, tuple[int, int]]]] = []

__here__ = Path(__file__).parent

data_dir = __here__ / "data"

for child in data_dir.iterdir():
  print(child)

print((data_dir / ("data" + str(len(list(data_dir.iterdir())) + 1) + ".pkl")))

def load_data(target: str) -> list[tuple[Game, tuple[Interaction, tuple[int, int]]]]:
  with (data_dir / (target+".pkl")).open("rb") as f:
    return load(f)

for target in data_dir.iterdir():
  if target.is_file() and target.suffix == ".pkl":
    print(target.stem)
    data.extend(load_data(target.stem))

# 데이터 전처리 (np로 변환)

data_input = np.array([i[0].field] for i in data)

input_shape = (16, 16)
output_shape = (16, 16)

model = tf.keras.models.Sequential([
  tf.keras.Input(shape=input_shape),
  tf.keras.layers.Dense(1024, activation='leakyRelu'),
  tf.keras.layers.Dense(512, activation='leakyRelu'),
  tf.keras.layers.Dense(tf.reduce_mean(output_shape), activation='leakyRelu'),
  tf.keras.layers.Dense(tf.reduce_mean(output_shape), activation='sigmoid'),
  tf.keras.layers.Reshape(output_shape)
])

model.compile(optimizer="adam", loss="binary_crossentropy", mertics=['accuracy'])

model.fit(numberic_data_input, numberic_data_output_position, epochs=20, batch_size=1)


# model.fit (x data, y data)