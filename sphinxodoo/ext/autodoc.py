#! /usr/bin/env python
# -*- coding: utf-8 -*-

import imp
import os
import sys


def setup(app):
    """
    Setup function used by sphinx, when loading sphinxodoo as sphinx extension
    """
    app.add_config_value('sphinxodoo_addons', [], True)
    app.add_config_value('sphinxodoo_root_path', '', True)
    app.add_config_value('sphinxodoo_addons_path', [], True)
    app.connect('builder-inited', load_modules)

    return {'version': '0.3.1'}


def load_modules(app):
    def load_odoo_modules(addons):
        for module_name in addons:
            info = openerp.modules.module \
                .load_information_from_description_file(module_name)
            try:
                f, path, descr = imp.find_module(
                    module_name, openerp.tools.config['addons_path'].split(','))
            except ImportError:
                # skip non module directories
                continue
            mod = imp.load_module(
                'openerp.addons.%s' % module_name, f, path, descr)
            setattr(openerp.addons, module_name, mod)
            setattr(getattr(openerp.addons, module_name),
                    '__doc__', info['description'])

    addons = app.env.config.sphinxodoo_addons
    addons_path = ','.join(app.env.config.sphinxodoo_addons_path)

    if(app.env.config.sphinxodoo_root_path):
        sys.path.append(app.env.config.sphinxodoo_root_path)
    import openerp

    if not addons_path:
        addons_path = os.environ.get('ODOO_ADDONS_PATH', '')

    if addons_path:
        openerp.tools.config.parse_config([
            '--addons-path=%s' % addons_path,
        ])

    load_odoo_modules(addons)
