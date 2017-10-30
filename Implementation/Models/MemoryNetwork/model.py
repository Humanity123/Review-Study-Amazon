import tensorflow as tf
import random


class model(object):
	def __init__(self, config):
		''' constructor for Memory Neotwork Model '''
		self.batch_size = config.batch_size
		self.lmda       = config.lmda
		self.init_std   = config.int_dev
		self.hops       = config.hops 	
		self.dim        = config.dim
	
	def build_model(self):
		''' builds the memory network by initialising all the weights '''
		self.q = tf.placeholder(tf.float32, [None, 1], name="q")
		self.x = tf.placeholder(tf.float32, [None, None, 1], name="x")

		self.B = tf.Variable(tf.random_normal([self.dim, self.N_target], stddev=self.init_std), name = 'B')
		self.A_t = tf.Variable(tf.random_normal([self.dim, self.N_voc], stddev=self.init_std), name = 'A_t')
		self.Vq_t = tf.Variable(tf.random_normal([self.dim, self.dim], stddev=self.init_std), name = 'Vq_t')
		self.C_t = tf.Variable(tf.random_normal([self.dim, self.N_voc], stddev=self.init_std), name = 'C_t')

		self.A_p = tf.Variable(tf.random_normal([self.dim, self.N_voc], stddev=self.init_std), name = 'A_p')
		self.Vq_p = tf.Variable(tf.random_normal([self.dim, self.dim], stddev=self.init_std), name = 'Vq_p')
		self.C_p = tf.Variable(tf.random_normal([self.dim, self.N_voc], stddev=self.init_std), name = 'C_p')

		self.W_t = tf.Variable(tf.random_normal([2, self.dim], stddev=self.init_std), name = 'W_t')
		self.W_t = tf.Variable(tf.random_normal([3, self.dim], stddev=self.init_std), name = 'W_p')

		self.H_t = tf.Variable(tf.random_normal([self.dim, self.dim], stddev=self.init_std), name = 'H_t')
		self.H_p = tf.Variable(tf.random_normal([self.dim, self.dim], stddev=self.init_std), name = 'H_p')

		u   = tf.nn.embedding_lookup(self.B, self.q)

		x_embed_A_t = tf.nn.embedding_lookup(tf.transpose(self.A_t), self.x)
		x_embed_reshaped_A_t = tf.reshape(x_embed_A_t, [-1, self.dim])
		m_t = tf.reshape(tf.transpose(tf.matmul(self.Vq_t, tf.transpose(x_embed_reshaped_A_t))), [-1, tf.shape(self.x)[1], self.dim])
		
		x_embed_C_t = tf.nn.embedding_lookup(tf.transpose(self.C_t), self.x)
		x_embed_reshaped_C_t = tf.reshape(x_embed_C_t, [-1, self.dim])
		c_t = tf.reshape(tf.transpose(tf.matmul(self.Vq_t, tf.transpose(x_embed_reshaped_C_t))), [-1, tf.shape(self.x)[1], self.dim])

		a_t_avg = None
		for hop in range(self.hops):
			u_expanded_dim = tf.expand_dims(u, 2)
			a_t = tf.nn.softmax(tf.squeeze(tf.matmul(m_t, u_expanded_dim),2))

			a_t_expanded_dim = tf.expand_dims(a_t, 1)
			o_t = tf.squeze(tf.matmul(a_t_expanded_dim, c_t), 1)

			if a_t_avg is None:
				a_t_avg = a_t
			else
				a_t_avg = tf.add(a_t_avg, a_t)
			
			z = tf.add(o_t, tf.transpose(tf.matmul(self.H_t, tf.transpose(u))))
			u = tf.nn.sigmoid(z)

		y_t = tf.nn.softmax(tf.transpose(tf.matmul(self.W_t, tf.transpose(u))))

		x_embed_A_p = tf.nn.embedding_lookup(tf.transpose(self.A_p), self.x)
		x_embed_reshaped_A_p = tf.reshape(x_embed_A_p, [-1, self.dim])
		m_p = tf.reshape(tf.transpose(tf.matmul(self.Vq_p, tf.transpose(x_embed_reshaped_A_p))), [-1, tf.shape(self.x)[1], self.dim])

		x_embed_C_p = tf.nn.embedding_lookup(tf.transpose(self.C_t), self.x)
		x_embed_reshaped_C_p = tf.reshape(x_embed_C_p, [-1, self.dim])
		c_p = tf.reshape(tf.transpose(tf.matmul(self.Vq_t, tf.transpose(x_embed_reshaped_C))), [-1, tf.shape(self.x)[1], self.dim])
		
		a_t_avg = tf.scalar_mul(1.0/self.hops, a_t_avg)

		a_t_avg = tf.divide(tf.cumsum(a_t_avg, axis = 1), tf.cast(tf.range(1, tf.shape(a_t_avg)[1]+1), tf.float32))

		for hop in range(self.hops):
			u_expanded_dim = tf.expand_dims(u, 2)
			a_p = tf.nn.softmax(tf.squeeze(tf.matmul(m_p, u_expanded_dim),2))

			b_p =  tf.add(tf.scalar_mul(1-self.lmda, a_p), tf.scalar_mul(self.lmda, a_t_avg))

			b_p_expanded_dim = tf.expand_dims(b_p, 1)
			o_p = tf.squeze(tf.matmul(b_p_expanded_dim, c_p), 1)			

			z = tf.add(o_p, tf.transpose(tf.matmul(self.H_p, tf.transpose(u))))
			u = tf.nn.sigmoid(z)

		y_p = tf.nn.softmax(tf.transpose(tf.matmul(self.W_p, tf.transpose(u))))

		return (y_t, y_p)