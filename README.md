# Macro variables for the 9th Outlook
Uses git repository template for APERC models. This repository holds many of the input assumptions/data that will be used for the forthcoming 9th APEC Energy Demand and Supply Outlook.

## GDP projections out to 2100
One of the main components of this repository is GDP projections for APEC economies.

The starting point is IMF GDP projections for APEC economies out to 2027. This is then built on out to 2100.

The model used is a Solow Swan constant elasticity of substitution Cobb Douglas production model, with labour and capital inputs, and derived efficiency of labour. 

Inputs to the model include:

- Population estimates to 2100 (provided by UN DESA)
- Capital stock (Penn World Tables)
- Depreciation (Penn World Tables)
- National savings rate (IMF)
- Labour efficiency (derived for historical years or where data is available)

Capital stock, depreciation, national savings, and labour efficiency are assumed to change through the projection period, based on qualitative assessment.

#### Scripts to generate results (in workflow >> scripts >> macro)

##### Data grab and visualisation 
- a1_UN_DESA_population_data.py: Grabs UN DESA population data, visualises population trajectories out to 2100, and saves data in required format for use later.
- a2_IMF_data_grab.py: Grabs relevant IMF data as input for the model.
- a3_PWT_data_grab.py: Grabs Penn World Tables data and visualises relevant data.
- a4_combined_mini_projection.py: Uses Swan Solow model to derive labour efficiency for historical/available data. Packages all relevant data: Available GDP (to 2027 from IMF), capital (k stock from PWT), labour (UN DESA choice to 2100), labour efficiency.

##### GDP projections
- b1_GDP_model_APERC.py

Builds a function that allows choice of how labour efficiency, savings, and depreciation evolves through time (these values are not static and have large implications for long-term GDP projections). The function then generates GDP estimates and plots these estimates alongside older GDP projections (from the 8th Outlook, published in 2022).

- b2_generate_GDP_results.py

Executes function built in the previous script for all 21 economies, with ability to make choices about how the inputs change through time, and visualises the results.

- b3_GDP_population_sensitivity.py

Executes the functions with the same selections in 2b, but with a population sensitivity of Low, Medium and High (UN DESA has more than 10 different population scenarios, but High, Medium, and Low are chosen as representative of most of the range).

- z_GDP_model_Pugh.py: A different approach from David Pugh for reference

## Project organization

Project organization is based on ideas from [_Good Enough Practices for Scientific Computing_](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510) and the [_SnakeMake_](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html) recommended workflow. 

1. Put each project in its own directory, which is named after the project.
2. Put data in the `data` directory. This can be input data or data files created by scripts and notebooks in this project.
3. Put configuration files in the `config` directory.
4. Put text documents associated with the project in the `docs` directory.
5. Put all scripts in the `workflow/scripts` directory.
6. Install the Conda environment into the `workflow/envs` directory. 
7. Put all notebooks in the `workflow/notebooks` directory.
8. Put final results in the `results` directory.
9. Name all files to reflect their content or function.

Note: input data for the models is not pushed to git. They are available from public sources (or from internal directories (Teams)) that you will need to save in the relevant location in the data folder on your cloned repository.

## Using Conda

### Creating the Conda environment

After adding any necessary dependencies to the Conda `environment.yml` file you can create the 
environment in a sub-directory of your project directory by running the following command.

```bash
$ conda env create --prefix ./env --file ./workflow/envs/environment.yml
```
Once the new environment has been created you can activate the environment with the following 
command.

```bash
$ conda activate ./env
```

Note that the `env` directory is *not* under version control as it can always be re-created from 
the `environment.yml` file as necessary.

### Update from finn (uses a different env file)
You can also use the macro_variables_env environment that finn has created for his use. 

Change the environment folder and environment.yml file in the steps above from:  
```bash
./env and ./workflow/envs/environment.yml 
```

to:
```bash
./macro_variables_env and ./workflow/envs/macro_variables_env.yml
```

### Updating the Conda environment

If you add (remove) dependencies to (from) the `environment.yml` file after the environment has 
already been created, then you can update the environment with the following command.

```bash
$ conda env update --prefix ./env --file ./workflow/envs/environment.yml --prune
```

### Listing the full contents of the Conda environment

The list of explicit dependencies for the project are listed in the `environment.yml` file. To see the full list of packages installed into the environment run the following command.

```bash
conda list --prefix ./env
```

