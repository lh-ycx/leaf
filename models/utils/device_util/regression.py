import tensorflow as tf
import numpy as np
import os
import json

def regression_lookup_table(device, layer):
    with open(os.path.join('regression', device, '{}.json'.format(layer)), 'r', encoding='utf-8') as f:
        d=json.load(f)
    features = np.array(d['X'])
    labels = np.array(d['Y'])
    rate = int(0.85 * len(labels))
    train_features = features[:rate]
    test_features = features[rate:]
    train_labels = labels[:rate]
    test_labels = labels[rate:]

    tf_x = tf.placeholder(tf.float32, [None, train_features.shape[1]], name='features')  # input x
    tf_y = tf.placeholder(tf.float32, [None, train_labels.shape[1]], name='labels')  # input y

    l1 = tf.layers.dense(tf_x, 10, tf.nn.relu)  # hidden layer
    l2 = tf.layers.dense(l1, 5, tf.nn.relu)
    output = tf.layers.dense(l2, 1)  # output layer
    loss = tf.losses.mean_squared_error(tf_y, output)  # compute cost
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.5)
    train_op = optimizer.minimize(loss)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        tf.add_to_collection('pred_network', output)
        best_loss = None
        n_epoch = 10000000
        layer = layer.split('_')[0]
        save_dir = os.path.join('checkpoint/lookup_table', device, layer)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        for epoch in range(n_epoch):
            _, l, pred = sess.run([train_op, loss, output], feed_dict={tf_x: train_features, tf_y: train_labels})            
            if epoch % 1000 == 0:
                if not best_loss or l < best_loss:
                    best_loss = l
                    saver.save(sess, os.path.join(save_dir, '{}.ckpt'.format(layer)))
                print(epoch, l)


if __name__ == '__main__':
    device_list = ['sumsung_note10', 'redmi_note8', 'nexus6']
    layer_list = ['embedding', 'lstm', 'output']
    for l in layer_list:
            regression_lookup_table('sumsung_note10', l)