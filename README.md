# COIN Project Repository

## Setting up environment
Installing Conda: https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html
 
```bash
# Create an environment from environment.yml
conda env create -f conda/environment.yml

# (De)activate the environment (coin)
conda activate coin
conda deactivate coin

# When installing new packages, updating environment with
conda env update -f conda/environment.yml --prune

# Exporting actual environment.yml (e.g., after installing new packages)
conda env export > conda/environment.yml

```