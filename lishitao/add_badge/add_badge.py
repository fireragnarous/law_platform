# Copyright Contributors to the Amundsen project.
# SPDX-License-Identifier: Apache-2.0

"""
This is a example script demonstrating how to load data into Neo4j and
Elasticsearch without using an Airflow DAG.

It contains several jobs:
- `run_csv_job`: runs a job that extracts table data from a CSV, loads (writes)
  this into a different local directory as a csv, then publishes this data to
  neo4j.
- `run_table_column_job`: does the same thing as `run_csv_job`, but with a csv
  containing column data.
- `create_last_updated_job`: creates a job that gets the current time, dumps it
  into a predefined model schema, and publishes this to neo4j.
- `create_es_publisher_sample_job`: creates a job that extracts data from neo4j
  and pubishes it into elasticsearch.

For other available extractors, please take a look at
https://github.com/amundsen-io/amundsendatabuilder#list-of-extractors
"""

import logging
import os
import sys
import uuid

from amundsen_common.models.index_map import DASHBOARD_ELASTICSEARCH_INDEX_MAPPING, USER_INDEX_MAP
from elasticsearch import Elasticsearch
from pyhocon import ConfigFactory
from sqlalchemy.ext.declarative import declarative_base
from databuilder.extractor.neo4j_extractor import Neo4jExtractor
from databuilder.extractor.csv_extractor import (
    CsvColumnLineageExtractor, CsvExtractor, CsvTableBadgeExtractor, CsvTableColumnExtractor, CsvTableLineageExtractor,
)
from databuilder.extractor.es_last_updated_extractor import EsLastUpdatedExtractor
from databuilder.extractor.neo4j_search_data_extractor import Neo4jSearchDataExtractor
from databuilder.job.job import DefaultJob
from databuilder.loader.file_system_elasticsearch_json_loader import FSElasticsearchJSONLoader
from databuilder.loader.file_system_neo4j_csv_loader import FsNeo4jCSVLoader
from databuilder.publisher.elasticsearch_publisher import ElasticsearchPublisher
from databuilder.publisher.neo4j_csv_publisher import Neo4jCsvPublisher
from databuilder.task.task import DefaultTask
from databuilder.transformer.base_transformer import ChainedTransformer, NoopTransformer
from databuilder.transformer.dict_to_model import MODEL_CLASS, DictToModel
from databuilder.transformer.generic_transformer import (
    CALLBACK_FUNCTION, FIELD_NAME, GenericTransformer,
)

es_host = os.getenv('CREDENTIALS_ELASTICSEARCH_PROXY_HOST', 'localhost')
neo_host = os.getenv('CREDENTIALS_NEO4J_PROXY_HOST', 'localhost')

es_port = os.getenv('CREDENTIALS_ELASTICSEARCH_PROXY_PORT', 9200)
neo_port = os.getenv('CREDENTIALS_NEO4J_PROXY_PORT', 7687)
if len(sys.argv) > 1:
    es_host = sys.argv[1]
if len(sys.argv) > 2:
    neo_host = sys.argv[2]

es = Elasticsearch([
    {'host': es_host, 'port': es_port},
])

Base = declarative_base()

NEO4J_ENDPOINT = f'bolt://{neo_host}:{neo_port}'

neo4j_endpoint = NEO4J_ENDPOINT

neo4j_user = 'neo4j'
neo4j_password = 'test'

LOGGER = logging.getLogger(__name__)


def run_table_column_job(table_path, column_path):
    tmp_folder = '/var/tmp/amundsen/table_column'
    node_files_folder = f'{tmp_folder}/nodes'
    relationship_files_folder = f'{tmp_folder}/relationships'
    extractor = CsvTableColumnExtractor()
    csv_loader = FsNeo4jCSVLoader()
    task = DefaultTask(extractor,
                       loader=csv_loader,
                       transformer=NoopTransformer())
    job_config = ConfigFactory.from_dict({
        'extractor.csvtablecolumn.table_file_location': table_path,
        'extractor.csvtablecolumn.column_file_location': column_path,
        'loader.filesystem_csv_neo4j.node_dir_path': node_files_folder,
        'loader.filesystem_csv_neo4j.relationship_dir_path': relationship_files_folder,
        'loader.filesystem_csv_neo4j.delete_created_directories': True,
        'publisher.neo4j.node_files_directory': node_files_folder,
        'publisher.neo4j.relation_files_directory': relationship_files_folder,
        'publisher.neo4j.neo4j_endpoint': neo4j_endpoint,
        'publisher.neo4j.neo4j_user': neo4j_user,
        'publisher.neo4j.neo4j_password': neo4j_password,
        'publisher.neo4j.neo4j_encrypted': False,
        'publisher.neo4j.job_publish_tag': 'unique_tag',  # should use unique tag here like {ds}
    })
    job = DefaultJob(conf=job_config,
                     task=task,
                     publisher=Neo4jCsvPublisher())
    job.launch()


def run_table_badge_job(table_path, badge_path):
    tmp_folder = '/var/tmp/amundsen/table_badge'
    node_files_folder = f'{tmp_folder}/nodes'
    relationship_files_folder = f'{tmp_folder}/relationships'
    extractor = CsvTableBadgeExtractor()
    csv_loader = FsNeo4jCSVLoader()
    task = DefaultTask(extractor=extractor,
                       loader=csv_loader,
                       transformer=NoopTransformer())
    job_config = ConfigFactory.from_dict({
        'extractor.csvtablebadge.table_file_location': table_path,
        'extractor.csvtablebadge.badge_file_location': badge_path,
        'loader.filesystem_csv_neo4j.node_dir_path': node_files_folder,
        'loader.filesystem_csv_neo4j.relationship_dir_path': relationship_files_folder,
        'loader.filesystem_csv_neo4j.delete_created_directories': True,
        'publisher.neo4j.node_files_directory': node_files_folder,
        'publisher.neo4j.relation_files_directory': relationship_files_folder,
        'publisher.neo4j.neo4j_endpoint': neo4j_endpoint,
        'publisher.neo4j.neo4j_user': neo4j_user,
        'publisher.neo4j.neo4j_password': neo4j_password,
        'publisher.neo4j.neo4j_encrypted': False,
        'publisher.neo4j.job_publish_tag': 'unique_tag_b',  # should use unique tag here like {ds}
    })
    job = DefaultJob(conf=job_config,
                     task=task,
                     publisher=Neo4jCsvPublisher())
    job.launch()


def create_es_publisher_sample_job(elasticsearch_index_alias='table_search_index',
                                   elasticsearch_doc_type_key='table',
                                   model_name='databuilder.models.table_elasticsearch_document.TableESDocument',
                                   cypher_query=None,
                                   elasticsearch_mapping=None):
    """
    :param elasticsearch_index_alias:  alias for Elasticsearch used in
                                       amundsensearchlibrary/search_service/config.py as an index
    :param elasticsearch_doc_type_key: name the ElasticSearch index is prepended with. Defaults to `table` resulting in
                                       `table_search_index`
    :param model_name:                 the Databuilder model class used in transporting between Extractor and Loader
    :param cypher_query:               Query handed to the `Neo4jSearchDataExtractor` class, if None is given (default)
                                       it uses the `Table` query baked into the Extractor
    :param elasticsearch_mapping:      Elasticsearch field mapping "DDL" handed to the `ElasticsearchPublisher` class,
                                       if None is given (default) it uses the `Table` query baked into the Publisher
    """
    # loader saves data to this location and publisher reads it from here
    extracted_search_data_path = '/var/tmp/amundsen/search_data.json'

    task = DefaultTask(loader=FSElasticsearchJSONLoader(),
                       extractor=Neo4jSearchDataExtractor(),
                       transformer=NoopTransformer())

    # elastic search client instance
    elasticsearch_client = es
    # unique name of new index in Elasticsearch
    elasticsearch_new_index_key = 'tables' + str(uuid.uuid4())

    job_config = ConfigFactory.from_dict({
        f'extractor.search_data.extractor.neo4j.{Neo4jExtractor.GRAPH_URL_CONFIG_KEY}': neo4j_endpoint,
        f'extractor.search_data.extractor.neo4j.{Neo4jExtractor.MODEL_CLASS_CONFIG_KEY}': model_name,
        f'extractor.search_data.extractor.neo4j.{Neo4jExtractor.NEO4J_AUTH_USER}': neo4j_user,
        f'extractor.search_data.extractor.neo4j.{Neo4jExtractor.NEO4J_AUTH_PW}': neo4j_password,
        f'loader.filesystem.elasticsearch.{FSElasticsearchJSONLoader.FILE_PATH_CONFIG_KEY}': extracted_search_data_path,
        f'loader.filesystem.elasticsearch.{FSElasticsearchJSONLoader.FILE_MODE_CONFIG_KEY}': 'w',
        f'publisher.elasticsearch.{ElasticsearchPublisher.FILE_PATH_CONFIG_KEY}': extracted_search_data_path,
        f'publisher.elasticsearch.{ElasticsearchPublisher.FILE_MODE_CONFIG_KEY}': 'r',
        f'publisher.elasticsearch.{ElasticsearchPublisher.ELASTICSEARCH_CLIENT_CONFIG_KEY}':
            elasticsearch_client,
        f'publisher.elasticsearch.{ElasticsearchPublisher.ELASTICSEARCH_NEW_INDEX_CONFIG_KEY}':
            elasticsearch_new_index_key,
        f'publisher.elasticsearch.{ElasticsearchPublisher.ELASTICSEARCH_DOC_TYPE_CONFIG_KEY}':
            elasticsearch_doc_type_key,
        f'publisher.elasticsearch.{ElasticsearchPublisher.ELASTICSEARCH_ALIAS_CONFIG_KEY}':
            elasticsearch_index_alias,
    })

    # only optionally add these keys, so need to dynamically `put` them
    if cypher_query:
        job_config.put(f'extractor.search_data.{Neo4jSearchDataExtractor.CYPHER_QUERY_CONFIG_KEY}',
                       cypher_query)
    if elasticsearch_mapping:
        job_config.put(f'publisher.elasticsearch.{ElasticsearchPublisher.ELASTICSEARCH_MAPPING_CONFIG_KEY}',
                       elasticsearch_mapping)

    job = DefaultJob(conf=job_config,
                     task=task,
                     publisher=ElasticsearchPublisher())
    return job

if __name__ == "__main__":
    # Uncomment next line to get INFO level logging
    # logging.basicConfig(level=logging.INFO)
    run_table_column_job('example/test/sample_table.csv', 'example/test/sample_col.csv')
    #run_table_badge_job('example/test/sample_table.csv', 'example/test/sample_badges.csv')
    job_es_table = create_es_publisher_sample_job(
        elasticsearch_index_alias='table_search_index',
        elasticsearch_doc_type_key='table',
        model_name='databuilder.models.table_elasticsearch_document.TableESDocument')
    job_es_table.launch()



