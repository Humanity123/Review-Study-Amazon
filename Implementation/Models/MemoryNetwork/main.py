import os 
import tensorflow as tf

from model import MemN2N

flags = tf.app.flags

flags.DEFINE_integer("batch_size", 100, "batch size for training [100]") // actual value to be filled later
flags.DEFINE_float("init_std", 0.05, "weight initialization std [0.05]")
flags.DEFINE_string("data_name", "reviews_us", "data set name [reviews_us]")
flags.DEFINE_string("checkpoint_dir", "checkpoints", "String: Directory name for checkpoints [checkpoints]")
flags.DEFINE_string("data_dir", "data", "String: Directory name for checkpoints [data]")
flags.DEFINE_boolean("is_test", False, "Boolean: False for training phase; True for testing phase [False]")

FLAGS = flags.FLAGS

def main():
	if not os.path.exists(FLAGS.checkpoint_dir):
      os.makedirs(FLAGS.checkpoint_dir)
	
	train_data = read('%s/%s.train.txt'%(FLAGS.data_dir, FLAGS.data_name))
	validation_data = read('%s/%s.validation.txt'%(FLAGS.data_dir, FLAGS.data_name))
	test_data = read('%s/%s.test.txt'%(FLAGS.data_dir, FLAGS.data_name))



if __name__ == "__main__":
	tf.app.run()