# -*- coding: utf-8 -*-

from odoo import api, fields, models
from . province import fetch_ghn, replacetrim_quan, get_ghn_item_by_name
from unidecode import unidecode
import json
def fetch_ghn_ward_data(ghn_district_id):
        headers = {'token': '81f253e7-e8da-11ea-84a7-3e05d9a3136e'}
        url = 'https://online-gateway.ghn.vn/shiip/public-api/master-data/ward?district_id'
        data = {"district_id": int(ghn_district_id)}#int(self.ghn_id)}
        r = fetch_ghn(url, headers, data)
        return r['data']


class District(models.Model):
    _inherit = 'res.country.district'
    _sql_constraints = [
        ('unique_ghn_code', 'unique (ghn_code)', 'unique_ghn_code'),
        ('unique_ghn_id', 'unique (ghn_id)', 'unique_ghn_id'),
    ]
    ghn_code = fields.Char()
    ghn_id = fields.Integer()
    char_json_wards_data = fields.Char()
    ward_ids = fields.One2many('res.country.ward','district_id')

    # @api.one
    # def get_ghn_ward_one_district(self):
    #     str_province_ghn_id = self.ghn_id
    #     ward_ghn_items = fetch_ghn_ward_data(str_province_ghn_id)
    #     self.char_json_wards_data = ward_ghn_items
    #     wards = self.env['res.country.ward'].search([('district_id','=',self.id)]) 
    #     for ward in wards:
    #         ghn_ward_item = get_ghn_item_by_name(ward, ward_ghn_items, item_name = 'WardName',
    #                 methods = [replacetrim_quan, unidecode])
    #         if ghn_ward_item:
    #             ward.ghn_code = ghn_ward_item['WardCode']
    #         else:
    #             print ('name ward not map**** ',  ward.name.upper())
    
    # @api.one
    def get_ghn_ward_one_district(self):
        ghn_district_id = self.ghn_id
        print ('***ghn_district_id***', ghn_district_id, self.name)
        ward_ghn_items = fetch_ghn_ward_data(ghn_district_id)
        self.char_json_wards_data = ward_ghn_items
        wards = self.env['res.country.ward'].search([('district_id','=',self.id)]) 
        for ward in wards:
            ward.get_ghn_ward_with_ghn_datas(ward_ghn_items)
            
                
    def get_ghn_ward_all_district(self):
        for district in self.search(['|', ('ghn_id','!=',False), ('ghn_id','!=',0)]):
            district.get_ghn_ward_one_district()

    def get_ghn_district(self):
        ghn_items = self.state_id.fetch_district_ghn_items_of_this_province()
        self.get_this_ghn_district(ghn_items)

    def get_this_ghn_district(self, ghn_items):
        district = self
        item = get_ghn_item_by_name(district, ghn_items, item_name = 'DistrictName')
        if item:
            district.ghn_id = item['DistrictID']
            district.ghn_code = item['Code']
        else:
            print ('name  not map**** ', district.name)

            

        