from dataclasses import field
import json
from odoo import api, fields, models
 
class ResPartner(models.Model):
    _inherit = 'res.partner'

    #Additional Information 
    ktp = fields.Char(string='No.KTP')
    ayah = fields.Char(string='Nama Ayah')
    pekerjaan_ayah = fields.Char(string='Pekerjaan Ayah')
    ibu = fields.Char(string='Nama Ibu')
    pekerjaan_ibu = fields.Char(string='Pekerjaan Ibu')
    tempat = fields.Char(string='Tempat Lahir')
    tanggal = fields.Date(string='Tanggal Lahir')
    pendidikan = fields.Selection([
        ('sd', 'SD Sederajat'),
        ('smp', 'SMP Sederajat'),
        ('smk', 'SMK Sedarajat'),
        ('diploma', 'Diploma'),
        ('sarjana', 'S1'),
        ('pascasarjana', 'S2'),
        ('doktor', 'S3'),
    ], string='Pendidikan')
    status = fields.Selection([
        ('menikah', 'Married'),
        ('lajang', 'Single'),
        ('cerai', 'Divorce'),
    ], string='Status Pernikahan')
    gender = fields.Selection([
        ('pria', 'Laki - Laki'),
        ('perempuan', 'Perempuan'),
    ], string='Jenis Kelamin')
    golongan_darah = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O'),
    ], string='Golongan Darah')
    ukuran = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL'),
        ('4L', '4L'),
    ], string='Ukuran Baju')

    #Field Passpor Information
    passpor = fields.Char(string='No.Passpor')
    berlaku = fields.Date(string='Tanggal Berlaku')
    imigrasi = fields.Char(string='Imigrasi')
    nama_passpor = fields.Char(string='Nama Passpor')
    expired = fields.Date(string='Tanggal Expired')

    #Field Scan Document
    scan_passpor = fields.Binary(string='Scan Passpor')
    scan_buku_nikah = fields.Binary(string='Scan Buku Nikah')
    scan_KTP = fields.Binary(string='Scan KTP')
    scan_kartu_keluarga = fields.Binary(string='Scan Kartu Keluarga')

    #Field Airline & Hotel
    airline = fields.Boolean(string='Airlines')
    hotel = fields.Boolean(string='Hotels')

    @api.model
    def create(self, vals):
        print("============ELSE=======", vals)
        return super(ResPartner, self).create(vals)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    package_id = fields.Many2one('travel.package', 'Paket Perjalanan', domain=[('state','=','confirm')])
    manifest_line = fields.One2many('manifest.line', 'order_id', string='Manifest', tracking=True)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    product_id = fields.Many2one('product.template', string='field_name')

    def print_delivery(self):
        return self.env.ref('ab_travel_umroh.report_delivery_order_action').report_action(self)

class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_widget(self):
        data = json.loads(self.invoice_payments_widget)
        if data:
            return data['content']
        return


