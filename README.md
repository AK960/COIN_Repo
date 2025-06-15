# COIN Project Repository

## Directory Structure
The project contains the following directories to store resources:
- conda/: Contains an environment.yml file with the configurations of the conda environment and installed libraries that 
are used for scripting and data analysis. To create the environment and install the dependencies, check the following 
subsection.
- conf/: Contains a template to store the api-key and other credentials. To store your credentials, create a personal
config.ini file and append your credentials. Remember to add the file to the .gitignore such that the credentials will
not be pushed to the remote repository.
- data/:
  - ./stocks/: Contains stock data files.
  - ./tiktok/: Contains tiktok data files.
  - ./twitter/: Contains twitter data files. 
- scripts/: Contains finished and working scripts that are used to scrape data from different endpoints. 
- test/: Contains scripts that are used for testing and are not necessarily used productively.
- utils/: Contains files and scripts, files, and other resources that potentially extend the functionalities of scripts 

## Setting up environment
Installing Conda: https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html
```bash
# Create an environment from environment_win.yml
conda env create -f conda/environment_win.yml

# (De)activate the environment (coin)
conda activate coin
conda deactivate coin

# When installing new packages, updating environment with
conda env update -f conda/environment_win.yml --prune

# Exporting actual environment_win.yml (e.g., after installing new packages)
conda env export > conda/environment_win.yml
```
