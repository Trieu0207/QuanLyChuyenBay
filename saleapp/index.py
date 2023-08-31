import cloudinary.uploader
from flask import render_template, request, redirect, url_for, session, jsonify
from saleapp import app, controller, login, utils
from flask_login import current_user
import dao
from cloudinary import uploader
import re
from flask_login import login_user, logout_user
from saleapp.admin import *


@app.route('/', methods=['get', 'post'])
def home():
    global tuyen_bay
    tuyen = dao.load_tuyen_bay_by_kw(kw=request.args.get('keyword'))
    all_tuyen = dao.load_tuyen_bay()
    ten_diem_di = dao.load_ten_diem_di()
    ten_diem_den = dao.load_ten_diem_den()
    if request.method.__eq__('POST'):
        diem_di = request.form['diem_di']
        diem_den = request.form['diem_den']
        tuyen_bay = dao.search_tuyen_bay(diem_di, diem_den)
        return render_template('index.html', tuyen_bay=tuyen_bay,
                               ten_diem_den=ten_diem_den,
                               ten_diem_di=ten_diem_di)
    return render_template('index.html', tuyen=tuyen, all_tuyen=all_tuyen,
                           ten_diem_den=ten_diem_den, ten_diem_di=ten_diem_di)


@app.route('/chuyen_bay/<int:tuyen_bay_id>')
def chuyen_bay(tuyen_bay_id):
    try:
        ds_lich_quy_dinh = dao.load_lich_bay_quy_dinh(tuyen_bay_id)
        count_lich = dao.count_lich_bay(tuyen_bay_id)
        lich_bay = dao.load_lich_bay(tuyen_bay_id)
        tuyen = dao.load_tuyen_bay_by_id(tuyen_bay_id)
        ds_ve_normal = dao.load_gia_ve_by_chuyen_bay(ds_lich_quy_dinh, hang_ve=1)
        ds_ve_vip = dao.load_gia_ve_by_chuyen_bay(ds_lich_quy_dinh, hang_ve=2)
        ex = ""
    except Exception as e:
        ex = str(e)
        return render_template('chuyenBays.html', ex=ex)

    return render_template('chuyenBays.html',
                           ds_lich_quy_dinh=ds_lich_quy_dinh, ex=ex,
                           count_lich=count_lich, lich_bay=lich_bay, tuyen=tuyen,
                           ds_ve_vip=ds_ve_vip, ds_ve_normal=ds_ve_normal)

@app.route('/register', methods=['get', 'post'])
def user_register():
    ex = ""
    if request.method.__eq__('POST'):
        ho_ten = request.form['first_name']
        ngay_thang_nam_sinh = request.form['birth_day']
        email = request.form['email']
        sdt = request.form['sdt']
        ten_dang_nhap = request.form['user_name']
        mat_khau = request.form['pass']
        file_to_upload = request.files['avatar']
        avt_path = ""
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload)
            app.logger.info(upload_result)
            avt_path = upload_result['secure_url']
        try:

            dao.register(ho_va_ten=ho_ten, ngay_sinh=ngay_thang_nam_sinh,
                         email=email, sdt=sdt, ten_dang_nhap=ten_dang_nhap,
                         mat_khau=mat_khau, avatar=avt_path)
            return redirect(url_for('user_login'))
        except Exception as e:
            ex = str(e)

    return render_template('register.html', method=['get', 'post'], ex=ex)


@app.route('/login', methods=['get', 'post'])
def user_login():
    ex = ""
    if request.method.__eq__('POST'):
        user_name = request.form['user_name']
        password = request.form['password']
        try:
            user = dao.login(user_name=user_name, password=password)
            if user:
                login_user(user=user)
                return redirect(url_for('home'))
        except Exception as e:
            ex = str(e)
    return render_template('login.html', ex=ex)


@app.route('/user-logout')
def user_logout():
    logout_user()
    return redirect('/')


@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id)

@app.route('/ve/<int:lich_bay_id>')
def ve_bay(lich_bay_id):
    ds_ghe = dao.load_ds_ghe(lich_bay_id)
    lich_bay = dao.find_lich_bay(lich_bay_id)
    ds_ve = dao.load_ds_ve(lich_bay_id)
    table_ghe = dao.load_table_ghe(lich_bay_id)
    ghe_da_dat = dao.get_ghe_da_dat(lich_bay_id)
    ghe_chua_dat = dao.get_ghe_chua_dat(lich_bay_id)
    gia_ve_normal = dao.load_don_gia_by_lich(lich_bay_id, 1)
    gia_ve_vip = dao.load_don_gia_by_lich(lich_bay_id, 2)
    chuyen = dao.get_chuyen_bay_by_id(lich_bay_id)
    return render_template('ve.html', ds_ghe=ds_ghe, table_ghe=table_ghe, chuyen=chuyen,
                           ghe_chua_dat=ghe_chua_dat, ghe_da_dat=ghe_da_dat, lich_bay=lich_bay, ds_ve=ds_ve,
                           gia_ve_normal = gia_ve_normal, gia_ve_vip = gia_ve_vip, lich_bay_id = lich_bay_id)

@app.route('/ve', methods=['get', 'post'])
def info_ve():
    if request.method.__eq__('POST'):
        ten = request.form['name']
        ngay_sinh = request.form['birth_day']
        cccd = request.form['cccd']
        vi_tri_ngoi = request.form['ghe']
        chuyen_bay = request.form['chuyen']
        lich_bay_id = request.form['lich_bay_id']
        lich_bay = dao.find_lich_bay(lich_bay_id)
        chuyen_bay_id = dao.get_chuyen_bay_by_id(chuyen_bay)
        err_mess = ""
        if current_user.is_authenticated:
            dao.dat_ve(ten, ngay_sinh, cccd, vi_tri_ngoi, chuyen_bay, current_user, lich_bay.id)
            return redirect(url_for('ve_bay', lich_bay_id=lich_bay.id))
        return redirect(url_for('ve_bay', lich_bay_id=lich_bay.id, ex=err_mess))
        # err_mess = "Yêu cầu cần được đăng nhập"
        # return redirect(url_for('ve_bay', lich_bay_id=lich_bay.id))
    return render_template('index.html')


@app.route('/thanh-toan', methods=['get', 'post'])
def thanh_toan():
    err_mess = "Bạn chưa mua vé"
    if current_user.is_authenticated:
        ds_ve = dao.load_ds_ve_chua_thanh_toan(current_user)
        tong_tien = dao.tong_tien()
        id_hoa_don = dao.id_hoa_don_chua_thanh_toan()
        if request.method.__eq__('POST'):
            if request.form['ve_id']:
                ve_id = request.form['ve_id']
                dao.xoa_ve(ve_id)
                return redirect(url_for('thanh_toan'))


        if ds_ve:
            return render_template('thanh_toan.html', ds_ve=ds_ve, tong_tien=tong_tien,
                                   id_hoa_don = id_hoa_don)
        else:

            return render_template('thanh_toan.html', id_hoa_don= id_hoa_don)
    else:
        err_mess = "Bạn chưa đăng nhập"
        return render_template('thanh_toan.html', err_mess=err_mess)

@app.route('/xac-nhan-thanh-toan', methods=['get', 'post'])
def xac_nhan_thanh_toan():
    if request.method.__eq__('POST'):
        temp = request.form['submit']
        dao.xac_nhan_thanh_toan()
        success = "Ban đã đặt vé thành công thành công"
        return render_template('thanh_toan.html', success=success)
    return render_template('index.html')

@app.route('/lichbay', methods=['get', 'post'])
def lap_lich_bay():
    chuyen = dao.load_all_chuyen_bay()
    if request.method.__eq__('POST'):
        if current_user.is_authenticated:
                chuyen_id = request.form['chuyen']
                # ngay_di = request.form['thoi_gian_khoi_hanh']
                thoi_gian_khoi_hanh = request.form['thoi_gian_khoi_hanh']
                time = request.form['thoi_gian_bay']
                so_ghe_loai_1 = request.form['ghe_loai_1']
                so_ghe_loai_2 = request.form['ghe_loai_2']
                gia_1 = request.form['gia_1']
                gia_2 = request.form['gia_2']
                thoi_gian_bay = dao.find_gio_bay(time)
                tuyen_bay_id = dao.load_tuyen_bay_by_chuyen_bay(chuyen_id)
                add_lich = dao.them_lich_bay(thoi_gian_bay,
                                             thoi_gian_khoi_hanh, chuyen_id, so_ghe_loai_1,
                                             so_ghe_loai_2,tuyen_bay_id, gia_1, gia_2)
                if chuyen_id:
                    chuyen_bay = dao.load_chuyen_bay(chuyen_id)
                    san_di = dao.load_ten_san_di(chuyen_id)
                    san_den = dao.load_ten_san_den(chuyen_id)
                    san = dao.load_all_san_bay()
                    return render_template('laplich.html', chuyen_bay=chuyen_id,
                                           chuyen=chuyen_bay, san_den=san_den, san_di=san_di, san = san)
            # ngay_di = request.form['lap_lich_bay']
            # thoi_gian_bay = request.form['thoi_gian_bay']
            # return redirect(url_for('home'))
    return render_template('laplich.html', chuyen = chuyen)
# @app.route('/laplich', methods=['get', 'post'])
# def check_lich_bay():
#     if request.method.__eq__('POST'):
#         return ren
#         # if current_user.is_authenticated:
#         #     ten_diem_di = dao.load_ten_diem_di()
#         #     ten_diem_den = dao.load_ten_diem_den()
#         #     if request.form['chuyen']:
#         #         chuyen_bay = request.form['chuyen']
#         #         ngay_di = request.form['thoi_gian_khoi_hanh']
#         #         chuyen = dao.load_chuyen_bay(chuyen_bay)
#         #         if chuyen:
#         #             san_di = dao.load_ten_san_di(chuyen_bay)
#         #             san_den = dao.load_ten_san_den(chuyen_bay)
#         #             return render_template('index.html')
#         #     ngay_di = request.form['ngay_di']
#         #     thoi_gian_bay = request.form['thoi_gian_bay']
#
#     return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
