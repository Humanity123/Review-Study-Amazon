def abstract_change(sentiment_flow):
	''' deletes repeating local sentiment in the sentiment flow as mentioned in the paper
	Sentiment Flow – A General Model of Web Review Argumentation; Sentiment Flow Abstraction Technique '''

	abstract_change_sentiment_flow = sentiment_flow[:1]
	for index, sentiment in enumerate(sentiment_flow[1:]):
		if sentiment == sentiment_flow[index]: continue
		abstract_change_sentiment_flow.append(sentiment)

	return abstract_change_sentiment_flow

def abstract_2class(sentiment_flow, sentiment_type):
	''' deletes all instance of a local sentiment from the sentiment flow as mentioned in the paper 
	Sentiment Flow – A General Model of Web Review Argumentation; Sentiment Flow Abstraction Technique '''		

	abstract_2class_sentiment_flow = [sentiment if sentiment != sentiment_type for sentiment in sentiment_flow]
	return abstract_2class_sentiment_flow

def is_loop(flow_head1, flow_head2, length, sentiment_flow):
	''' checks if the two flows are equal are not and is made of atleast two local sentiments '''
	
	if max(flow_head1, flow_head2) + length > len(sentiment_flow) or len(set(sentiment_flow[flow_head1:flow_head1+length])) <= 1:
		return False

	return  (sentiment_flow[flow_head1:flow_head1+length] == sentiment_flow[flow_head2:flow_head2+length])

def abstract_no_loops(sentiment_flow):
	''' deletes repeating sequences of two or more local sentiments as mentioned in the paper
	Sentiment Flow – A General Model of Web Review Argumentation; Sentiment Flow Abstraction Technique '''		

	abstract_no_loops_sentiment_flow = []
	sentiment_dic = {}
	for index in range(len(sentiment_flow)):
		sentiment = sentiment_flow[index]
		if sentiment not in sentiment_dic:
			sentiment_dic[sentiment] = [index]
			abstract_no_loops_sentiment_flow.append(sentiment)
		else:
			if is_loop(index, sentiment_dic[sentiment][-1], index-sentiment_dic[sentiment][-1], sentiment_flow):
				index += index - sentiment_dic[sentiment][-1]
			else:
				sentiment_dic[sentiment].append(index)
				abstract_no_loops_sentiment_flow.append(sentiment)	

	return abstract_no_loops_sentiment_flow

def main():
	return 0	
if __name__ == "__main__":
	main()