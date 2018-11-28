import unittest
from nose_parameterized import parameterized

import os
import shutil

import cbsodata

datasets = [
    '82010NED',
    '80884ENG'
]

datasets_derden = [
    '47015NED',
    '47003NED'
]

TEST_ENV = 'test_env'


class TestCBSOData(unittest.TestCase):

    @classmethod
    def setupClass(self):

        if not os.path.exists(TEST_ENV):
            os.makedirs(TEST_ENV)

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(TEST_ENV)

    @parameterized.expand(datasets)
    def test_info(self, table_id):

        # testing
        info = cbsodata.get_info(table_id)

        self.assertIsInstance(info, dict)

    @parameterized.expand(datasets)
    def test_download(self, table_id):

        cbsodata.download_data(table_id)

    @parameterized.expand(datasets)
    def test_http_https_download(self, table_id):

        cbsodata.options['use_https'] = True
        cbsodata.download_data(table_id)
        cbsodata.options['use_https'] = False
        cbsodata.download_data(table_id)
        cbsodata.options['use_https'] = True

    @parameterized.expand(datasets)
    def test_download_and_store(self, table_id):

        cbsodata.download_data(
            table_id,
            dir=os.path.join(TEST_ENV, table_id)
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(TEST_ENV, table_id, 'TableInfos.json')
            )
        )

    @parameterized.expand(datasets)
    def test_get_data(self, table_id):

        cbsodata.get_data(table_id)

    @parameterized.expand(datasets)
    def test_info_values(self, table_id):

        info = cbsodata.get_info(table_id)

        # Check response is dict (not a list)
        self.assertIsInstance(info, dict)

        # Check required keys are available
        self.assertTrue('Description' in info.keys())
        self.assertTrue('ID' in info.keys())
        self.assertTrue('Identifier' in info.keys())

    def test_table_list(self):

        self.assertGreaterEqual(len(cbsodata.get_table_list()), 100)

    def test_filters(self):

        default_sel_filt = cbsodata.get_info('82070ENG')['DefaultSelection']
        filters_and_selections = default_sel_filt.split("&")

        for fs in filters_and_selections:
            if fs.startswith('$filter='):
                filt = fs[8:]

        cbsodata.get_data('82070ENG', filters=filt)

    def test_select(self):

        default_sel_filt = cbsodata.get_info('82070ENG')['DefaultSelection']
        filters_and_selections = default_sel_filt.split("&")

        for fs in filters_and_selections:
            if fs.startswith('$select='):
                select = fs[8:]

        cbsodata.get_data('82070ENG', select=select)

    def test_select_list(self):

        default_sel_filt = cbsodata.get_info('82070ENG')['DefaultSelection']
        filters_and_selections = default_sel_filt.split("&")

        for fs in filters_and_selections:
            if fs.startswith('$select='):
                select = fs[8:]

        cbsodata.get_data('82070ENG', select=select.split(', '))

    def test_select_subset(self):

        default_sel_filt = cbsodata.get_info('82070ENG')['DefaultSelection']
        filters_and_selections = default_sel_filt.split("&")

        for fs in filters_and_selections:
            if fs.startswith('$select='):
                select = fs[8:]

        select_list = select.split(', ')
        cbsodata.get_data('82070ENG', select=select_list[0:2])

    def test_select_n_cols(self):

        default_sel_filt = cbsodata.get_info('82070ENG')['DefaultSelection']
        filters_and_selections = default_sel_filt.split("&")

        for fs in filters_and_selections:
            if fs.startswith('$select='):
                select = fs[8:]

        select_list = select.split(', ')
        data = cbsodata.get_data('82070ENG', select=select_list[0:2])

        self.assertEqual(len(data[0].keys()), 2)
        self.assertEqual(len(data[5].keys()), 2)
        self.assertEqual(len(data[10].keys()), 2)

    @parameterized.expand(datasets_derden)
    def test_get_table_list_derden(self, table_id):

        # option 1
        cbsodata.options.catalog_url = 'dataderden.cbs.nl'
        data_option1 = cbsodata.get_table_list()
        cbsodata.options.catalog_url = 'opendata.cbs.nl'

        # option 2
        with cbsodata.catalog('dataderden.cbs.nl'):
            data_option2 = cbsodata.get_table_list()

        # option 3
        data_option3 = cbsodata.get_table_list(
            catalog_url='dataderden.cbs.nl'
        )

        assert data_option1[0].keys() > 0

        for key in data_option1[0].keys():

            assert data_option1[0][key] == \
                data_option2[0][key] == data_option3[0][key]

    @parameterized.expand(datasets)
    def test_get_data_derden(self, table_id):

        # option 1
        cbsodata.options.catalog_url = 'dataderden.cbs.nl'
        data_option1 = cbsodata.get_data(table_id)
        cbsodata.options.catalog_url = 'opendata.cbs.nl'

        # option 2
        with cbsodata.catalog('dataderden.cbs.nl'):
            data_option2 = cbsodata.get_data(table_id)

        # option 3
        data_option3 = cbsodata.get_data(
            table_id,
            catalog_url='dataderden.cbs.nl'
        )

        assert data_option1[0].keys() > 0

        for key in data_option1[0].keys():

            assert data_option1[0][key] == \
                data_option2[0][key] == data_option3[0][key]
