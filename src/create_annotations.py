import os
from pathlib import Path
import zipfile
import requests


def download_file_from_google_drive(id: str, destination: Path) -> None:
    URL = "https://docs.google.com/uc?export=download"
    print(f'Downloading file {id} into {os.path.relpath(destination)}')
    with requests.Session() as session:
        response = session.get(URL, params={'id': id, 'confirm': 't'}, stream=True)
    save_response_content(response, destination)
    unzip_content(destination)


def download_annotations(destination: Path) -> None:
    print('Downloading annotations')
    url = 'http://shuoyang1213.me/WIDERFACE/support/bbx_annotation/wider_face_split.zip'
    response = requests.get(url, stream=True)
    save_response_content(response, destination)
    unzip_content(destination)


def save_response_content(response: requests.Response, destination: Path) -> None:
    CHUNK_SIZE = 32768

    current_size = 0
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.with_name(destination.name + '.zip').open("wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                print(f'\r{current_size=}', end=' ')
                current_size += CHUNK_SIZE
    print('\nDone saving content')


def unzip_content(destination: Path) -> None:
    print('Unzipping')
    try:
        with zipfile.ZipFile(destination.with_name(destination.name + '.zip'), 'r') as zip:
            zip.extractall(destination.parent)
        print('Done unzipping')
        destination.with_name(destination.name + '.zip').unlink()
    except zipfile.BadZipFile:
        print('Ignoring unzip')


def save_annotations(destination: Path) -> None:
    for dataset_type in ['train', 'val']:
        with (destination / f'wider_face_split/wider_face_{dataset_type}_bbx_gt.txt').open('r') as predictions_file:
            while True:
                filename = predictions_file.readline().strip()
                if not filename: break

                number_bbox = int(predictions_file.readline())
                predictions = [predictions_file.readline() for _ in range(number_bbox)]
                if not number_bbox:
                    predictions_file.readline()
                annotation_path = destination / f'WIDER_{dataset_type}/annotations/{filename.rsplit(".", 1)[0]}'
                annotation_path.parent.mkdir(parents=True, exist_ok=True)
                with annotation_path.open('w') as annotation_file:
                    annotation_file.writelines(predictions)
                print(f'finished file {filename}')


def main():
    DATASET_PATH = Path(os.path.join(os.path.dirname(__file__), '..', 'dataset')).resolve()
    for file_id, filename in [('15hGDLhsx8bLgLcIRD5DhYt5iBxnjNF1M', 'WIDER_train'), 
                              ('1GUCogbp16PMGa39thoMMeWxp7Rp5oM8Q', 'WIDER_val')]:
        download_file_from_google_drive(file_id, DATASET_PATH / filename)
    download_annotations(DATASET_PATH / 'wider_face_split')
    save_annotations(DATASET_PATH)


if __name__ == '__main__':
    main()
