import BloomFilter
import numpy as np
import sys
import string



def test_BloomFilter(input_list, test_list, bf, WRITE_FILE=False, CUSTOM=False):
    '''
    Test the function of Bloom filter
    input_list: a list of string to be added to the filter
    test_list: a list of strings used for testing
    bf: a Bloom Filter instance
    WRITE_FILE: flag to determine weather or not to write the testing results into a file
    '''
    fp_list = []
    fn_list = []
    # Add items into the Bloom filter defined
    for item in input_list:
        bf.add(item) 
    
    print(f"\nThe size of the Bloom filter is {bf.size} bits, and it is designed for a false positive rate of {bf.fp_prob}\n")
    print(f"The number of strings stored in the filter is: {len(input_list)}\n")
    print(f"The number of strings to be tested is: {len(test_list)}\n")
   
    # Look up each test item
    if WRITE_FILE:
        f = open('test_result.txt', 'w')
        print("The results are saved in file test_result.txt")
        
        f.write("="*50 + "\nThe following lines are the details of the result\n" + "="*50 + "\n")
        for item in test_list:
            if bf.lookup(item):
                f.write(f"'{item}' probabily exists.\n")
                if item not in input_list:
                    fp_list.append(item)
                    f.write(" "*20 + f"--- This is a FALSE positive!\n")
            else:
                f.write(f"'{item}' definitely doesn't exists.\n")
        
        f.write("="*50 + "\nResult Summary\n" + "="*50 + "\n")
        f.write(f"The size of the Bloom filter is {bf.size} bits, and it is designed for a false positive rate of {bf.fp_prob}\n\n")
        f.write(f"The number of strings stored in the filter is: {len(input_list)}\n")
        f.write(f"The number of strings to be tested is: {len(test_list)}\n")
        f.write(f"The number of FALSE positives occured: {len(fp_list)}\n")
        f.write(f"The false positive rate for the test strings is: {len(fp_list)/len(test_list)}\n")
        f.write(f"False positive list: {fp_list}\n")
        f.write(f"False negative list: {fn_list}\n")
        f.close()      
    else:
        print("="*50, "\nThe following lines are the details of the result\n", "="*50, "\n")    
        for item in test_list:
            if bf.lookup(item):
                print(f"'{item}' probabily exists.")
                if item not in input_list:
                    fp_list.append(item)
                    print(" "*20 + f"--- This is a FALSE positive!")
            else:
                print(f"'{item}' definitely doesn't exists.")
                if item in input_list:
                    fn_list.append(item)
                    print(" "*20 + f"--- This is a FALSE negative!")
        if not CUSTOM:         
            print(f"The number of FALSE positives occured: {len(fp_list)}\n")
            print(f"The false positive rate for the test strings is: {len(fp_list)/len(test_list)}\n")
            print(f"The number of FALSE Negatives occured: {len(fn_list)}\n")
            print(f"The false negative rate for the test strings is: {len(fn_list)/len(test_list)}\n")
            
    return fp_list, fn_list


            
            
            
            
def main(argv):
    if len(argv) != 2:
        print("Usage: python3 test.py [simple,speller,custom]")
        print("Please choose one of the three different tests.")
        sys.exit(2)  # command line syntax error
    
    if argv[1] == 'simple':
        input_list = ['apple', 'banana', 'pear', 'peach', 'amazon', 'grapes']
        test_list = ['apple', 'cherry', 'train', 'david', 'pineapple']
        print(f"Added list: {input_list}")
        print(f"Test list: {test_list}")

        simpleBF = BloomFilter.simpleBloomFilter(len(input_list), 0.01)
        fp_list,fn_list = test_BloomFilter(input_list, test_list, simpleBF)
        print(f"False positive list: {fp_list}")
        print(f"False negative list: {fn_list}")
        
    elif argv[1] == 'speller':
        infile = open('large_dictionary', 'r')
        dictionary_data = infile.read().splitlines()
        infile.close()
    
        infile = open('lalaland.txt', 'r')
        test_data = infile.read()
        table = str.maketrans({key: None for key in string.punctuation})
        test_data = list(set(test_data.translate(table).split()))
        
        print(f"Added strings from file 'large_dictionary'")
        print(f"Test strings from file 'lalaland.txt'")
        print(f"Dictionary words count: {len(dictionary_data)}")
        print(f"Text unique words count: {len(test_data)}")

        filter_size = BloomFilter.simpleBloomFilter.get_size(len(dictionary_data), 0.1)
        print(f"Size of the filter: {filter_size} bits = {filter_size/8} bytes")
        print("Desired false positive rate: 0.1")
        print(" =========   Results   ==========")
        fp_prob = 0.1
        simpleBF = BloomFilter.simpleBloomFilter(len(dictionary_data), fp_prob)
        fp_list, fn_list = test_BloomFilter(dictionary_data, test_data, simpleBF, WRITE_FILE=True)
        
    
    elif argv[1] == 'custom':
        input_list = eval(input("Please type a list of strings you want to add to the filter :\n"))
        fp_prob = float(input("What's your prefered false positive rate?   "))
        simpleBF = BloomFilter.simpleBloomFilter(len(input_list), fp_prob)
        
        while True:
            test_string = input("Please type the string you want to test: \n")    
            _,_ = test_BloomFilter(input_list, [test_string], simpleBF, CUSTOM=True)
       
    else:
        print("Usage: python3 test.py [simple,speller,custom]")
        print("You can only choose one from the three given tests.")
        sys.exit(1)  # other error 

    
if __name__ == "__main__":
    main(sys.argv)
    

