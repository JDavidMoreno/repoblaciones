# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Habitat(models.Model):
	_name = 'planta.habitat'
	_description = "Habitats disponible para cada uno de los tipos de plantas"

	name = fields.Char("Nombre del Hábitat")
	descripcion = fields.Text("Descripción")


class Humedad(models.Model):
	_name = 'planta.humedad'
	_description = "Humedad necesaria para cada uno de los tipos de plantas"

	name = fields.Char("Humedad Entorno")
	descripcion = fields.Text("Descripción")


class Planta(models.Model):
	_name = 'planta'
	_description = "Cada una de las plantas disponibles para una repoblación"


	name = fields.Char("Nombre Común")
	nombre_científico = fields.Char("Nombre Científico")
	habitats = fields.Many2many('planta.habitat', 'name', "Habitats")
	humedad_entorno = fields.Many2many('planta.humedad', 'name', "Humedad")
	cantidad = fields.Integer("Cantidad de Ejemplares")
	tiempo_desarrollo = fields.Integer("Tiempo desarrollo expresado en días")
	disponibilidad = fields.Selection([('muy_alta','Muy alta'),('alta','Alta'),('media','Media'),('baja','Baja'),('muy_baja','Muy baja')], "Disponibilidad")
	coste_produccion = fields.Float("Coste en Euros por cada 100 plantas")


# class repoblaciones(models.Model):
#     _name = 'repoblaciones.repoblaciones'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100