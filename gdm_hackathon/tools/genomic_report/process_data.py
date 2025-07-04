# %%

from engine_features.patient.loading.mosaic.wes import load_wes

patient_ids = ['CH_B_030a', 'CH_B_033a', 'CH_B_037a', 'CH_B_041a', 'CH_B_046a', 'CH_B_059a', 'CH_B_062a', 'CH_B_064a', 'CH_B_068a', 'CH_B_069a', 'CH_B_073a', 'CH_B_074a', 'CH_B_075a', 'CH_B_079a', 'CH_B_087a']

# %%

# SNV_INDEL

df = load_wes("Bladder","CHUV",  gene_nomenclature="gene_name", data_type="snv_indel").loc[patient_ids]

for patient in df.index:
    
    
# %%
