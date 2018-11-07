from Utilitaires import *
import tensorflow as tf
import os
import matplotlib.pyplot as plt
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#
#   Gestion des données d'entrée
#

listeECG = load_animal_datas()
x_train,y_train = create_train_homogene_2(listeECG)
x_test,y_test = create_test_semi_random(listeECG)
#listePara = []

#x_test_true, y_test_true = create_test_true(listeECG)
#x_test_false, y_test_false = create_test_false(listeECG)


#
#   Gestion des couches RDN
#

n_input = len(x_train[0]['SMA'])+len(x_train[0]['EMA'])+1 # input layer (28x28 pixels)
n_hidden1 = 2 # 1st hidden layer
n_hidden2 = 3 # 2nd hidden layer
n_hidden3 = 2 # 3rd hidden layer
#n_output = 2   # output layer (0-9 digits)
n_output = 1

weights =   {
    'w1': tf.Variable(tf.truncated_normal([121, n_hidden1], stddev=0.1)),
    'w2': tf.Variable(tf.truncated_normal([n_hidden1, n_hidden2], stddev=0.1)),
    'w3': tf.Variable(tf.truncated_normal([n_hidden2, n_hidden3], stddev=0.1)),
    'out': tf.Variable(tf.truncated_normal([n_hidden3, n_output], stddev=0.1)),
            }

biases =    {
    'b1': tf.Variable(tf.constant(0.1, shape=[n_hidden1])),
    'b2': tf.Variable(tf.constant(0.1, shape=[n_hidden2])),
    'b3': tf.Variable(tf.constant(0.1, shape=[n_hidden3])),
    'out': tf.Variable(tf.constant(0.1, shape=[n_output]))
            }

keep_prob = tf.placeholder("float")

def multilayer_perceptron(x, weights, biases, keep_prob):
    layer_1 = tf.add(tf.matmul(x, weights['w1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    layer_2 = tf.add(tf.matmul(layer_1, weights['w2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)
    layer_3 = tf.add(tf.matmul(layer_2, weights['w3']), biases['b3'])
    layer_3 = tf.nn.relu(layer_3)
    #layer_drop = tf.nn.dropout(layer_3, keep_prob)
    output = tf.matmul(layer_3, weights['out']) + biases['out']
    return output

def train_neural_network_1(x, y):
    prediction = multilayer_perceptron(x, weights, biases, keep_prob)
    cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=prediction, labels=y))
    optimizer = tf.train.AdamOptimizer(learning_rate=0.0000001).minimize(cost)

    hm_epochs = 20000
    with tf.Session() as sess:
        # OLD:
        # sess.run(tf.initialize_all_variables())
        # NEW:
        sess.run(tf.global_variables_initializer())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            epoch_x, epoch_y = get_epoch(x_train, y_train)
            a,c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
            epoch_loss += c
            if epoch % 1000 == 0:
                print('Epoch', epoch, 'completed out of', hm_epochs, 'loss:', epoch_loss)

        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        test_x, test_y = get_epoch(x_test,y_test)
        #test_x_true, test_y_true = get_epoch(x_test_true, y_test_true)
        #test_x_false, test_y_false = get_epoch(x_test_false, y_test_false)
        print('Accuracy:', accuracy.eval({x: test_x, y: test_y}))
        #print('Accuracy true:', accuracy.eval({x: test_x_true, y: test_y_true}))
        #print('Accuracy false:', accuracy.eval({x: test_x_false, y: test_y_false}))

        #saver = tf.train.Saver()
        #save_path = saver.save(sess, "./my_model_final.ckpt")
        #saver.restore(sess, save_path)
        #accuracy_val = accuracy.eval(feed_dict={x: test_x_true, y: test_y_true})
        #print(accuracy_val)


def train_neural_network_2(x,y):
    prediction = multilayer_perceptron(x, weights, biases, keep_prob)
    prediction = (tf.nn.sigmoid(prediction))
    learningRate = 0.00005
    #cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=prediction, labels=y))
    cost = tf.reduce_mean(tf.nn.weighted_cross_entropy_with_logits(logits=prediction, targets=y, pos_weight=0.1))
    optimizer = tf.train.AdamOptimizer(learning_rate =learningRate).minimize(cost)

    hm_epochs = 30000
    train_keep_prob = 0.5
    listeEpoch = []
    with tf.Session() as sess:
        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())
        epoch_x, epoch_y = get_epoch(x_train, y_train)

        for epoch in range(hm_epochs):
            epoch_loss = 0
            #a,c = sess.run([optimizer, cost], feed_dict={x: epoch_x[epoch:epoch+1], y: epoch_y[epoch:epoch+1], keep_prob:train_keep_prob})
            a, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y, keep_prob: train_keep_prob})
            epoch_loss += c
            listeEpoch.append(epoch_loss)


        saver.save(sess, "./monRDN")
        #saver.restore(sess,"./my_time_series_model")
        #correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
        predicted_class = tf.greater(prediction, 0.5)
        correct = tf.equal(predicted_class, tf.equal(y, 1.0))

        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        test_x, test_y = get_epoch(x_test,y_test)
        #print('Accuracy:', accuracy.eval({x: test_x, y: test_y}))
        acc_train = accuracy.eval(feed_dict={x:  epoch_x, y:  epoch_y})
        acc_test = accuracy.eval(feed_dict={x: test_x, y: test_y})
        print( "Train accuracy:", acc_train, "Test accuracy:", acc_test)
        y_pred = sess.run(prediction, feed_dict={x: test_x})
        #print (test_y)
        a, b = sess.run([accuracy, prediction], feed_dict={x: test_x,y : test_y})
        plt.subplot(2, 1, 1)
        plt.plot(b, 'b', marker='+')
        b = np.transpose(b)
        print('Test Accuracy:', b)
        plt.plot(test_y, 'r', marker='*')
        plt.subplot(2, 1, 2)
        plt.plot(listeEpoch)
        plt.show()
        #listePara.append(n_hidden1, n_hidden2, n_hidden3, learningRate, acc_train, acc_test)

x = tf.placeholder(tf.float32, shape=[None,121], name='X')
y = tf.placeholder(tf.float32, shape=[None, n_output], name='Y')
train_neural_network_2(x, y)

#fichier = open("./parameters.txt", "a")
#fichier.write(listePara)
#fichier.close()
#afficher_un_ECG(listeECG)


