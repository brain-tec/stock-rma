# Copyright (C) 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

{
    'name': 'RMA (Return Merchandise Authorization)',
    'version': '12.0.2.2.0',
    'license': 'LGPL-3',
    'category': 'RMA',
    'summary': 'Introduces the return merchandise authorization (RMA) process '
               'in odoo',
    'author': "Eficent, Odoo Community Association (OCA)",
    'website': 'https://github.com/Eficent/stock-rma',
    'depends': ['stock', 'mail', 'web'],
    'demo': ['demo/stock_demo.xml',
             ],
    'data': ['security/rma.xml',
             'security/ir.model.access.csv',
             'data/rma_sequence.xml',
             'data/stock_data.xml',
             'data/rma_operation.xml',
             'report/rma_report.xml',
             'report/rma_report_templates.xml',
             'views/rma_order_view.xml',
             'views/rma_operation_view.xml',
             'views/rma_order_line_view.xml',
             'views/stock_view.xml',
             'views/stock_warehouse.xml',
             'views/product_view.xml',
             'views/res_partner_view.xml',
             'wizards/rma_make_picking_view.xml',
             'wizards/rma_add_stock_move_view.xml',
             'wizards/stock_config_settings.xml',
             'wizards/rma_order_line_make_supplier_rma_view.xml',
             ],
    'installable': True,
    'auto_install': False,
}
