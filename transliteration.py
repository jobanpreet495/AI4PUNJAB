from keras.models import load_model
import tensorflow as tf
import numpy as np
import pickle 

#-----------------------------------------------------Punjabi- English/ English-Punjabi--------------------------------------------------------------------------

PE_model = load_model('Punjabi_to_English/pun_to_eng.hdf5') 
EP_model=load_model('English_to_punjabi/eng_to_pun.hdf5')

with open('Punjabi_to_English/punjabi_vocab_to_int.pickle', 'rb') as handle:
    punjabi_vocab_to_int = pickle.load(handle)

with open('Punjabi_to_English/english_int_to_vocab.pickle', 'rb') as handle:
    english_int_to_vocab = pickle.load(handle)

with open('English_to_punjabi/engvocab_to_int.pickle', 'rb') as handle:
    english_vocab_to_int = pickle.load(handle)

with open('English_to_punjabi/punint_to_vocab.pickle', 'rb') as handle:
    punjabi_int_to_vocab = pickle.load(handle)





#-----------------------------------------Punjabi to English----------------------------------------------------------------------


def pun_to_eng(text):
    word_pred = []
    text=text.split()
    text = ['@' + item + '#' for item in text]
    for i in text:
    # Convert the new input sentence to a tensor using the Word2Index objects
        new_input_tensor = [[punjabi_vocab_to_int.get(char, punjabi_vocab_to_int['<pad>']) for char in i]]
        # Pad the tensor to the maximum length
        new_input_tensor = tf.keras.preprocessing.sequence.pad_sequences(new_input_tensor, maxlen=24, padding='post')
        english_tensor_predicted = np.argmax(PE_model.predict(new_input_tensor),axis=-1)
    
        for i in english_tensor_predicted[0]:
           word_pred.append(english_int_to_vocab[i])
    return word_pred


#---------------------------------------------------English to Punjabi------------------------------------------------------------------------


def eng_to_pun(text):
    word_pred = []
    text=text.split()
    text = ['@' + item + '#' for item in text]
    for i in text:
    # Convert the new input sentence to a tensor using the Word2Index objects
        new_input_tensor = [[english_vocab_to_int.get(char, english_vocab_to_int['<pad>']) for char in i]]
        # Pad the tensor to the maximum length
        new_input_tensor = tf.keras.preprocessing.sequence.pad_sequences(new_input_tensor, maxlen=29, padding='post')
        punjabi_tensor_predicted = np.argmax(EP_model.predict(new_input_tensor),axis=-1)
    
        for i in punjabi_tensor_predicted[0]:
           word_pred.append(punjabi_int_to_vocab[i])
    return word_pred



def eng_to_pun2(text):
    word_pred = []
    text=text.split()
    text = ['@' + item + '#' for item in text]
    for i in text:
    # Convert the new input sentence to a tensor using the Word2Index objects
            new_input_tensor = [[english_vocab_to_int.get(char, english_vocab_to_int['<pad>']) for char in i]]
            # Pad the tensor to the maximum length
            new_input_tensor = tf.keras.preprocessing.sequence.pad_sequences(new_input_tensor, maxlen=29, padding='post')
            punjabi_tensor_predicted = np.argmax(EP_model.predict(new_input_tensor),axis=-1)
          
            for i in punjabi_tensor_predicted[0]:
               word_pred.append(punjabi_int_to_vocab[i])
    return word_pred

