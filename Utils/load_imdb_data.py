from pandas import read_csv, concat

def load_imdb_data():

    train_pos_file_path = "../data/train-pos.txt"
    train_neg_file_path = "../data/train-pos.txt"
    test_pos_file_path = "../data/test-pos.txt"
    test_neg_file_path = "../data/test-neg.txt"

    #read file from train_pos_file_path, create a df and set labels as 1
    train_pos_df = read_csv(train_pos_file_path, sep='\n', header = None)

    #add column for labels and set labels as 1
    train_pos_df.columns = ['review']
    train_pos_df['sentiment'] = 1

    # do likewise for rest 3 files

    train_neg_df = read_csv(train_neg_file_path, sep='\n', header = None)
    train_neg_df.columns = ['review']
    train_neg_df['sentiment'] = -1

    test_pos_df = read_csv(test_pos_file_path, sep='\n', header = None)
    test_pos_df.columns = ['review']
    test_pos_df['sentiment'] = 1
    
    test_neg_df = read_csv(test_neg_file_path, sep='\n', header = None)
    test_neg_df.columns = ['review']
    test_neg_df['sentiment'] = -1

    data_frame = concat([train_pos_df, train_neg_df, test_pos_df, test_neg_df], ignore_index=True)

    return data_frame
