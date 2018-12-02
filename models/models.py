# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

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


	name = fields.Char("Nombre Común", required=True)
	nombre_científico = fields.Char("Nombre Científico")
	habitats_ids = fields.Many2many('planta.habitat', string="Habitats")
	humedad_entorno_ids = fields.Many2many('planta.humedad', string="Humedad")
	cantidad = fields.Integer("Cantidad de Ejemplares")
	desarrollo = fields.Integer("Desarrollo", help="Tiempo desarrollo expresado en días")
	disponibilidad = fields.Selection([('muy_alta','Muy alta'),('alta','Alta'),('media','Media'),('baja','Baja'),('muy_baja','Muy baja')], "Disponibilidad")
	coste_produccion = fields.Float("Coste en Euros por cada 100 plantas")


class ProyectoLine(models.Model):
	_name = 'proyecto.line'
	_descripcion = "Linea plantas en proyecto de Reforestación"

	name = fields.Many2one('planta', "Tipo de Planta")
	cantidad = fields.Integer("Cantidad")
	precio_total = fields.Float("Total", compute="_get_total", store=True)
	proyecto_id = fields.Many2one('proyecto', "Pertenece a ", ondelete="cascade")

	@api.depends('cantidad', 'name')
	def _get_total(self):
		for elem in self:
			elem.precio_total = elem.cantidad * elem.name.coste_produccion

class ProyectoEstado(models.Model):
	_name = 'proyecto.estado'
	_description = "Distintos estadíos de un proyecto hasta su terminación"
	_order = 'sequence'

	name = fields.Char("Estado")
	sequence = fields.Integer("Secuencia")
	default = fields.Boolean("Default")

class Proyecto(models.Model):
	_name = 'proyecto'
	_description = "Proyecto de Reforestación"

	name = fields.Char("Nombre Proyecto", required=True)
	poblacion = fields.Char("Poblacion")
	provincia = fields.Char("Provincia")
	lat = fields.Float("Latitud", digits=(10,8))
	lng = fields.Float("Longitud", digits=(10,8))
	inversion = fields.Float("Inversión", help="Cantidad en Euros destinada al proyecto")
	origen_inversion = fields.Char("Origen Inversión", help="Entidad pública o privada que aporta el dinero necesario para el proyecto.")
	proyecto_lines_ids = fields.One2many('proyecto.line', 'proyecto_id', string="Plantas Escogidas")
	inicio_proyecto = fields.Date("Fecha Inicio")
	final_proyecto = fields.Date("Fecha final estimada")
	responsable = fields.Many2one('res.users', "Responsable")
	equipo_trabajadores = fields.Many2one('res.partner', "Equipo de Trabajo")
	estado_id = fields.Many2one('proyecto.estado', "Estado Proyecto")

	@api.model
	def create(self, vals):
		estado_id = self.env['proyecto.estado'].search([('sequence','=',1)])[0]
		vals['estado_id'] = estado_id.id 
		return super(Proyecto, self).create(vals)

	def avanzar_estado(self):
		# Voy por aqui, comprobar con logger que devuelve self[0] y realizar ajustes para que la función funcione
		proyecto = self[0]
		next_sequence = proyecto.estado_id.sequence + 1

		if next_sequence > len(self.env['proyecto.estado'].search([])):
			return False
		else:
			next_state = self.env['proyecto.estado'].search([('sequence','=',next_sequence)])[0]

		proyecto.estado_id = next_state.id




