import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import tensorflow as tf
import numpy as np
import nltk 
from nltk.stem import WordNetLemmatizer
import random
import json
import pickle

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('omw-1.4')

lemmatizer = nltk.WordNetLemmatizer()

intents = json.loads(open('data.json').read())

class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if(logs.get('accuracy') == 1.0 and logs.get('loss') <= 0.015):
            print("\n Achieved 100% accuracy and 0.015 loss")
            self.model.stop_training = True

callbacks = myCallback()

words = []
classes = []
documents = []
ignore_letters = ['!', '?', ',', '.', "'", '-', '_', '/', '\\', '\'', ]

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# print(words)
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
# print(words)

words = sorted(set(words))
classes = sorted(set(classes))
# print(words)
# print(classes)          

pickle.dump(words, open('words.pk1', 'wb'))
pickle.dump(classes, open('classes.pk1', 'wb'))

training = []
output_empty = [0] * len(classes)

for documents in documents:
    bag = []
    word_patterns = documents[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    # print(bag)

    output_row = list(output_empty)
    output_row[classes.index(documents[1])] = 1
    training.append([bag, output_row])

# print(training)
random.shuffle(training)
training = np.array(training, dtype=object)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = tf.keras.Sequential()

model.add(tf.keras.layers.Dense(512, input_shape=(len(train_x[0]),), activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(256, activation='relu'))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(128, activation='relu'))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(len(train_y[0]), activation='softmax'))

# adamax, adagrad, nadam 
sgd = tf.keras.optimizers.legacy.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(np.array(train_x), np.array(train_y), epochs=500, batch_size=64, verbose=1, callbacks=[callbacks])
model.save('charbot_model.model', history)



