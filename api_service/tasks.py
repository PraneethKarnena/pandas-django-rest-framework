from __future__ import absolute_import, unicode_literals
import uuid
import json

import pandas as pd
from pandas import ExcelWriter
from celery import shared_task

from api_service import models


def get_dataset(dataset_id):
    dataset = models.DatasetModel.objects.get(id=dataset_id)
    return dataset

@shared_task
def process_dataset(dataset_id):
    save_dataframe(dataset_id)


def save_dataframe(dataset_id):
    dataset = get_dataset(dataset_id)
    data = pd.read_csv(f'{dataset.file.name}')
    df = pd.DataFrame(data)

    name = f'{str(uuid.uuid4())}.feather'
    df.to_feather(name)

    # Save dataframe details
    dataset.dataframe_file_name = name
    dataset.dataframe_creation_status = 'CRT'
    dataset.dataframe_url = f'/media/{name}'
    dataset.save()

    # Process further
    export_excel(dataset_id)
    export_json(dataset_id)
    export_histogram_pdf(dataset_id)


def export_excel(dataset_id):
    dataset = get_dataset(dataset_id)
    data = pd.read_feather(dataset.dataframe_file_name)
    df = pd.DataFrame(data)

    name = f'{str(uuid.uuid4())}.xlsx'

    with ExcelWriter(name) as writer:
        df.to_excel(writer)

    # Save excel details
    dataset.excel_file_name = name
    dataset.excel_creation_status = 'CRT'
    dataset.excel_url = f'/media/{name}'
    dataset.save()


def export_json(dataset_id):
    dataset = get_dataset(dataset_id)
    data = pd.read_feather(dataset.dataframe_file_name)
    df = pd.DataFrame(data)

    json_data = df.describe().to_json()

    # Save json details
    dataset.stats = json_data
    dataset.stats_creation_status = 'CRT'
    dataset.save()


def export_histogram_pdf(dataset_id):
    dataset = get_dataset(dataset_id)
    data = pd.read_feather(dataset.dataframe_file_name)
    df = pd.DataFrame(data)
    ax = df.plot.hist()
    figure = ax.get_figure()

    name = f'{str(uuid.uuid4())}.pdf'
    figure.savefig(name)

    # Save PDF details
    dataset.pdf_file_name = name
    dataset.pdf_creation_status = 'CRT'
    dataset.pdf_url = f'/media/{name}'
    dataset.save()