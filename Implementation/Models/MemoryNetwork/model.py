import tensorflow as tf
import random


class model(object):
	def __init__(self, config):
		''' constructor for Memory Neotwork Model '''
		self.batch_size = config.batch_size
		self.init_std   = config.int_dev 
		pass

	def build_model(self):
		self.
		self.B = tf.Variable(tf.random_normal([self.dim, self.N_target], stddev=self.init_std), name = 'B')
		self.A_t = tf.Variable(tf.random_normal([self.dim, self.N_voc], stddev=self.init_std), name = 'A_t')
		self.Vq_t = tf.Variable(tf.random_normal([self.dim, self.dim], stddev=self.init_std), name = 'Vq_t')
		self.C_t = tf.Variable(tf.random_normal([self.dim, self.N_voc], stddev=self.init_std), name = 'C_t')

		self.A_p = tf.Variable(tf.random_normal([self.dim, self.N_voc], stddev=self.init_std), name = 'A_p')
		self.Vq_p = tf.Variable(tf.random_normal([self.dim, self.dim], stddev=self.init_std), name = 'Vq_p')
		self.C_p = tf.Variable(tf.random_normal([self.dim, self.N_voc], stddev=self.init_std), name = 'C_p')

