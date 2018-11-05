from Utilitaires import *
import tensorflow as tf
from tensorflow import keras
# Just disables the warning, doesn't enable AVX/FMA
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#mode = select_mode()
#if mode == 1:
#    ecg = load_base1_data()
#    ecg.plot()
#elif mode == 2:
#    ecg_animal = load_animal_data()
#    ecg_animal.plot()
#elif mode == 3:
#    ecg_m = load_m_data()
#    ecg_m.plot()


n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 1
batch_size = 100

listeECG = load_animal_datas()
x_test,y_test = create_test(listeECG)
x_train,y_train = create_train(listeECG)


n_input = len(x_train[0]['SMA'])+len(x_train[0]['EMA'])+1 # input layer (28x28 pixels)
n_hidden1 = 512 # 1st hidden layer
n_hidden2 = 256 # 2nd hidden layer
n_hidden3 = 128 # 3rd hidden layer
n_output = 1   # output layer (0-9 digits)

batch_size = get_size_batch(listeECG)
print(len(x_train[:]))
#n_input = get_shape(listeECG)

weights = {
    'w1': tf.Variable(tf.truncated_normal([121, n_hidden1], stddev=0.1)),
    'w2': tf.Variable(tf.truncated_normal([n_hidden1, n_hidden2], stddev=0.1)),
    'w3': tf.Variable(tf.truncated_normal([n_hidden2, n_hidden3], stddev=0.1)),
    'out': tf.Variable(tf.truncated_normal([n_hidden3, n_output], stddev=0.1)),
}
biases = {
    'b1': tf.Variable(tf.constant(0.1, shape=[n_hidden1])),
    'b2': tf.Variable(tf.constant(0.1, shape=[n_hidden2])),
    'b3': tf.Variable(tf.constant(0.1, shape=[n_hidden3])),
    'out': tf.Variable(tf.constant(0.1, shape=[n_output]))
}
keep_prob = tf.placeholder("float")





def multilayer_perceptron(x, weights, biases, keep_prob):
    layer_1 = tf.add(tf.matmul(x, weights['w1']), biases['b1'])
    layer_2 = tf.add(tf.matmul(layer_1, weights['w2']), biases['b2'])
    layer_3 = tf.add(tf.matmul(layer_2, weights['w3']), biases['b3'])
    layer_drop = tf.nn.dropout(layer_3, keep_prob)
    output = tf.matmul(layer_3, weights['out']) + biases['out']
    return output



def train_neural_network(x):
    prediction = multilayer_perceptron(x, weights, biases, keep_prob)
    # OLD VERSION:
    # cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(prediction,y) )
    # NEW:
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    hm_epochs = 10
    with tf.Session() as sess:
        # OLD:
        # sess.run(tf.initialize_all_variables())
        # NEW:
        sess.run(tf.global_variables_initializer())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            for _ in range(batch_size):
                epoch_x, epoch_y = get_epoch(x_train,y_train)

                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                epoch_loss += c

            print('Epoch', epoch, 'completed out of', hm_epochs, 'loss:', epoch_loss)

        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        test_x, test_y = get_epoch(x_test,y_test)
        print('Accuracy:', accuracy.eval({x: test_x, y: test_y}))






x = tf.placeholder(tf.float32, shape=[None,121], name='X')
y = tf.placeholder(tf.float32, shape=[None, n_classes], name='Y')
print("hello")
train_neural_network(x)

afficher_un_ECG(listeECG)


