import tensorflow as tf
import numpy as np
import random


class model(object):
	def __init__(self, config, sess):
		''' constructor for Memory Neotwork Model '''
		self.batch_size = config.batch_size
		self.N_target   = config.N_target
		self.N_voc      = config.N_voc
		self.lmda       = config.lmda
		self.init_std   = config.int_dev
		self.hops       = config.hops 	
		self.dim        = config.dim
		self.sess       = sess
		self.step       = 0
	
	def build_model(self):
		''' builds the memory network by initialising all the weights '''
		self.global_step = tf.Variable(0, name="global_step")

		self.q = tf.placeholder(tf.float32, [None, 1], name="q")
		self.x = tf.placeholder(tf.float32, [None, None, 1], name="x")
		self.label_t = tf.placeholder(tf.placeholder, [None, 1], name="label_t")
		self.label_p = tf.placeholder(tf.placeholder, [None, 1], name="label_p")

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

		self.y_t = tf.nn.softmax(tf.transpose(tf.matmul(self.W_t, tf.transpose(u))))

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

		self.y_p = tf.nn.softmax(tf.transpose(tf.matmul(self.W_p, tf.transpose(u))))

		cross_entropy_loss_t = tf.nn.softmax_cross_entropy_with_logits(labels = self.label_t, logits = self.y_t)
		cross_entropy_loss_p = tf.nn.softmax_cross_entropy_with_logits(labels = self.label_p, logits = self.y_p)
		cross_entropy_conditional_loss_p = tf.multiply(tf.transpose(tf.gather(tf.transpose(self.label_t), [1])), cross_entropy_loss_p)
		
		self.loss = -1 * tf.reduce_sum(tf.add(cross_entropy_loss_t, cross_entropy_conditional_loss_p))

		self.optim = tf.train.AdamOptimizer(learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-08).minimize(loss = loss, global_step = self.global_step)

		tf.global_variables_initializer().run()
		self.saver = tf.train.Saver()
	

	def train(self, data, val_data):
		''' trains the model on the given data '''
		num_batches = int(math.ceil(len(data) / self.batch_size))

		for epoch in range(self.epochs):
			loss_list = []
			for batch in data[::self.batch_size]:
				train_q, train_c, train_y_t, train_y_p = data
				 _, loss, self.step = self.sess.run([self.optim, self.loss, self.global_step], feed_dict={
                                                    self.q: train_q,
                                                    self.c: train_c,
                                                    self.y_t: train_y_t,
                                                    self.y_p: train_y_p})
				loss_list.append(loss)
			
			if epoch % 1 == 0:
				val_loss = self.test(val_data)

				state = {
					'Loss Avg': np.mean(loss_list)
					'Loss std_dev': np.std(loss_list)
					'Val loss': val_loss
				}
				print state

			if epoch % 5 == 0:
                self.saver.save(self.sess,
                                os.path.join(self.checkpoint_dir, "MemN2N.model"),
                                global_step = self.step.astype(int))

    def test(self, data):
    	''' tests the model on the given data'''
    	num_batches = int(math.ceil(len(data) / self.batch_size))

		for batch in data[::self.batch_size]:
			test_q, test_c, test_y_t, test_y_p = data
			loss = self.sess.run([self.loss], feed_dict={
                                                self.q: test_q,
                                                self.c: test_c,
                                                self.y_t: test_y_t,
                                                self.y_p: test_y_p})

		return loss

	def run(self, train_data, test_data):
		''' a function to train or test the memory network depending on the is_test flag'''
        if not self.is_test:
        	self.train(train_data, test_data)
            train_loss = np.sum(self.train(train_data))
            test_loss = np.sum(self.test(test_data, label='Validation'))
      
        else:
            self.load()

            valid_loss = self.test(train_data)
            test_loss  = self.test(test_data)

            state = {
                'valid_perplexity': math.exp(valid_loss),
                'test_perplexity': math.exp(test_loss)
            }
            print state
	
	def load(self):
		''' loads the latest saved checkpoint '''
        print(" [*] Reading checkpoints...")
        ckpt = tf.train.get_checkpoint_state(self.checkpoint_dir)
        if ckpt and ckpt.model_checkpoint_path:
            self.saver.restore(self.sess, ckpt.model_checkpoint_path)
        else:
            raise Exception(" [!] Trest mode but no checkpoint found")