# -*- coding: utf-8 -*-
{
    'name': "Repoblaciones",

    'summary': """
        Aplicación para la gestión de repoblaciones forestales.""",

    'description': """
        Con esta aplicación es más facil tener control de todos los pasos involucrados en la consecución de una Reforestación.

        Se pueden crear registros de plantas disponibles, y luego hacer uso de ellos como elementos independientes en la planificación de la reforestación.
        Así mismo es posible establecer el responsable de cada proyecto y los grupos de trabajadores que van a estar encargado de completar el proyecto.
        Por último, para cada proyecto existen opciones para tener acceso a un seguimiento del mismo, con el objetivo de asegurar que todas las metas se están compliento. En último lugar una valoración
        final del mismo puede ser efectuada de forma que puedan extraerse concluciones sobre si el proyecto ha estado bien orientado o no.
    """,

    'author': "J David Moreno",
    'website': "https://www.facebook.com/david.moreno0440",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'data/planta_humedad.xml',
        'data/planta_habitat.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}