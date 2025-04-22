# Analysis Code for "Revealing Rotational Characteristics of the Uniflagellate Mutant of Chlamydomonas reinhardtii through DeepLabCut-Based Autotracking" (microPublication Biology 10.17912/micropub.biology.001535)

This repository contains the analysis code used in the publication:

> Azusa Kage, Ken H. Nagai, Takayuki Nishizaka, Kenta Ishimoto. "Revealing Rotational Characteristics of the Uniflagellate Mutant of Chlamydomonas reinhardtii through DeepLabCut-Based Autotracking." *microPublication Biology*, 10.17912/micropub.biology.001535.
https://micropublication.org/journals/biology/micropub-biology-001535

## Contents

- `main_analysis.py`: Main analysis pipeline  

## How to Run

1. Clone this repository:
    ```bash
    git clone https://github.com/kageazusa/uni.git
    cd uni
    ```

2. Prepare the CSV data:  
   Download the analyzed data (DeepLabCut output) from Zenodo and unzip it into any directory:

   https://zenodo.org/records/15098911

3. Edit the name of the directory in the main_analysis.py (Lines 26 and 30).

4. Run the main script:
    ```bash
    python main_analysis.py
    ```


## Data Availability

The raw data used in this analysis is available on Zenodo:

[https://zenodo.org/records/15098911](https://zenodo.org/records/15098911)

Please cite both this code repository and the Zenodo dataset when reusing the material.

## Licensing and Attribution

This repository is licensed under the **Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0)** license.  
See the [`LICENSE`](./LICENSE) file for more details.

Some portions of the code are adapted or copied from third-party sources:

- Lines 35–43 of `main_analysis.py` are adapted from a Stack Overflow Japan post by user "neco":  
  https://ja.stackoverflow.com/questions/23275/  
  Licensed under CC BY-SA 3.0

- Lines 46–83 of `main_analysis.py` are copied from code by "Akehi":  
  https://akehi.github.io/containts/20161119_angle/anglelib.html  
  Licensed under CC BY 3.0 as specified in:  
  https://github.com/Akehi/Akehi.github.io/blob/master/LICENSE.txt

## Contact

For questions or feedback, please contact:  
Azusa Kage (@kageazusa)
