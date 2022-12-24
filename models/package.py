from email.policy import default
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

class TravelPackage(models.Model):
    _name = 'travel.package'
    _description = 'Travel Package'

    product_sale_id = fields.Many2one('product.template', string='Sale', domain=['|', ('categ_id', '=', 'umroh'), ('categ_id.name', 'ilike', 'umroh')], required=True, readonly=True, states={'draft' : [('readonly', False)]})
    product_package_id = fields.Many2one('product.template', string='Package', domain=['|', ('categ_id', '=', 'umroh'), ('categ_id.name', 'ilike', 'umroh')], required=True, readonly=True, states={'draft' : [('readonly', False)]})
    berangkat = fields.Date(string='Tanggal Berangkat', required=True, readonly=True, states={'draft' : [('readonly', False)]})
    kembali = fields.Date(string='Tanggal Kembali', required=True, readonly=True, states={'draft' : [('readonly', False)]})
    quota = fields.Integer(string='Quota', default=20, readonly=True, states={'draft' : [('readonly', False)]})
    
    @api.depends('quota', 'manifest_line')
    def compute_remaining_quota(self):
        # print('=============', self)
        for i in self:
            i.remaining_quota = i.quota
            i.progress = 100 * len(i.manifest_line) / i.quota
            i.remaining_quota = i.remaining_quota - len(i.manifest_line)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('travel.package')
        return super(TravelPackage, self).create(vals)

    @api.onchange('product_package_id')
    def oncahnge_paket_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            for barang in self.product_package_id.bom_ids.bom_line_ids:
                vals = {
                    'nama_barang': barang.display_name,
                    'quantity': barang.product_qty,
                    'uom_id': barang.product_uom_id,
                    'unit_price': barang.product_id.standard_price,
                }
                lines.append((0, 0, vals))
            rec.component_line = lines


    progress = fields.Float(string='Quota Progress', compute='compute_remaining_quota')
    remaining_quota = fields.Integer(string='Remaining Quota', readonly=True, compute='compute_remaining_quota')
    name = fields.Char(string='Referensi', readonly=True, default='-')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done')], string='Status', default='draft')

    def package_draft(self):
        for o in self:
            return o.write({'state': 'draft'})
 
    def package_open(self):
        for o in self:
            return o.write({'state': 'confirm'})
 
    def package_done(self):
        for o in self:
            return o.write({'state': 'done'})

    def update_jamaah(self):
        print("********************************", 'masuk_update_jamaah')
        for x in self:
            x.manifest_line.unlink()
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&", x.name, x.id)
            order = self.env['sale.order'].search([('package_id', '=', x.id), ('state', 'in', ('sale', 'done'))])
            print ("##################################",order)
            for sale in order:
                print("#########################################", sale.name, sale.partner_id.name)
                for manifest in sale.manifest_line:
                    print("============================================================", manifest.partner_id.name)
                    print("*************************************************************", manifest.mahrom_id.name)
                    self.env['manifest.line'].create({
                        'partner_id': manifest.partner_id.id,
                        'tipe_kamar': manifest.tipe_kamar,
                        'mahrom_id': manifest.mahrom_id.id,
                        'package_id': x.id,
                        # 'order_id': sale.id,
                        })
            
    def cetak_manifest(self):
        return self.env.ref('ab_travel_umroh.report_travel_package_action').report_action(self)

    @api.depends('component_line.subtotal')
    def _amount_all(self):
        for o in self:
            o.update({
                'total_cost': sum([l.subtotal for l in o.component_line])
            })


    hotels_line = fields.One2many('hotels.line', 'package_id', string='Hotel')
    airlines_line = fields.One2many('airlines.line', 'package_id', string='Airlines')
    schedules_line = fields.One2many('schedule.line', 'package_id', string='Schedules')
    component_line = fields.One2many('component.line', 'package_id', string='Component')
    manifest_line = fields.One2many('manifest.line', 'package_id', string='Manifest', readonly=True)
    order_line = fields.One2many('sale.order', 'package_id', string='manifest')

    total_cost = fields.Integer('Total Cost', compute="_amount_all", track_visibility='onchange')

class ComponentLine(models.Model):
    _name = 'component.line'

    package_id = fields.Many2one('travel.package', string='HPP Lines')

    nama_barang = fields.Char(string='Barang', required=True)
    quantity = fields.Integer(string='Quantity')
    uom_id = fields.Many2one('uom.uom', string='Unit(s)')
    unit_price = fields.Integer(string='Unit Price')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal')

    # Subtotal HPP Lines
    @api.depends('quantity')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = 0
            if rec.quantity and rec.unit_price:
                rec.subtotal = rec.quantity * rec.unit_price

class HotelsLine(models.Model):
    _name = 'hotels.line'
    
    package_id = fields.Many2one('travel.package', string='Hotel')

    partner_id = fields.Many2one('res.partner', string='Nama Hotel', required=True, domain=[('hotel', '=', True)])
    check_in = fields.Date(string='Check In Hotel', required=True)
    check_out = fields.Date(string='Check Out Hotel', required=True)
    kota = fields.Char(string='Kota', related='partner_id.city', readonly=True)

class AirlinesLine(models.Model):
    _name = 'airlines.line'
    
    package_id = fields.Many2one('travel.package', string='Airline')
    
    partner_id = fields.Many2one('res.partner', string='Nama Airline', required=True, domain=[('airline', '=', True)])
    tanggal_berangkat = fields.Date('Tanggal Berangkat', required=True)
    kota_asal = fields.Char(string='Kota Asal', required=True)
    kota_tujuan = fields.Char(string='Kota Tujuan', required=True)

class ScheduleLine(models.Model):
    _name = 'schedule.line'
    
    package_id = fields.Many2one('travel.package', string='Schedule')

    schedules = fields.Char(string='Nama Kegiatan', required=True)
    tanggal_kegiatan = fields.Date('Tanggal Kegiatan')

class ManifestLine(models.Model):
    _name = 'manifest.line'
    
    package_id = fields.Many2one('travel.package', string='Manifest')
    order_id = fields.Many2one('sale.order', string='order')

    #Personal 
    partner_id = fields.Many2one('res.partner', string='Nama Jamaah', required=True)
    no_ktp = fields.Char(string='No.KTP', related='partner_id.ktp')
    mahrom_id = fields.Many2one('res.partner', string='Mahrom')
    title = fields.Char(string='Title', related='partner_id.title.name')
    umur = fields.Integer(string='Umur', compute='total_age')
    tempat_lahir = fields.Char(string='Tempat Lahir', related='partner_id.tempat')
    tanggal_lahir = fields.Date(string='Tanggal Lahir', related='partner_id.tanggal')
    tipe_kamar = fields.Selection([
        ('double', 'Double'),
        ('triple', 'Triple'),
        ('quad', 'Quad'),
    ], string='Tipe Kamar')
    jenis_kelamin = fields.Selection([
        ('pria', 'Laki - Laki'),
        ('perempuan', 'Perempuan'),
    ], string='Jenis Kelamin', related='partner_id.gender')
    users_id = fields.Many2one('res.users','Agent', default=lambda self: self.env.user)
    notes = fields.Char(string='Notes')

    #Field Passpor Information
    no_passpor = fields.Char(string='No.Passpor', related='partner_id.passpor')
    tanggal_berlaku = fields.Date(string='Tanggal Berlaku', related='partner_id.berlaku')
    nama_imigrasi = fields.Char(string='Imigrasi', related='partner_id.imigrasi')
    nama_passport = fields.Char(string='Nama Passpor', related='partner_id.nama_passpor')
    tanggal_expired = fields.Date(string='Tanggal Expired', related='partner_id.expired')
    # notes = fields.Char(string='Notes')

    #Field Scan Document
    scanner_passpor = fields.Binary(string='Scan Passpor', related='partner_id.scan_passpor')
    scanner_buku_nikah = fields.Binary(string='Scan Buku Nikah', related='partner_id.scan_buku_nikah')
    scanner_KTP = fields.Binary(string='Scan KTP', related='partner_id.scan_KTP')
    scanner_kartu_keluarga = fields.Binary(string='Scan Kartu Keluarga', related='partner_id.scan_kartu_keluarga')

    @api.depends('tanggal_lahir')
    def total_age(self):
        for record in self:
            if record.tanggal_lahir and record.tanggal_lahir <= fields.Date.today():
                record.umur = relativedelta(
                    fields.Date.from_string(fields.Date.today()),
                    fields.Date.from_string(record.tanggal_lahir)).years 
            else: 
                record.umur = 0




    