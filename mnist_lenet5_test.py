#coding:utf-8
import time    # 为了延时
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import mnist_lenet5_forward
import mnist_lenet5_backward
import numpy as np

TEST_INTERVAL_SECS = 5

def test(mnist):
    # 复现计算图
    with tf.Graph().as_default() as g: 
        x = tf.placeholder(tf.float32,[
            mnist.test.num_examples,
            mnist_lenet5_forward.IMAGE_SIZE,
            mnist_lenet5_forward.IMAGE_SIZE,
            mnist_lenet5_forward.NUM_CHANNELS]) 
        y_ = tf.placeholder(tf.float32, [None, mnist_lenet5_forward.OUTPUT_NODE])
        y = mnist_lenet5_forward.forward(x,False,None)  # 用前向传播过程计算出y的值
                                                        # 因为测试中使用的是训练好的神经网络，所以不需要dropout

        # 实例化带滑动平均值的saver对象
        ema = tf.train.ExponentialMovingAverage(mnist_lenet5_backward.MOVING_AVERAGE_DECAY)
        ema_restore = ema.variables_to_restore()
        saver = tf.train.Saver(ema_restore)
		
        # 判断预测值和实际值是否相同
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1)) 
        # 求平均得到准确率
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32)) 

        # 加载ckpt，即把滑动平均值赋给各个参数
        while True:
            with tf.Session() as sess:
                # 加载ckpt模型
                ckpt = tf.train.get_checkpoint_state(mnist_lenet5_backward.MODEL_SAVE_PATH)
                # 如果有ckpt模型，则恢复该模型
                if ckpt and ckpt.model_checkpoint_path:
                    # 恢复模型到当前会话
                    saver.restore(sess, ckpt.model_checkpoint_path)
                    # 恢复轮数
                    # 根据读入模型的名字判断该模型属于迭代了多少次保存的
                    global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1] 
                    reshaped_x = np.reshape(mnist.test.images,(
                                                        mnist.test.num_examples,
                                            	        mnist_lenet5_forward.IMAGE_SIZE,
                                            	        mnist_lenet5_forward.IMAGE_SIZE,
                                            	        mnist_lenet5_forward.NUM_CHANNELS))
                    # 计算准确率
                    accuracy_score = sess.run(accuracy, feed_dict={x:reshaped_x,y_:mnist.test.labels}) 
                    print("After %s training step(s), test accuracy = %g" % (global_step, accuracy_score))
                # 如果没有ckpt模型    
                else:
                    print('No checkpoint file found')
                    return
            time.sleep(TEST_INTERVAL_SECS)  # 每隔5秒寻找一次是否有最新的模型

def main():
    # 读入数据集
    mnist = input_data.read_data_sets("./data/", one_hot=True)
    test(mnist)

if __name__ == '__main__':
    main()
