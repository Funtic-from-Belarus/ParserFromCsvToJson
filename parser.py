import os
import pandas as pd
import json
import argparse
import re


def format_audio_path(audio_file):
    return f"/data/local-files/?d=audio/{audio_file}.wav"


def create_json_data(df):
    data = []
    for _, row in df.iterrows():
        audio_path = format_audio_path(row['audiofile'])
        item = {
            "data": {
                "audio": audio_path
            },
            "predictions": [
                {
                    "result": [
                        {
                            "from_name": "transcription",
                            "to_name": "audio",
                            "type": "textarea",
                            "value": {
                                "text": row['transcript']
                            }
                        }
                    ]
                }
            ]
        }
        data.append(item)
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="input_file",
                        required=True)
    parser.add_argument("--out", dest="output_csv",
                        required=True)
    parser.add_argument("--to", dest="output_json",
                        required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input_file, sep='\t', header=None, names=['data'])

    data = df['data'].str.extract(r'(.*?)pri_(\d\d)(.*)', expand=True)
    data[0] = data[0].str.strip()
    data[1] = 'pri_' + data[1].str.strip()
    data[2] = data[2].str.strip()

    result = pd.DataFrame(
        {'audiofile': data[0] + data[1], 'transcript': data[2]})
    result = result[result['transcript'].notna()]

    result.to_csv(args.output_csv, index=False)

    json_data = create_json_data(result)

    with open(args.output_json, 'w') as f:
        json.dump(json_data, f, indent=4)
