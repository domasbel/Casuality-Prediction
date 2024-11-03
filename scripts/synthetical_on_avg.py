import pandas as pd
import numpy as np
import random
import argparse

# Adjust as needed
num_records = 1000  
save_folder = 'data/synthetic/synthetic_patients.csv'

def generate_synthetic_patients(num_records):

    sex_options = ['Male', 'Female']

    diagnosis_options = ['Coma', 'Aphasia', 'Dysphagia', 'Seizure', 'Headache', 'Stroke', 'Migraine',
                         'Insultus ischaemicus cerebellum sin', 'Ataxia', 'Hemiplegia',
                         'Reinsultus ischaemicus cerebri in b. ACM sin', 'transformatio haemorrhagica']

    data = {
        'age': [],
        'CRB': [],
        'creatinine': [],
        'hematocrit': [],
        'sex': [],
        'diagnosis': []
    }

    for _ in range(num_records):
        # Generate Age
        age = int(np.random.normal(loc=50, scale=18))  #using normal distribution we generate the age for a person with mean=50, and std=18
        age = max(0, min(age, 100))  

        # Generate Sex
        sex = random.choice(sex_options)

        # Generate CRB Score
        crb = random.randint(0, 3)

        # Generate Creatinine based on sex
        if sex == 'Male':
            creatinine = round(np.random.uniform(0.74, 1.35), 2)
        else:
            creatinine = round(np.random.uniform(0.59, 1.04), 2)

        # Generate Hematocrit based on sex
        if sex == 'Male':
            hematocrit = round(np.random.uniform(38.3, 48.6), 1)
        else:
            hematocrit = round(np.random.uniform(35.5, 44.9), 1)

        # Generate Diagnosis
        num_diagnoses = random.randint(1, 3)  # Each patient can have 1 to 3 diagnoses
        patient_diagnoses = random.sample(diagnosis_options, num_diagnoses)
        diagnosis = '; '.join(patient_diagnoses)

        # Append data
        data['age'].append(age)
        data['CRB'].append(crb)
        data['creatinine'].append(creatinine)
        data['hematocrit'].append(hematocrit)
        data['sex'].append(sex)
        data['diagnosis'].append(diagnosis)

    # Create DataFrame
    df = pd.DataFrame(data)
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate synthetic patient data.')
    parser.add_argument('--num-records', type=int, default=1000, help='Number of records to generate.')
    parser.add_argument('--output-file', type=str, default='synthetic_patients.csv', help='Output CSV file name.')
    args = parser.parse_args()

    num_records = args.num_records
    save_folder = args.output_file

    df_patients = generate_synthetic_patients(num_records)
    df_patients.to_csv(save_folder, index=False)
    print(f'Synthetic patient data generated and saved to {save_folder}')
