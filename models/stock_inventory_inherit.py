# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    Autor: Brayhan Andres Jaramillo Castaño
#    Correo: brayhanjaramillo@hotmail.com
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

import logging
from odoo import api, fields, models, _
_logger = logging.getLogger(__name__)

import xlsxwriter
#from io import StringIO
from io import BytesIO
import base64

import time
from datetime import datetime, timedelta, date
import sys

from xlrd import open_workbook
import base64


import openpyxl
from openerp import models, fields, api, _
from tempfile import TemporaryFile

class StockInvetoryInherit(models.Model):
	
	_inherit = 'stock.inventory'

	filename = fields.Binary('Archivo')
	excel_file = fields.Binary(string='Excel File')

	def return_column_excel(self, data_excel):
		if data_excel:
			if data_excel[0]:
				return data_excel[0]

	def return_column_position(self, data_excel, name_colum):
		if data_excel:
			data_column = self.return_column_excel(data_excel)

			if data_column:
				for x in range(0, len(data_column)):
					if data_column[x] == name_colum:
						return x 
			return -1


	def return_product_by_barcode(self, data_excel, pos_barcode, pos_qty):
		data = []
		if data_excel:
			for x in range(1, len(data_excel)):
				product_barcode = data_excel[x][pos_barcode]
				product_qty = data_excel[x][pos_qty]
				vals = {
				'barcode' : product_barcode,
				'product_qty' : float(product_qty),
				'product_id': 0,
				}
				data.append(vals)
		return data

	def return_data_product(self, data):
		repeat_barcode = []
		new_data = []
		if data:
			model_product_product = self.env['product.product']
			for x in data:
				product = model_product_product.search([('barcode', '=', x['barcode'])])
				print(product)
				if len(product) == 1:
					print(product.name)
					x['product_id'] = product.id
				else:
					
					#productos que tienen el mismo barcode
					for repeat in product:
						repeat_barcode.append(repeat.id)
		print('productos repetidos')
		print(repeat_barcode)

		return data

	@api.multi
	def button_update_lines(self):
		workbook = open_workbook(file_contents = base64.decodestring(self.excel_file))
		sheet = workbook.sheets()[0]

		data_excel = []

		for s in workbook.sheets():
			values = []
			for row in range(s.nrows):
				col_value = []
				for col in range(s.ncols):
					value  = (s.cell(row,col).value)
					try:
						value = str(int(value))
					except: 
						pass
					col_value.append(value)
				values.append(col_value)

			data_excel = values

		return data_excel


	@api.multi
	def update_qty_line_ids(self):

		data_excel = self.button_update_lines()

		#print(self.return_column_position(data_excel, 'referencia'))
		#print(self.return_column_position(data_excel, 'qty'))

		barcode = self.return_column_position(data_excel, 'Inventarios/Producto')
		qty = self.return_column_position(data_excel, 'line_ids/product_qty')

		data = self.return_product_by_barcode(data_excel, barcode, qty)
		print(data)

		print(self.return_data_product(data))

		vals_product = self.return_data_product(data)

		if self.line_ids:
			for x in vals_product:
				for line in self.line_ids:
					if line.product_id.id == x['product_id']:
						line.product_qty = x['product_qty']

StockInvetoryInherit()