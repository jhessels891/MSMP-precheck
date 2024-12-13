# MSMP+ with LSH, extensive data cleaning and pre-check

This page contains the code used for implementing MSMP+ with LSH, data cleaning and a key-value pre-check.

## Main
Running `main.py` executes the entire code. It first preprocesses and cleans the data according to `data_cleaning.py`. It then performs 10 bootstraps of the duplication detection method.

1. In `model_words.py`, model words are extracted and from these, binary vectors are created for each product.
2. In `minhashing.py`, these binary vectors are reduced in size using permutations. A signature matrix is created, which is the input for LSH.
3. Next, `lsh.py` is executed to obtain LSH candidate pairs.
  
## MSM   
4. The distance matrix used for clustering is generated in `msm.py`. Here, pairs not included in the LSH candidate pairs are assigned a dissimilarity of 100.
5. The LSH candidate pairs then go through the pre-check, including the brand check and common keys-value check. These can be found in `precheck.py`.
6. For the candidate pairs left after the pre-check, the three-part similarity function is calculated. The third part implements the TMWM, found in `tmwm.py`. Using the resulting distance matrix, hierarchical clustering is performed in `msm.py`, resulting in a set of detected duplicates.
7. The main function then calculates performance measures for the steps involved, and optimises the clustering threshold on a training data set. 

