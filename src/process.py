import os
import sys
import uuid
import toml
import logging
import numpy as np
import pandas as pd
import rameau as rm
import shutil

from lexique import DATA, PARAMS 

#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def save_dataframes_as_csv(path, **dataframes)-> list:
    """
    Save many DataFrames in files using the name as file name 

    :param dataframes (list<DataFrame>) dataframes to save with structur name=value.
    :return list of filename saved.
    """
    saved = []
    for nom, df in dataframes.items():
        if df is None or df == "" or df == "None":
            continue
        data = pd.read_csv(df)
        data.to_csv(os.path.join(path, f"{nom}.csv"), index=False)
        saved.append(f"{nom}.csv")
    return saved

def save_toml_parameters(toml_data, filenames, path)->str:
    """
    If the toml file is available, save it and update the part with files names.
    :param toml (str) toml data
    :param filenames (list<str>) 
    :return name of the toml file
    """
    if toml_data == "" or toml_data is None:
        return None
    config = toml.load(toml_data)

    for file in filenames:
        config['files'][DATA[file.split(".")[0]]] = file
    with open(os.path.join(path, PARAMS), 'w') as f:
        toml.dump(config, f)
    return PARAMS

def script(run, param, arbros, debit,\
                   piezo, etp, pluie, temperature, neige, pre_surf, pre_sout,\
                    output_dir, output_param):
    # get root directory
    root = os.getcwd()
    # Create repository with random repository name 
    work_directory = str(uuid.uuid4())
    os.mkdir(work_directory)
    created_files = save_dataframes_as_csv(path= work_directory, debit=debit, piezo=piezo, etp=etp,
                        pluie=pluie, temperature=temperature, neige=neige,
                        prelevement_surface=pre_surf, prelevement_souterain = pre_sout,
                        arbros= arbros)
    save_toml_parameters(param, filenames=created_files, path=work_directory)

    try:
        os.chdir(work_directory)
    except IOError as ioe:
        #logging.error(ioe)
        sys.exit(-1)
    model = rm.Model.from_toml(PARAMS)
    # return to root directory
    os.chdir(root)
    try:
        if "optimization" in run:
            #logging.info("Execution optimisation")
            optimization = model.run_optimization()
            optimization.get_output("riverflow").to_csv(os.path.join(output_dir,"optimization_riverflow.csv"))
            optimization.get_output("watertable").to_csv(os.path.join(output_dir,"optimization_watertable.csv"))
            optimization.get_metrics(variable="riverflow").to_csv(os.path.join(output_dir,"optimization_metrics_riverflow.csv"))
            optimization.get_metrics(variable="watertable").to_csv(os.path.join(output_dir,"optimization_metrics_watertable.csv"))
            model.tree = optimization.tree
            model.to_toml(os.path.join(output_param))
             
        if "simulation" in run:
            #logging.info("Execution simulation")
            simulation = model.run_simulation()
            simulation.get_output("riverflow").to_csv(os.path.join(output_dir,"simulation_riverflow.csv"))
            simulation.get_output("watertable").to_csv(os.path.join(output_dir,"simulation_watertable.csv"))
            simulation.get_metrics(variable="riverflow").to_csv(os.path.join(output_dir,"simulation_metrics_riverflow.csv"))
            simulation.get_metrics(variable="watertable").to_csv(os.path.join(output_dir,"simulation_metrics_watertable.csv"))
        if "forecast" in run:
            #logging.info("Execution prévision")
            forecast = model.run_forecast()
            forecast.get_forecast_output(variable='riverflow').to_csv(os.path.join(output_dir,"forecast_riverflow.csv"))
            forecast.get_forecast_output(variable='watertable').to_csv(os.path.join(output_dir,"forecast_watertable.csv"))
            model.tree = forecast.tree
            model.to_toml(output_param)
    except:
        #logging.error("Erreur dans l'execution")
        sys.exit(-1)
    finally:
        #logging.info("Suprresion du répertoire")
        shutil.rmtree(work_directory)    

    #logging.info("Fin du programme.")
    sys.exit(0)
    

    


