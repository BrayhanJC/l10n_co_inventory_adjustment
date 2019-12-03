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

	filename = fields.Char('Nombre Archivo')
	document = fields.Binary(string = 'Descargar Excel')


	@api.multi
	def generate_excel(self):

		name_report = "Ajuste de Inventario - " + str(fields.Datetime.from_string(fields.Datetime.now()))

		Header_Text = name_report
		file_data = BytesIO()
		workbook = xlsxwriter.Workbook(file_data)
		worksheet = workbook.add_worksheet(name_report)
	
		header_format = workbook.add_format({'bold': 1,'align':'center','valign':'vcenter', 'border':1, 'fg_color':'#f9770c', 'font_size': 18 })
		format_tittle = workbook.add_format({'bold': 1,'align':'center', 'valign':'vcenter', 'border':1, 'fg_color':'#f9770c', 'font_size': 25 })
		letter_category = workbook.add_format({'bold': 1,'align':'center','valign':'vcenter', 'border':1, 'fg_color':'#F9CEA9', 'font_size': 16 })
		letter_pvt = workbook.add_format({'bold': 1,'align':'center','valign':'vcenter', 'border':1, 'fg_color':'#ffe8d8', 'font_size': 15 })
		letter_number_total = workbook.add_format({'bold': 1,'align':'right','valign':'vcenter', 'num_format': '$#,##0.00', 'border':1, 'fg_color':'#F9CEA9', 'font_size': 16 })
		
		letter_left = workbook.add_format({'align':'left', 'font_color': 'black', 'font_size': 14})
		letter_number = workbook.add_format({'align':'right', 'font_color': 'black', 'num_format': '$#,##0.00', 'font_size': 14})
		bold = workbook.add_format({'bold': 1,'align':'left','border':1, 'font_size': 14})


		worksheet.set_column('A1:A1',35)
		worksheet.set_column('B1:B1',35)
		worksheet.set_column('C1:C1',35)
		worksheet.set_column('D1:C1',35)
		worksheet.set_column('E1:E1',35)
		worksheet.set_column('F1:F1',35)
		worksheet.set_column('G1:G1',55)
		worksheet.set_column('H1:H1',35)
		worksheet.set_column('I1:I1',35)
		worksheet.set_column('J1:J1',35)
		worksheet.set_column('K1:K1',35)
		worksheet.set_column('L1:L1',35)
		worksheet.set_column('M1:J1',35)
		worksheet.set_column('N1:K1',35)
		worksheet.set_column('O1:J1',35)
		worksheet.set_column('P1:K1',35)	

		preview = name_report 

		for i in range(1):
			
			if len(self.line_ids) > 0:

				worksheet.write('A1', 'Producto', header_format)
				worksheet.write('B1', 'Unidad de Medida', header_format)
				worksheet.write('C1', 'Ubicación', header_format)
				worksheet.write('D1', 'Lote/Nº de Serie', header_format)
				worksheet.write('E1', 'Paquete', header_format)
				worksheet.write('F1', 'Propietario', header_format)
				worksheet.write('G1', 'Cantidad Teorica', header_format)
				worksheet.write('H1', 'Cantidad Real', header_format)
				worksheet.write('I1', 'Diferencia', header_format)

				row=1
				col=0

				for value in self.line_ids:

					worksheet.write(row,col , str(value.product_id.name), letter_left)
					worksheet.write(row,col+1 , str(value.product_uom_id.name), letter_left)
					worksheet.write(row,col+2 , str(value.location_id.name), letter_left)
					worksheet.write(row,col+3 ,  (value.prod_lot_id.name or ''), letter_number)
					worksheet.write(row,col+4 ,  (value.package_id.name or ''), letter_number)
					worksheet.write(row,col+5, (value.partner_id.name or ''), letter_number)
					worksheet.write(row,col+6 , (value.theoretical_qty), letter_number)
					worksheet.write(row,col+7 ,  value.product_qty, letter_number)
					worksheet.write(row,col+8 ,  value.diference, letter_number)

					row+=1


			workbook.close()
			file_data.seek(0)

			self.write({'document':base64.encodestring(file_data.read()), 'filename':Header_Text+'.xlsx'})




StockInvetoryInherit()