import argparse
import os
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

mlb = MultiLabelBinarizer()

column_name = 'diagnoses'
output_folder = 'data/processed_data'

def one_hot_encoding(file_name, input_folder = 'data/raw', column_name='diagnoses', delimiter=','):
    """
    Perform one-hot encoding on the specified column of the given CSV file.

    Parameters:
    - file_name (str): Name of the input CSV file.
    - input_folder (str): Directory where the input file is located.
    - column_name (str): Name of the column to be one-hot encoded.
    - delimiter (str): Delimiter used to separate multiple entries in the column.

    Returns:
    - None
    """
    input_path = os.path.join(input_folder, file_name)
    output_file_name = f"encoded_{file_name}"
    output_path = os.path.join(output_folder, output_file_name)
    os.makedirs(output_folder, exist_ok=True)

    try:
        df = pd.read_csv(input_path)

        if column_name not in df.columns:
            print(f"Error: Column '{column_name}' not found in the input file.")
            return


        df['diagnosis_list'] = df[column_name].astype(str).str.split(delimiter)
        
        # Handle missing values by filling with empty list
        df['diagnosis_list'] = df['diagnosis_list'].apply(lambda x: x if isinstance(x, list) else [])

        # Perform one-hot encoding
        diagnosis_encoded = mlb.fit_transform(df['diagnosis_list'])

        # Create a DataFrame with the one-hot encoded columns
        diagnosis_df = pd.DataFrame(diagnosis_encoded, columns=mlb.classes_, index=df.index)

        # Concatenate the one-hot encoded columns with the original DataFrame
        df_final = pd.concat([df.drop(['diagnosis_list', column_name], axis=1), diagnosis_df], axis=1)
        df_final.to_csv(output_path, index=False)

        print(f"One-hot encoding completed successfully.\nEncoded file saved to '{output_path}'.")

    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{input_path}' is empty.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':  
    parser = argparse.ArgumentParser(description='Execute one-hot encoding on the specified CSV file.')
    parser.add_argument('--file-name', type=str, required=True, help='Name of the input CSV file.')
    parser.add_argument('--input-folder', type=str, default='data/raw', help='Directory where the input file is located.')
    parser.add_argument('--column-name', type=str, default='diagnoses', help='Name of the column to be one-hot encoded.')
    parser.add_argument('--delimiter', type=str, default=',', help='Delimiter used to separate multiple entries in the column.')
    args = parser.parse_args()

    one_hot_encoding(
        file_name=args.file_name,
        input_folder=args.input_folder,
        column_name=args.column_name,
        delimiter=args.delimiter
    )
