import os 
import tensorflow as tf
import pprint

from data import read_data
from model import MemN2N

pp = pprint.PrettyPrinter()

flags = tf.app.flags

flags.DEFINE_integer("hops", 3, "number of layers/hops [3]")
flags.DEFINE_integer("dim", 300, "number of layers/hops [300]")	# actual value to be filled later
flags.DEFINE_integer("batch_size", 100, "batch size for training [100]") # actual value to be filled later
flags.DEFINE_float("init_std", 0.05, "weight initialization std [0.05]")
flags.DEFINE_float("lmda", 0.5, "weight initialization std [0.5]")
flags.DEFINE_string("data_name", "reviews_us", "data set name [reviews_us]")
flags.DEFINE_string("checkpoint_dir", "checkpoints", "String: Directory name for checkpoints [checkpoints]")
flags.DEFINE_string("data_dir", "data", "String: Directory name for checkpoints [data]")
flags.DEFINE_boolean("is_test", False, "Boolean: False for training phase; True for testing phase [False]")

FLAGS = flags.FLAGS

def main(obj):
	if not os.path.exists(FLAGS.checkpoint_dir):
      os.makedirs(FLAGS.checkpoint_dir)
	
	count_c = []
    word2idx_c = {}
	
	count_t = []
	word2idx_t = {}

	train_data_t = read_data('%s/%s.train_t.txt'%(FLAGS.data_dir, FLAGS.data_name), count_t, word2idx_t)
	validation_data_t = read_data('%s/%s.validation_t.txt'%(FLAGS.data_dir, FLAGS.data_name), count_t, word2idx_t)
	test_data_t = read_data('%s/%s.test_t.txt'%(FLAGS.data_dir, FLAGS.data_name), count_t, word2idx_t)

	train_data_c = read_data('%s/%s.train_c.txt'%(FLAGS.data_dir, FLAGS.data_name), count_c, word2idx_c)
	validation_data_c = read_data('%s/%s.validation_c.txt'%(FLAGS.data_dir, FLAGS.data_name), count_c, word2idx_c)
	test_data_c = read_data('%s/%s.test_c.txt'%(FLAGS.data_dir, FLAGS.data_name), count_c, word2idx_c)

	train_data_y_t = read('%s/%s.train_y_t.txt'%(FLAGS.data_dir, FLAGS.data_name))
	validation_data_y_t = read('%s/%s.validation_y_t.txt'%(FLAGS.data_dir, FLAGS.data_name))
	test_data_y_t = read('%s/%s.test_y_t.txt'%(FLAGS.data_dir, FLAGS.data_name))

	train_data_y_p = read('%s/%s.train_y_p.txt'%(FLAGS.data_dir, FLAGS.data_name))
	validation_data_y_p = read('%s/%s.validation_y_p.txt'%(FLAGS.data_dir, FLAGS.data_name))
	test_data_y_p = read('%s/%s.test_y_p.txt'%(FLAGS.data_dir, FLAGS.data_name))

	idx2word_c = dict(zip(word2idx_c.values(), word2idx_c.keys()))
	idx2word_t = dict(zip(word2idx_t.values(), word2idx_t.keys()))

	FLAGS.N_voc = len(word2idx_c)
	FLAGS.N_target = len(word2idx_t)
 	
 	pp.pprint(flags.FLAGS.__flags)

    with tf.Session() as sess:
        model = MemN2N(FLAGS, sess)
        model.build_model()

        if FLAGS.is_test:
            model.run((validation_data_t, validation_data_c, validation_y_t, validation_y_p), (test_data_t, test_data_c, test_y_t, test_y_p))
        else:
            model.run((train_data_t, train_data_c, train_y_t, train_data_y_p), validation_data_t, validation_data_c, validation_y_t, validation_y_p))

if __name__ == "__main__":
	tf.app.run()