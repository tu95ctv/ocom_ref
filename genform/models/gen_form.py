# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import re
from odoo.tools import lazy_property

magic_fields = ['create_uid','create_date','write_uid','write_date','__last_update','display_name']
class Genform(models.Model):
    _name = 'gen.form'
    _description = 'Test model'

    search_box = fields.Char()
    search_model_list_box_paste = fields.Text()
    search_model_list_box = fields.Text(compute='_compute_search_model_list_box_paste')
    is_wrap_comment = fields.Boolean()

    is_tree = fields.Boolean(default=True)
    is_form = fields.Boolean(default=True)
    is_action = fields.Boolean(default=True)
    is_menu = fields.Boolean(default=True)
    view_mode = fields.Char()
    editable = fields.Char()

    @api.depends('search_model_list_box_paste')
    def _compute_search_model_list_box_paste(self):
        for r in self:
            if r.search_model_list_box_paste:
                search_model_list_box_paste = r.search_model_list_box_paste
                search_model_list_box_paste = search_model_list_box_paste.strip()
                search_model_list_box_paste = re.sub('\s+',',', search_model_list_box_paste)
                r.search_model_list_box = search_model_list_box_paste
            else:
                r.search_model_list_box = False



    is_exclude_magic_field = fields.Boolean(default=True)
    is_exclude_id_field = fields.Boolean(default=True)
    model_ids = fields.Many2many('ir.model')
    out_put = fields.Text()
    gen_model_field_ids = fields.One2many('gen.model.field', 'gen_form_id')
    


    def a_xml_field(self, field):
        return '<field name="%s" />'%field.name

    def multi_xml_field(self, gen_field_ids):
        rs = [self.a_xml_field(i.field_id) for i in gen_field_ids]
        rs = '\n'.join(rs)
        return rs
        
    def gen_action_per_model(self, gen_model_field):
        model = gen_model_field.model_id
        model_name = model.model
        name = model_name
        name = re.sub('^crm\.','',name)
        name = name.replace('.',' ').title()
        id_act = model_name.replace('.','_') + '_' + 'act'
        view_mode = self.view_mode or 'tree,form'
        form_template = '''
        <record id="%(id)s" model="ir.actions.act_window">
            <field name="name">%(name)s</field>
            <field name="res_model">%(model_name)s</field>
            <field name="view_mode">%(view_mode)s</field>
        </record>
        '''
        rs = form_template%{'id':id_act, 'name':name, 'model_name':model_name, 'view_mode':view_mode}
        if self.is_menu:
            id_menu = model_name.replace('.','_') + '_' + 'menu'
            menu_template = \
            '''<menuitem id="%(id)s"
                name="%(name)s"
                sequence="200"
                parent="crm_application_settings"
                groups="sales_team.group_sale_manager"
                action="%(id_act)s"/>'''
            act_rs = menu_template%{'id':id_menu, 'name':name, 'id_act':id_act}
            rs = rs +'\n\n' +act_rs
        return rs

    # def gen_menu_per_model(self, gen_model_field):
    #     model = gen_model_field.model_id
    #     model_name = model.model
    #     name = model_name
    #     name = re.sub('^crm\.','',name)
    #     name = name.replace('.',' ').title()
    #     id = model_name.replace('.','_') + '_' + 'act'
    #     view_mode = self.view_mode or 'tree,form'
    #     form_template = '''
    #     <record id="%(id)s" model="ir.actions.act_window">
    #         <field name="name">%(name)s</field>
    #         <field name="res_model">%(model_name)s</field>
    #         <field name="view_mode">%(view_mode)s</field>
    #     </record>
    #     '''

    #     form_template = '''
    #     <record id="%(id)s" model="ir.actions.act_window">
    #         <field name="name">%(name)s</field>
    #         <field name="res_model">%(model_name)s</field>
    #         <field name="view_mode">%(view_mode)s</field>
    #     </record>
    #     '''


    #     rs = form_template%{'id':id, 'name':name, 'model_name':model_name, 'view_mode':view_mode}
    #     return rs


    def gen_tree_per_model(self, gen_model_field):
        return self.gen_form_per_model( gen_model_field, 'tree')

    def gen_form_per_model(self, gen_model_field,type='form'):
        model = gen_model_field.model_id
        model_name = model.model
        name = model_name
        id = model_name.replace('.','_') + '_' + type
        gen_field_ids = gen_model_field.gen_field_ids
        gen_field_ids = gen_field_ids.sorted(lambda i: i.field_id.ttype)
        xml_fields = self.multi_xml_field(gen_field_ids)
        editable = 'editable="%s"'%self.editable if type=='tree' and self.editable else ''
        tree_or_form_template = \
        '''<%(type)s %(editable)s>
                    %%(xml_fields)s
                </%(type)s>'''%{'type':type, 'editable':editable}

        tree_or_form_data = tree_or_form_template%{'xml_fields': xml_fields}
        form_template = '''
        <record id="%(id)s" model="ir.ui.view">
            <field name="name">%(name)s</field>
            <field name="model">%(model_name)s</field>
            <field name="arch" type="xml">
                %(tree_or_form_data)s
            </field>
        </record>
        '''
        print ('tree_or_form_data', tree_or_form_data)
        rs = form_template%{'id':id, 'name':name, 'model_name':model_name, 'tree_or_form_data':tree_or_form_data}
        return rs
        


    def gen_form_tree(self, gen_model_field):
        rs = [
            self.gen_form_per_model(gen_model_field) if self.is_form else None,
            self.gen_tree_per_model(gen_model_field)if self.is_tree else None,
            self.gen_action_per_model(gen_model_field)if self.is_action else None
             ]
        rs = [i for i in rs if i]
        out_put = '\n'.join(rs)
        is_wrap_comment = self.is_wrap_comment
        # model_name = gen_model_field.model_id.name
        # model_name = model_name.replace('.',' ').title()
        model_name = gen_model_field.model_name()
        if is_wrap_comment:
            out_put = '<!--%(model_name)s-->\n%(form_tree_out_put)s\n<!--!%(model_name)s-->'\
                %{'form_tree_out_put':out_put, 'model_name': model_name}
        return out_put

    def gen_form_trees(self):
        gen_model_field_ids = self.gen_model_field_ids
        out_puts = [self.gen_form_tree(gen_model_field) for gen_model_field in gen_model_field_ids]
        out_put = '\n\n'.join(out_puts)
        
        return out_put

    def gen_form(self):
        self.out_put = self.gen_form_trees()

    def button_get_all_field_of_model(self):
        for i in self.gen_model_field_ids:
            model = i.model_id
            fields = model.field_id
            exist = i.gen_field_ids.mapped('field_id.name')
            exclude_fields = magic_fields if self.is_exclude_magic_field else []
            if self.is_exclude_id_field:
                exclude_fields.append('id')
            exclude_fields += exist
            adds = [(0,0,{'field_id':field_id.id}) for field_id in fields if field_id.name not in exclude_fields]
            i.gen_field_ids = adds

    def button_clear_model_field(self):
        self.gen_model_field_ids = False


    def button_clear_gen_field_ids(self):
        for i in self.gen_model_field_ids:
            i.gen_field_ids = False

    def add_model_from_search_box(self):
        
        limit = 20
        domain = []
        search_model_list_boxs = []
        def sorted_index(model):
            if model.model in search_model_list_boxs:
                return search_model_list_boxs.index(model.model)
            else:
                return 1000

        if self.search_box:
            domain +=[('model','ilike',self.search_box)]
        if self.search_model_list_box_paste:
            search_model_list_boxs = self.search_model_list_box.split(',')
            domain +=[('model','in', search_model_list_boxs)]
        print ('domain', domain)
        if domain:
            model_ids = self.env['ir.model'].search(domain)
            if search_model_list_boxs:
                model_ids = model_ids.sorted(sorted_index)
            exist_model = self.gen_model_field_ids.mapped('model_id')
            adds = [(0,0,{'model_id':model_id.id}) for model_id in model_ids if model_ids not in exist_model]
            self.gen_model_field_ids = adds


class GenModelField(models.Model):

    _name = 'gen.model.field'

    gen_form_id = fields.Many2one('gen.form')
    model_id = fields.Many2one('ir.model')
    gen_field_ids = fields.One2many('gen.field','gen_model_field_id')

    # @lazy_property
    def model_name(self):
        model_name = self.model_id.name
        model_name = model_name.replace('.',' ').title()
        return model_name


class GenField(models.Model):

    _name = 'gen.field'
    
    name = fields.Char(related='field_id.name', store=True)
    gen_model_field_id = fields.Many2one('gen.model.field')
    field_id = fields.Many2one('ir.model.fields')
    group = fields.Integer()







    

    
    