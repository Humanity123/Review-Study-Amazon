def get_list_from_table_dump(dump_file_path, num_columns):
	''' parse the sql table dump contain num_column number of columns assuming
	separated by tabs assuming the first row contains the columns names'''
	with open(dump_file_path, 'r') as dump_file:
		column_names = []
		records = []
		tokens = dump_file.read().split('\t')
		column_names = tokens[:num_columns]
		for index in range(1, len(tokens)/num_columns):
			record = {}
			for column_index in range(num_columns):
				record[column_names[column_index]] = tokens[num_columns*index+column_index]
			records.append(record)

	return records



