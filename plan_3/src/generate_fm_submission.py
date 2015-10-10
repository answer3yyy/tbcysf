from test_builder import 



if __name__ == "__main__":
    test_decoder = TestDecoder()

    test_feature_file = ''
    pred_items_file   = ''
    num = 200
    pred_fm_res_file  = ''
    test_decoder.decode(test_feature_file, pred_items_file, num, pred_fm_res_file)
