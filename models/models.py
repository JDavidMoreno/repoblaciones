# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

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
	coste = fields.Monetary("Precio", help="Precio de cada plantón", readonly=True, store=True, compute="_get_coste")
	cantidad = fields.Integer("Cantidad")
	precio_subtotal = fields.Monetary("Subtotal", compute="_get_subtotal", store=True)
	proyecto_id = fields.Many2one('proyecto', "Pertenece a ", ondelete="cascade")
	currency_id = fields.Many2one('res.currency', "Moneda", default=lambda self: self.env['res.currency'].browse(1))

	@api.depends('name')
	def _get_coste(self):
		self.coste = self.name.coste_produccion

	@api.depends('cantidad', 'name')
	def _get_subtotal(self):
		for elem in self:
			elem.precio_subtotal = elem.cantidad * elem.name.coste_produccion

	@api.constrains('cantidad','name')
	def _check_and_update_quantity(self):
		for elem in self:
			if elem.cantidad > elem.name.cantidad:
				raise ValidationError(_("La cantidad de plantas seleccionadas es mayor a las disponibles"))
			else:
				elem.name.cantidad -= elem.cantidad

	@api.model
	def unlink(self):
		if self.cantidad > 0:
			self.name.cantidad += self.cantidad
		return super().unlink()

class Test(models.Model):
	_name = 'testeando'

	name = fields.Char("Nombre Test")


class ProyectoEstado(models.Model):
	_name = 'proyecto.estado'
	_description = "Distintos estadíos de un proyecto hasta su terminación"
	_order = 'sequence'

	name = fields.Char("Estado")
	sequence = fields.Integer("Secuencia")
	default = fields.Boolean("Default")

class ProyectoEquipo(models.Model):
	_name = 'proyecto.equipo'
	_description = "Equipo de trabajo seleccionable para un Proyecto"

	name = fields.Char("Nombre")
	responsable_equipo = fields.Many2one('res.partner', "Responsable Equipo")
	componentes = fields.Many2many('res.partner', string="Componentes")
	coste = fields.Monetary("Coste Jornada", help="Coste del Equipo por una jornada completa")
	color = fields.Selection((('rojo',"Rojo"), ('verde',"Verde"),('amarillo',"Amarillo"),('azul',"Azul")), "Color")
	notas = fields.Text("Notas")
	currency_id = fields.Many2one('res.currency', "Moneda", default=lambda self: self.env['res.currency'].search([('name','=','EUR')]), readonly=True)

	

	@api.onchange('responsable_equipo', 'componentes')
	def _check_responsable(self):
		if self.responsable_equipo in self.componentes:
			return {'warning':{
				'title':"Responsable no puede ser un componente",
				'message': "El responsable no puede se un componente del equipo. Por favor, elige otro responsable o elimínalo como componente del equipo de trabajo"
			}}


	@api.constrains('responsable_equipo', 'componentes')
	def _constrain_check_responsable(self):
		if self.responsable_equipo in self.componentes:
			raise ValidationError("El responsable no puede se un componente del equipo. Por favor, elige otro responsable o elimínalo como componente del equipo de trabajo")


class ProyectoEquipoLinea(models.Model):
	_name = 'proyecto.equipo.linea'
	_description = "Cada una de las linea de trabajo de un proyecto asociada a un equipo"

	name = fields.Many2one('proyecto.equipo', required=True)
	coste_dias = fields.Monetary("Coste Jornada", compute="_get_coste", readonly=True, store=True)
	currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env['res.currency'].search([('name','=','EUR')]), readonly=True)
	numero_dias = fields.Integer("Número Jornadas")
	subtotal = fields.Monetary("Subtotal", compute="_get_subtotal", store=True)
	proyecto_id = fields.Many2one('proyecto',"Pertenede a ", readonly=True)

	@api.depends('name')
	def _get_coste(self):
		self.coste_dias = self.name.coste

	@api.depends('coste_dias','numero_dias')
	def _get_subtotal(self):
		self.subtotal = self.coste_dias * self.numero_dias


class Proyecto(models.Model):
	_name = 'proyecto'
	_description = "Proyecto de Reforestación"

	# Antes de guardas el proyecto parece que muestras todo, incluyendo plantas y equipos

	name = fields.Char("Nombre Proyecto", required=True)
	poblacion = fields.Char("Poblacion")
	provincia = fields.Char("Provincia")
	lat = fields.Float("Latitud", digits=(10,8))
	lng = fields.Float("Longitud", digits=(10,8))
	inversion = fields.Monetary("Inversión", help="Cantidad en Euros destinada al proyecto")
	origen_inversion = fields.Char("Origen Inversión", help="Entidad pública o privada que aporta el dinero necesario para el proyecto.")
	currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env['res.currency'].search([('name','=','EUR')]), readonly=True)
	proyecto_lines_ids = fields.One2many('proyecto.line', 'proyecto_id', string="Plantas Escogidas")
	inicio_proyecto = fields.Date("Fecha Inicio")
	final_proyecto = fields.Date("Fecha final estimada")
	responsable = fields.Many2one('res.users', "Responsable", required=True)
	equipos_trabajadores_lineas = fields.One2many('proyecto.equipo.linea', 'proyecto_id', string="Equipo de Trabajo")
	estado_id = fields.Many2one('proyecto.estado', "Estado Proyecto")
	subtotal_equipos = fields.Monetary("Subtotal Equipos", compute="_get_subtotal_equipos", store=True )
	subtotal_plantas = fields.Monetary("Subtotal Plantones", compute="_get_subtotal_plantas", store=True)
	precio_total = fields.Monetary("Precio Total", compute="_get_total", store=True)
	estudio_terreno = fields.Binary("Estudio del Terreno")
	estudio_terreno_filename = fields.Char("Estudio del Terreno filename")

	@api.model
	def create(self, vals):
		estado_id = self.env['proyecto.estado'].search([('sequence','=',1)])[0]
		vals['estado_id'] = estado_id.id 
		return super(Proyecto, self).create(vals)

	def avanzar_estado(self):
		proyecto = self[0]
		next_sequence = proyecto.estado_id.sequence + 1

		if next_sequence > len(self.env['proyecto.estado'].search([('name','!=','Cancelado')])):
			return False
		else:
			if proyecto.estado_id.sequence == 1:
				if not self.estudio_terreno:
					raise ValidationError("Faltan Documentos. El Estudio del Terreno no está subido. Por favor, asegurese de incluir este documento antes de avanzar de estado el proyecto.") 
			elif proyecto.estado_id.sequence == 2:
				if not self.proyecto_lines_ids:
					raise ValidationError("No ha sido seleccionada ningun tipo de plantones para este proyecto. Debe existir al menos un tipo seleccionado para poder avanzar de estado.")
				
				
		next_state = self.env['proyecto.estado'].search([('sequence','=',next_sequence)])[0]
		proyecto.estado_id = next_state.id

	# Debo hacer imposible de reeditar un proyecto que esté cancelado
	def cancelar_proyecto(self):
		estado_id = self.env['proyecto.estado'].search([('name','=','Cancelado')])
		self.estado_id = estado_id.id


	@api.depends('proyecto_lines_ids')
	def _get_subtotal_plantas(self):	
		for record in self:
			total = 0
			for line in record.proyecto_lines_ids:
				total += line.precio_subtotal
			record.subtotal_plantas = total

	@api.depends('equipos_trabajadores_lineas')
	def _get_subtotal_equipos(self):	
		for record in self:
			total = 0
			for line in record.equipos_trabajadores_lineas:
				total += line.subtotal
			record.subtotal_equipos = total

	@api.depends('subtotal_equipos', 'subtotal_plantas')
	def _get_total(self):
		for record in self:
			total = 0
			record.precio_total = record.subtotal_equipos + record.subtotal_plantas

			

	@api.onchange('responsable', 'equipo_trabajadores')
	def _onchange_check_responsable(self):

		for trabajador in self.equipos_trabajadores_lineas.name.componentes:
	
			if trabajador.email == self.responsable.login:
				return {'warning':{
					'title': "El responsable (" + self.responsable.name + ") no puede ser uno de los operarios",
					'message': "Elimina " +  self.responsable.name + " del Grupo de Trabajo o cambia de responsable"
				}}

	@api.constrains('responsable', 'equipo_trabajadores')
	def _check_responsable(self):
		for trabajador in self.equipos_trabajadores_lineas.name.componentes:
			if trabajador.email == self.responsable.login:
				raise ValidationError(_("El responsable (" + self.responsable.name + ") no puede ser uno de los operarios"))

