import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-opnsynid-account-voucher",
    description="Meta package for open-synergy-opnsynid-account-voucher Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_voucher_advance_settlement',
        'odoo14-addon-ssi_voucher_bank_cash',
        'odoo14-addon-ssi_voucher_cheque',
        'odoo14-addon-ssi_voucher_giro',
        'odoo14-addon-ssi_voucher_invoice_settlement',
        'odoo14-addon-ssi_voucher_mixin',
        'odoo14-addon-ssi_voucher_refund_settlement',
        'odoo14-addon-ssi_voucher_settlement_common',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
