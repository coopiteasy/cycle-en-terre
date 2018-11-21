# © 2016 Robin Keunen, Coop IT Easy SCRL fs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo.tests.common import TransactionCase


# I did not manage to get these tests to run
class ProductMigration(TransactionCase):

    def setUp(self):
        super(ProductMigration, self).setUp()

    def test_me(self):
        self.assertEqual(1+1, 3)

    def test_migrate_variants_to_template(self):
        print('**--' * 100)
        print('**--' * 100)
        print('**--' * 100)
        print('**--' * 100)
        print('**--' * 100)
        template = self.env['product.template']
        template.migrate_variants_to_template()
        self.assertTrue(False)
