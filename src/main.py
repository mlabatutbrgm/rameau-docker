import os
import sys
import logging
import json
import process

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARN)

def required_parameters(run, params, etp, pluie):
    """
    Before calling the process, the function verifies if all parameters requiered 
    are not empty or not null.
    """
    if run is None:
        logging.error("Missing variable RUN")
        sys.exit(-1)
    if not os.path.isfile(params):
        logging.error("Missing parameter file")
        sys.exit(-1)
    if not os.path.isfile(etp) or not os.path.isfile(pluie): 
        logging.error("Missing input data ETP or PLUIE")
        sys.exit(-1)

def luncher(inputs, outputs):
    run = inputs['run'] # string[]
    param = inputs['param_section']['param'] # string
    arbros = inputs['param_section']['arbros'] # string

     # data files
    etp = inputs['data_section']['etp'] # string
    pluie = inputs['data_section']['pluie'] # string
    required_parameters(run, param, etp, pluie)
    run = [s.lower() for s in run.split(',')]
    debit = inputs['data_section']['debit'] # string
    piezo = inputs['data_section']['piezo'] # string
    temperature = inputs['data_section']['temperature'] # string
    neige = inputs['data_section']['neige'] # string
    pre_surf = inputs['data_section']['pre_surf'] # string
    pre_sout = inputs['data_section']['pre_sout'] # string

    # path output
    working_dir = os.getcwd()
    output_dir = os.path.join(working_dir, outputs['outputs_dir'])
    os.makedirs(output_dir, exist_ok=True)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_param = os.path.join(working_dir, outputs['output']) # string
    process.script(run=run, param=param, arbros=arbros, 
                   debit=debit, piezo=piezo, etp=etp, pluie=pluie,
                   temperature=temperature, neige=neige, 
                   pre_surf=pre_surf, pre_sout=pre_sout,
                   output_dir=output_dir, output_param=output_param)

if __name__ == "__main__":
    with open('inputs.json', 'rb') as f:
        inputs = json.loads(f.read().decode("utf-8"))
    with open('outputs.json', 'rb') as f:
        outputs = json.loads(f.read().decode("utf-8"))
    luncher(inputs, outputs)
    print("=== END 🪽==")