# Rest_thoughts

**Jin Ke, Taylor A. Chamberlain, Hayoung Song, Anna Corriveau, Ziwei Zhang, Taysha Martinez, Laura Sams, Marvin M. Chun, Yuan Chang Leong, Monica D. Rosenberg. (2025). Ongoing thoughts at rest reflect functional brain organization and behavior. _bioRvix_**  

Correspondence to jin.ke@yale.edu and mdrosenberg@uchicago.edu
         
**The Chicago Attentin ang Thoughts (CAT) Dataset**

60 participants performed up to four 10-minute runs of an annotated rest task as part of a two-session fMRI study that also collected movie-watching, continuous performance task, and post-scan memory and narrative engagement data. Each run of the annotated rest task had 8 trials. In each trial, participants rested for 30 seconds, verbally reported their ongoing thoughts during the preceding resting period for 10 seconds, and rated them on 9 dimensions on a 9-point scale. 

* The functional and structural MRI data will be publicly available on OpenNeuro when the paper gets published. Link: https://openneuro.org/datasets/ds006515
* The associated behavioral data are available here: https://github.com/jinke828/rest_thoughts/tree/main/data/beh
* The transcriptions of each individual’s spontaneous speech and its USE-semantic embeddings will not be open sourced due to privacy concerns.
* Preprocessed fMRI and eyetracking data are available upon reasonable request.

**Code**

We provide a step-by-step, very detailed instructions to run the scripts that replicate the key findings of this paper (i.e., brain decoding of ongoing thoughts): 
[Code Guide](https://github.com/jinke828/rest_thoughts/blob/main/Code%20guide_JK.pdf)

The instructions cover code of these following steps:
* **Step00**: preprocess the fMRI data downloaded from OpenNeuro [./code/a_preprocessing](https://github.com/jinke828/rest_thoughts/tree/main/code/a_preprocessing)
* Step01: load the preprocessed fMRI data [step01_load_netts.m]()
* Step02: calculate FC patterns for each trial [step02_calc_FC.ipynb]
* Step03: representational similarity analysis [step03_FC-thoughts_RSA.ipynb]
* Step04: connectome-based modeling to predict thought dimensions
 - (step4a)
