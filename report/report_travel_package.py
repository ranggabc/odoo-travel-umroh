from re import X
from odoo import api, fields, models
 
class PackageXlsx(models.AbstractModel):
    _name = 'report.ab_travel_umroh.report_package'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):
        sheet = workbook.add_worksheet('Package %s' % obj.name)
        text_top_style = workbook.add_format({
            'font_size': 12, 
            'bold': True ,
            'font_color' : 'white', 
            'bg_color': '#b904bf', 
            'valign': 'vcenter', 
            'text_wrap': True})
        text_header_style = workbook.add_format({
            'font_size': 12, 
            'bold': True ,
            'font_color' : 'white', 
            'bg_color': '#b904bf', 
            'valign': 'vcenter', 
            'text_wrap': True, 
            'align': 'center'})
        text_style = workbook.add_format({
            'font_size': 12,
            'valign': 'vcenter', 
            'text_wrap': True, 
            'align': 'center'})
        number_style = workbook.add_format({
            'num_format': '#,##0', 
            'font_size': 12, 
            'align': 'right', 
            'valign': 'vcenter', 
            'text_wrap': True})
 
        sheet.write(3, 2, "MANIFEST", text_top_style)
        sheet.write(3, 3, obj.name)
    
        row = 5
        sheet.freeze_panes(6, 17)
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 6, 20)
        sheet.set_column(6, 17, 20)
        header = ['NO', 'TITLE', 'GENDER', 'FULLNAME', 'TEMPAT LAHIR','TANGGAL LAHIR', 'NO. PASSPOR', 'PASSPOR ISSUED','PASSPOR EXPIRED','IMIGRASI', 'MAHROM', 'USIA', 'NIK', 'ORDER', 'ROOM TYPE', 'ROOM LEADER', 'NO.ROOM', 'ALAMAT']
        sheet.write_row(row, 0, header, text_header_style)

        row_airline = 7
        header_airline = ['NO', 'AIRLINE', 'DEPARTURE DATE', 'DEPARTURE CITY', 'ARTIVAL CITY']
            

        # Manifest 
        no_list = []
        title = []
        gender = []
        full_name = []
        tempat = []
        tanggal = []
        no_passpor = []
        berlaku = []
        expired = []
        imigrasi = []
        mahrom = []
        usia = []
        no_ktp = []
        order = []
        tipe_room = []
        room_leader = []
        no_room = []
        alamat = []

        #Manifest
        no = 1
        for x in obj.manifest_line:
            no_list.append(no)
            title.append(x.title)
            gender.append(x.jenis_kelamin)
            full_name.append(x.partner_id.name)
            tempat.append(x.tempat_lahir)
            tanggal.append(x.tanggal_lahir.strftime('%d-%m-%Y') if x.tanggal_lahir else '')
            no_passpor.append(x.no_passpor)
            berlaku.append(x.tanggal_berlaku.strftime('%d-%m-%Y') if x.tanggal_berlaku else '')
            expired.append(x.tanggal_expired.strftime('%d-%m-%Y') if x.tanggal_expired else '')
            imigrasi.append(x.nama_imigrasi)
            mahrom.append(x.mahrom_id.name or '-')
            usia.append(x.umur)
            no_ktp.append(x.no_ktp)
            domain = ['&', ('package_id', '=', obj.id), ('manifest_line.partner_id.name', '=', x.partner_id.name)]
            order_sale = self.env['sale.order'].search(domain)
            print("========================================", order_sale.name)
            order.append(order_sale.name)
            # print("########################################", x.partner_id.id)
            # print("#########################################", x.partner_id.name)
            tipe_room.append(x.tipe_kamar)
            room_leader.append("-")
            no_room.append("-")
            alamat.append(x.partner_id.city)
            row_airline += 1
            no+=1

        #Manifest
        row += 1
        sheet.write_column(row, 0, no_list, text_style)
        sheet.write_column(row, 1, title, text_style)
        sheet.write_column(row, 2, gender, text_style)
        sheet.write_column(row, 3, full_name, text_style)
        sheet.write_column(row, 4, tempat, text_style)
        sheet.write_column(row, 5, tanggal, text_style)
        sheet.write_column(row, 6, no_passpor, number_style)
        sheet.write_column(row, 7, berlaku, number_style)
        sheet.write_column(row, 8, expired, number_style)
        sheet.write_column(row, 9, imigrasi, text_style)
        sheet.write_column(row, 10, mahrom, text_style)
        sheet.write_column(row, 11, usia, text_style)
        sheet.write_column(row, 12, no_ktp, text_style)
        sheet.write_column(row, 13, order, text_style)
        sheet.write_column(row, 14, tipe_room, text_style)
        sheet.write_column(row, 15, room_leader, text_style)
        sheet.write_column(row, 16, no_room, text_style)
        sheet.write_column(row, 17, alamat, text_style)


        # Airline
        no_urut = []
        airline = []
        departure = []
        departure_city = []
        arrival_city = []

        #Airline
        no = 1
        for d in obj.airlines_line:
            no_urut.append(no)
            airline.append(d.partner_id.name)
            departure.append(d.tanggal_berangkat.strftime('%d-%m-%Y') if d.tanggal_berangkat else '')
            departure_city.append(d.kota_asal)
            arrival_city.append(d.kota_tujuan)
            no+=1

        sheet.write_row(row_airline, 2, header_airline, text_header_style)

        #Airline
        row_airline += 1
        sheet.write_column(row_airline, 2, no_urut, text_style)
        sheet.write_column(row_airline, 3, airline, text_style)
        sheet.write_column(row_airline, 4, departure, text_style)
        sheet.write_column(row_airline, 5, departure_city, text_style)
        sheet.write_column(row_airline, 6, arrival_city, text_style)