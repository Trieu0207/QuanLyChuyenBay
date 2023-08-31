from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, \
    Date, DateTime, Enum, Time
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from saleapp import db, app
from enum import Enum as user_enum


class base_model(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Hang_bay(base_model):
    __tablename__ = "hang_bay"
    ten = Column(String(50), nullable=False)
    may_bay = relationship('May_bay', backref='hang_bay', lazy=True)
    chuyen_bay = relationship('Chuyen_bay', backref='hang_bay', lazy=True)
    ve = relationship('Ve_may_bay', backref='hang_bay', lazy=True)


class Tuyen_bay(base_model):
    __tablename__ = "tuyen_bay"
    img = Column(String(200))
    ten = Column(String(10), nullable=False)
    diem_di = Column(String(50), nullable=False)
    diem_den = Column(String(50), nullable=False)
    Chuyen_bays = relationship('Chuyen_bay', backref='tuyen_bay', lazy=True)

    def __str__(self):
        return self.ten


class May_bay(base_model):
    __tablename__ = "may_bay"
    hang_bay_id = Column(Integer, ForeignKey(Hang_bay.id), nullable=False)
    ten = Column(String(20), nullable=False)
    loai_may_bay = Column(String(20), nullable=False)
    ghi_chu = Column(String(255))
    Ghes = relationship('Ghe', backref='may_bay', lazy=True)
    Chuyen_bays = relationship('Chuyen_bay', backref='may_bay', lazy=True)

    def __str__(self):
        return self.ten


class San_bay(base_model):
    __tablename__ = "san_bay"
    ten_san_bay = Column(String(50), nullable=False)
    San_bay_trung_gian_s = relationship('San_bay_trung_gian', backref='San_bay', lazy=True)

    # chuyen_bay_s = relationship('Chuyen_bay', backref='San_bay', lazy = True)
    def __str__(self):
        return self.ten_san_bay


class Chuyen_bay(base_model):
    __tablename__ = "chuyen_bay"
    hang_bay_id = Column(Integer, ForeignKey(Hang_bay.id), nullable=False)
    loai_chuyen_bay = Column(String(5), nullable=False)
    trang_thai = Column(String(10), nullable=False)
    tuyen_bay_id = Column(Integer, ForeignKey(Tuyen_bay.id), nullable=False)
    Ve_may_bays = relationship('Ve_may_bay', backref='chuyen_bay', lazy=True)
    san_bay_di_id = Column(Integer, ForeignKey(San_bay.id), nullable=False)
    san_bay_di = relationship('San_bay', foreign_keys='Chuyen_bay.san_bay_di_id')
    san_bay_den_id = Column(Integer, ForeignKey(San_bay.id), nullable=False)
    san_bay_den = relationship('San_bay', foreign_keys='Chuyen_bay.san_bay_den_id')
    may_bay_id = Column(Integer, ForeignKey(May_bay.id), nullable=False)
    san_bay_trung_gian_s = relationship('San_bay_trung_gian', backref='Chuyen_bay', lazy=True)


class San_bay_trung_gian(base_model):
    __tablename__ = "san_bay_trung_gian"
    san_bay_id = Column(Integer, ForeignKey(San_bay.id), nullable=False)
    chuyen_bay_id = Column(Integer, ForeignKey(Chuyen_bay.id), nullable=False)
    thoi_gian_cho = Column(Time, nullable=False)
    ghi_chu = Column(String(255))

    def __str__(self):
        return San_bay.ten_san_bay


class Ghe(base_model):
    __tablename__ = "ghe"
    ten_ghe = Column(String(10), nullable=False)
    loai_ghe = Column(String(10), nullable=False)
    trang_thai = Column(Boolean, default=False)
    ve_may_bays = relationship('Ve_may_bay', backref='ghe', lazy=True)
    Chiec_may_bay_id = Column(Integer, ForeignKey(May_bay.id), nullable=False)

    def __str__(self):
        return self.ten_ghe


class loai_nguoi_dung(user_enum):
    QT = 1
    NV = 2
    ND = 3


class Nguoi_dung(base_model):
    __tablename__ = "nguoi_dung"
    ho_va_ten = Column(String(150), nullable=False)
    ngay_thang_nam_sinh = Column(Date)
    email = Column(String(50), nullable=False)
    sdt = Column(String(10), nullable=False)
    ten_dang_nhap = Column(String(30), nullable=False)
    mat_khau = Column(String(30), nullable=False)
    avatar = Column(String(100))
    loai_nguoi_dung = Column(Enum(loai_nguoi_dung), default=loai_nguoi_dung.ND)
    hoat_dong = Column(Boolean, default=True)
    ngay_dang_ki = Column(DateTime)
    Ve_may_bays = relationship('Ve_may_bay', backref='nguoi_dung', lazy=True)
    Hoa_dons = relationship('Hoa_don', backref='nguoi_dung', lazy=True)

    def __str__(self):
        return self.ten_dang_nhap


class Hoa_don(base_model):
    __tablename__ = "hoa_don"
    thoi_gian_thanh_toan = Column(DateTime, nullable=False)
    so_luong_ve = Column(Integer, nullable=False)
    tong_tien = Column(Float, nullable=False)
    Ve_may_bays = relationship('Ve_may_bay', backref='hoa_don', lazy=True)
    nguoi_thanh_toan = Column(Integer, ForeignKey(Nguoi_dung.id), nullable=False)


class Ve_may_bay(base_model):
    ten = Column(String(100), nullable=False, unique=True)
    cccd = Column(String(12), nullable=False)
    ngay_sinh = Column(DateTime, nullable=False)
    gia_tien = Column(Float, nullable=False)
    hang_bay_id = Column(Integer, ForeignKey(Hang_bay.id), nullable=False)
    hang_ve = Column(String(20), nullable=False)
    Ngay_xuat_ve = Column(DateTime, nullable=False)
    ghe_id = Column(Integer, ForeignKey(Ghe.id), nullable=False)
    chuyen_bay_id = Column(Integer, ForeignKey(Chuyen_bay.id), nullable=False)
    nguoi_mua_id = Column(Integer, ForeignKey(Nguoi_dung.id), nullable=False)
    hoa_don_id = Column(Integer, ForeignKey(Hoa_don.id), nullable=False)


class Lich_bay(base_model):
    __tablename__ = "lich_bay"
    thoi_gian_khoi_hanh = Column(DateTime, nullable=False)
    so_ghe_loai_1 = Column(Integer, nullable=False)
    so_ghe_loai_2 = Column(Integer, nullable=False)
    chuyen_bay_id_id = Column(Integer, ForeignKey(Chuyen_bay.id), nullable=False)
    chuyen_bays = relationship('Chuyen_bay', foreign_keys='Lich_bay.chuyen_bay_id_id')
    san_bay_di_id_id = Column(Integer, ForeignKey(Chuyen_bay.id), nullable=False)
    san_bay_dis = relationship('Chuyen_bay', foreign_keys='Lich_bay.san_bay_di_id_id')
    san_bay_den_id_id = Column(Integer, ForeignKey(Chuyen_bay.id), nullable=False)
    san_bay_dens = relationship('Chuyen_bay', foreign_keys='Lich_bay.san_bay_den_id_id')


with app.app_context():
    if __name__ == '__main__':
        db.create_all()
        # tao_tuyen_bay = [
        #     {
        #         "img": "https://images.pexels.com/photos/12635055/pexels-photo-12635055.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        #         "ten": "HN-DN",
        #         "diem_di": "Hà Nội",
        #         "diem_den": "Đà Nẵng"
        #     },
        #     {
        #         "img": "https://images.pexels.com/photos/7999857/pexels-photo-7999857.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        #         "ten": "HN-HCM",
        #         "diem_di": "Hà Nội",
        #         "diem_den": "Tp.Hồ Chí Minh"
        #     },
        #     {
        #         "img": "https://i.pinimg.com/564x/7e/5e/e7/7e5ee7b730518d2647d1f358b8743b21.jpg",
        #         "ten": "HN-DL",
        #         "diem_di": "Hà Nội",
        #         "diem_den": "Đà Lạt"
        #     },
        #     {
        #         "img": "https://images.pexels.com/photos/7715276/pexels-photo-7715276.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        #         "ten": "HCM-DN",
        #         "diem_di": "Tp.Hồ Chí Minh",
        #         "diem_den": "Đà Nẵng"
        #     },
        #     {
        #         "img": "https://i.pinimg.com/564x/7e/5e/e7/7e5ee7b730518d2647d1f358b8743b21.jpg",
        #         "ten": "DN-DL",
        #         "diem_di": "Đà Nẵng",
        #         "diem_den": "Đà lạt"
        #     }
        # ]
        # for t in tao_tuyen_bay:
        #     tuyen = Tuyen_bay(ten=t['ten'], diem_di=t['diem_di'], diem_den=t['diem_den'], img=t['img'])
        #     db.session.add(tuyen)
        # db.session.commit()

        # data base của chương trình
        tao_san_bay = [{"ten_san_bay": "Nội Bài"},
                       {"ten_san_bay": "Tân Sơn Nhất"},
                       {"ten_san_bay": "Chu Lai"},
                       {"ten_san_bay": "Liên Khương"}]
        for t in tao_san_bay:
            san = San_bay(ten_san_bay=t['ten_san_bay'])
            db.session.add(san)
        db.session.commit()
        tao_tuyen_bay = [
            {
                "img": "https://images.pexels.com/photos/7715276/pexels-photo-7715276.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
                "ten": "HN-DN",
                "diem_di": "Hà Nội",
                "diem_den": "Đà Nẵng"
            },
            {
                "img": "https://images.pexels.com/photos/1437618/pexels-photo-1437618.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
                "ten": "DN-HN",
                "diem_di": "Đà Nẵng",
                "diem_den": "Hà Nội"
            },
            {
                "img": "https://images.pexels.com/photos/11742806/pexels-photo-11742806.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
                "ten": "HN-HCM",
                "diem_di": "Hà Nội",
                "diem_den": "Tp.Hồ Chí Minh"
            },
            {
                "img": "https://images.pexels.com/photos/1437618/pexels-photo-1437618.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
                "ten": "HCM-HN",
                "diem_di": "Tp.Hồ Chí Minh",
                "diem_den": "Hà Nội"
            },
            {
                "img": "https://i.pinimg.com/564x/7e/5e/e7/7e5ee7b730518d2647d1f358b8743b21.jpg",
                "ten": "HN-DL",
                "diem_di": "Hà Nội",
                "diem_den": "Đà Lạt"
            },
            {
                "img": "https://images.pexels.com/photos/1437618/pexels-photo-1437618.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
                "ten": "DL-HN",
                "diem_di": "Đà Lạt",
                "diem_den": "Hà Nội"
            },
            {
                "img": "https://images.pexels.com/photos/7715276/pexels-photo-7715276.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
                "ten": "HCM-DN",
                "diem_di": "Tp.Hồ Chí Minh",
                "diem_den": "Đà Nẵng"
            },
            {
                "img": "https://images.pexels.com/photos/11742806/pexels-photo-11742806.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
                "ten": "DN-HCM",
                "diem_di": "Đà Nẵng",
                "diem_den": "Tp.Hồ Chí Minh"
            }
        ]
        for t in tao_tuyen_bay:
            tuyen = Tuyen_bay(ten=t['ten'], diem_di=t['diem_di'], diem_den=t['diem_den'], img=t['img'])
            db.session.add(tuyen)
        tao_may_bay = [
            {
                "ten": "xp1",
                "hang_bay": "VNA",
                "loai_may_bay": "900CC",
            },
            {
                "ten": "2k8g",
                "hang_bay": "BBA",
                "loai_may_bay": "900CC",
            },
            {
                "ten": "asmr",
                "hang_bay": "VNA",
                "loai_may_bay": "900CC",
            },
            {
                "ten": "w200",
                "hang_bay": "VJA",
                "loai_may_bay": "900CC",
            }
        ]
        for t in tao_may_bay:
            mb = May_bay(ten=t['ten'], hang_bay=t['hang_bay'],
                         loai_may_bay=t['loai_may_bay'])
            db.session.add(mb)
        tao_ghe_xp1 = [
            {
                "ten_ghe": "xp1-a1",
                "loai_ghe": 1,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-a2",
                "loai_ghe": 1,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-a3",
                "loai_ghe": 1,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-a4",
                "loai_ghe": 1,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-a5",
                "loai_ghe": 1,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-a6",
                "loai_ghe": 1,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-a7",
                "loai_ghe": 1,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-a8",
                "loai_ghe": 1,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-a9",
                "loai_ghe": 1,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-a10",
                "loai_ghe": 1,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-b1",
                "loai_ghe": 2,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-b2",
                "loai_ghe": 2,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-b3",
                "loai_ghe": 2,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-b4",
                "loai_ghe": 2,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-b5",
                "loai_ghe": 2,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-b6",
                "loai_ghe": 2,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-b7",
                "loai_ghe": 2,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-b8",
                "loai_ghe": 2,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-b9",
                "loai_ghe": 2,
                "chiec_may_bay": 1
            },
            {
                "ten_ghe": "xp1-b10",
                "loai_ghe": 2,
                "chiec_may_bay": 1
            },

        ]
        tao_ghe_2k8g = [
            {
                "ten_ghe": "2k8g-a1",
                "loai_ghe": 1,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-a2",
                "loai_ghe": 1,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-a3",
                "loai_ghe": 1,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-a4",
                "loai_ghe": 1,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-a5",
                "loai_ghe": 1,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-a6",
                "loai_ghe": 1,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-a7",
                "loai_ghe": 1,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-a8",
                "loai_ghe": 1,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-a9",
                "loai_ghe": 1,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-a10",
                "loai_ghe": 1,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-b1",
                "loai_ghe": 2,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-b2",
                "loai_ghe": 2,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-b3",
                "loai_ghe": 2,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-b4",
                "loai_ghe": 2,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-b5",
                "loai_ghe": 2,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-b6",
                "loai_ghe": 2,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-b7",
                "loai_ghe": 2,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-b8",
                "loai_ghe": 2,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-b9",
                "loai_ghe": 2,
                "chiec_may_bay": 2
            },
            {
                "ten_ghe": "2k8g-b10",
                "loai_ghe": 2,
                "chiec_may_bay": 2
            },

        ]
        tao_ghe_asmr = [
            {
                "ten_ghe": "asmr-a1",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-a2",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-a3",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-a4",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-a5",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-a6",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-a7",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-a8",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-a9",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-a10",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-b1",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-b2",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-b3",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-b4",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-b5",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-b6",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-b7",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-b8",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-b9",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-b10",
                "loai_ghe": 1,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-c1",
                "loai_ghe": 2,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-c2",
                "loai_ghe": 2,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-c3",
                "loai_ghe": 2,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-c4",
                "loai_ghe": 2,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-c5",
                "loai_ghe": 2,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-c6",
                "loai_ghe": 2,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-c7",
                "loai_ghe": 2,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-c8",
                "loai_ghe": 2,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-c9",
                "loai_ghe": 2,
                "chiec_may_bay": 3
            },
            {
                "ten_ghe": "asmr-c10",
                "loai_ghe": 2,
                "chiec_may_bay": 3
            },

        ]
        tao_ghe_w200 = [
            {
                "ten_ghe": "w200-a1",
                "loai_ghe": 1,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-a2",
                "loai_ghe": 1,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-a3",
                "loai_ghe": 1,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-a4",
                "loai_ghe": 1,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-a5",
                "loai_ghe": 1,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-a6",
                "loai_ghe": 1,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-a7",
                "loai_ghe": 1,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-a8",
                "loai_ghe": 1,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-a9",
                "loai_ghe": 1,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-a10",
                "loai_ghe": 1,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-b1",
                "loai_ghe": 1,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-b2",
                "loai_ghe": 1,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-b3",
                "loai_ghe": 1,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-b4",
                "loai_ghe": 1,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-b5",
                "loai_ghe": 1,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-b6",
                "loai_ghe": 2,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-b7",
                "loai_ghe": 2,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-b8",
                "loai_ghe": 2,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-b9",
                "loai_ghe": 2,
                "chiec_may_bay":4
            },
            {
                "ten_ghe": "w200-b10",
                "loai_ghe": 2,
                "chiec_may_bay":4
            },

        ]
        for t in tao_ghe_xp1:
            ghe = Ghe(ten_ghe=t['ten_ghe'], loai_ghe=t['loai_ghe'],
                      Chiec_may_bay_id=t['chiec_may_bay'])
            db.session.add(ghe)
        for t in tao_ghe_2k8g:
            ghe = Ghe(ten_ghe=t['ten_ghe'], loai_ghe=t['loai_ghe'],
                      Chiec_may_bay_id=t['chiec_may_bay'])
            db.session.add(ghe)
        for t in tao_ghe_asmr:
            ghe = Ghe(ten_ghe=t['ten_ghe'], loai_ghe=t['loai_ghe'],
                      Chiec_may_bay_id=t['chiec_may_bay'])
            db.session.add(ghe)
        for t in tao_ghe_w200:
            ghe = Ghe(ten_ghe=t['ten_ghe'], loai_ghe=t['loai_ghe'],
                      Chiec_may_bay_id=t['chiec_may_bay'])
            db.session.add(ghe)
        db.session.commit()
        tao_chuyen_bay = [{

        }]
        tao_ve = [
            {
                "gia_ve": 2500000,
                "hang_ve": 1,
                "chuyen_bay_id": 1,
                "ngay_di": 1,
                "lich_bay": 1
            },
            {
                "gia_ve": 2500000,
                "hang_ve": 1,
                "chuyen_bay_id": 1,
                "ngay_di": 1,
                "lich_bay": 1
            },
            {
                "gia_ve": 2500000,
                "hang_ve": 1,
                "chuyen_bay_id": 1,
                "ngay_di": 1,
                "lich_bay": 1
            },
            {
                "gia_ve": 2500000,
                "hang_ve": 1,
                "chuyen_bay_id": 1,
                "ngay_di": 1,
                "lich_bay": 1
            },
            {
                "gia_ve": 2500000,
                "hang_ve": 1,
                "chuyen_bay_id": 1,
                "ngay_di": 1,
                "lich_bay": 1
            },
            {
                "gia_ve": 2500000,
                "hang_ve": 1,
                "chuyen_bay_id": 1,
                "ngay_di": 1,
                "lich_bay": 1
            },
            {
                "gia_ve": 2500000,
                "hang_ve": 1,
                "chuyen_bay_id": 1,
                "ngay_di": 1,
                "lich_bay": 1
            },
            {
                "gia_ve": 2500000,
                "hang_ve": 1,
                "chuyen_bay_id": 1,
                "ngay_di": 1,
                "lich_bay": 1
            },
            {
                "gia_ve": 2500000,
                "hang_ve": 1,
                "chuyen_bay_id": 1,
                "ngay_di": 1,
                "lich_bay": 1
            },
            {
                "gia_ve": 3000000,
                "hang_ve": 2,
                "chuyen_bay_id": 1,
                "ngay_di": 1,
                "lich_bay": 1
            },
            {
                "gia_ve": 3000000,
                "hang_ve": 2,
                "chuyen_bay_id": 1,
                "ngay_di": 1,
                "lich_bay": 1
            },
            {
                "gia_ve": 3000000,
                "hang_ve": 2,
                "chuyen_bay_id": 1,
                "ngay_di": 1,
                "lich_bay": 1
            },
            {
                "gia_ve": 3000000,
                "hang_ve": 2,
                "chuyen_bay_id": 1,
                "ngay_di": 1,
                "lich_bay": 1
            },
            {
                "gia_ve": 3000000,
                "hang_ve": 2,
                "chuyen_bay_id": 1,
                "ngay_di": 1,
                "lich_bay": 1
            },
        ]
        tao_ve_2 = [
            {
                "gia_ve": 4500000,
                "hang_ve": 1,
                "chuyen_bay_id": 2,
                "ngay_di": 2,
                "lich_bay": 2
            },
            {
                "gia_ve": 4500000,
                "hang_ve": 1,
                "chuyen_bay_id": 2,
                "ngay_di": 2,
                "lich_bay": 2
            },
            {
                "gia_ve": 4500000,
                "hang_ve": 1,
                "chuyen_bay_id": 2,
                "ngay_di": 2,
                "lich_bay": 2
            },
            {
                "gia_ve": 4500000,
                "hang_ve": 1,
                "chuyen_bay_id": 2,
                "ngay_di": 2,
                "lich_bay": 2
            },
            {
                "gia_ve": 4500000,
                "hang_ve": 1,
                "chuyen_bay_id": 2,
                "ngay_di": 2,
                "lich_bay": 2
            },
            {
                "gia_ve": 4500000,
                "hang_ve": 1,
                "chuyen_bay_id": 2,
                "ngay_di": 2,
                "lich_bay": 2
            },
            {
                "gia_ve": 4500000,
                "hang_ve": 1,
                "chuyen_bay_id": 2,
                "ngay_di": 2,
                "lich_bay": 2
            },
            {
                "gia_ve": 4500000,
                "hang_ve": 1,
                "chuyen_bay_id": 2,
                "ngay_di": 2,
                "lich_bay": 2
            },
            {
                "gia_ve": 4500000,
                "hang_ve": 1,
                "chuyen_bay_id": 2,
                "ngay_di": 2,
                "lich_bay": 2
            },
            {
                "gia_ve": 6000000,
                "hang_ve": 2,
                "chuyen_bay_id": 2,
                "ngay_di": 2,
                "lich_bay": 2
            },
            {
                "gia_ve": 6000000,
                "hang_ve": 2,
                "chuyen_bay_id": 2,
                "ngay_di": 2,
                "lich_bay": 2
            },
            {
                "gia_ve": 6000000,
                "hang_ve": 2,
                "chuyen_bay_id": 2,
                "ngay_di": 2,
                "lich_bay": 2
            },
            {
                "gia_ve": 6000000,
                "hang_ve": 2,
                "chuyen_bay_id": 2,
                "ngay_di": 2,
                "lich_bay": 2
            },
            {
                "gia_ve": 6000000,
                "hang_ve": 2,
                "chuyen_bay_id": 2,
                "ngay_di": 2,
                "lich_bay": 2
            },
        ]
        tao_ve_3 = [
            {
                "gia_ve": 1200000,
                "hang_ve": 1,
                "chuyen_bay_id": 3,
                "ngay_di": 3
            },
            {
                "gia_ve": 1200000,
                "hang_ve": 1,
                "chuyen_bay_id": 3,
                "ngay_di": 3
            },
            {
                "gia_ve": 1200000,
                "hang_ve": 1,
                "chuyen_bay_id": 3,
                "ngay_di": 3
            },
            {
                "gia_ve": 1200000,
                "hang_ve": 1,
                "chuyen_bay_id": 3,
                "ngay_di": 3
            },
            {
                "gia_ve": 1200000,
                "hang_ve": 1,
                "chuyen_bay_id": 3,
                "ngay_di": 3
            },
            {
                "gia_ve": 1200000,
                "hang_ve": 1,
                "chuyen_bay_id": 3,
                "ngay_di": 3
            },
            {
                "gia_ve": 1200000,
                "hang_ve": 1,
                "chuyen_bay_id": 3,
                "ngay_di": 3
            },
            {
                "gia_ve": 1200000,
                "hang_ve": 1,
                "chuyen_bay_id": 3,
                "ngay_di": 3
            },
            {
                "gia_ve": 1200000,
                "hang_ve": 1,
                "chuyen_bay_id": 3,
                "ngay_di": 3
            },
            {
                "gia_ve": 3600000,
                "hang_ve": 2,
                "chuyen_bay_id": 3,
                "ngay_di": 3
            },
            {
                "gia_ve": 3600000,
                "hang_ve": 2,
                "chuyen_bay_id": 3,
                "ngay_di": 3
            },
            {
                "gia_ve": 3600000,
                "hang_ve": 2,
                "chuyen_bay_id": 3,
                "ngay_di": 3
            },
            {
                "gia_ve": 3600000,
                "hang_ve": 2,
                "chuyen_bay_id": 3,
                "ngay_di": 3
            },
            {
                "gia_ve": 3600000,
                "hang_ve": 2,
                "chuyen_bay_id": 3,
                "ngay_di": 3
            },
        ]
        for t in tao_ve:
            ve = Ve_may_bay(gia_tien=t['gia_ve'], hang_ve=t['hang_ve'],
                            chuyen_bay_id=t['chuyen_bay_id'], lich_bay_id=t['ngay_di'])
            db.session.add(ve)
        for t in tao_ve_2:
            ve = Ve_may_bay(gia_tien=t['gia_ve'], hang_ve=t['hang_ve'],
                            chuyen_bay_id=t['chuyen_bay_id'], lich_bay_id=t['ngay_di'])
            db.session.add(ve)
        for t in tao_ve_3:
            ve = Ve_may_bay(gia_tien=t['gia_ve'], hang_ve=t['hang_ve'],
                            chuyen_bay_id=t['chuyen_bay_id'], lich_bay_id=t['ngay_di'])
            db.session.add(ve)
        db.session.commit()

