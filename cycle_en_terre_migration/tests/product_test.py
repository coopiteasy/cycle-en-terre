# © 2016 Robin Keunen, Coop IT Easy SCRL fs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo.tests.common import TransactionCase


# I did not manage to get these tests to run
class ProductMigration(TransactionCase):
    def setUp(self):
        super(ProductMigration, self).setUp()

    def test_me(self):
        self.assertEqual(1 + 1, 3)

    def test_migrate_variants_to_template(self):
        # These print statement should be replaced by 'logger'
        # statement. These print statement prevent this file to pass
        # linting check. As mentioned in a comment above, this test doesn't
        # work so I just comment out these lines. -- remytms
        # print('**--' * 100)
        # print('**--' * 100)
        # print('**--' * 100)
        # print('**--' * 100)
        # print('**--' * 100)
        template = self.env["product.template"]
        template.migrate_variants_to_template()
        self.assertTrue(False)
