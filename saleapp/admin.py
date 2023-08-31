from saleapp import app, db, admin
from flask_admin.contrib.sqla import ModelView
from saleapp.models import *

admin.add_view(ModelView(Chuyen_bay, db.session, name="Chuyến bay"))
admin.add_view(ModelView(Tuyen_bay, db.session, name="Tuyến bay"))
admin.add_view(ModelView(May_bay, db.session, name="Máy bay"))
admin.add_view(ModelView(Hoa_don, db.session, name= "Hóa đơn"))
admin.add_view(ModelView(Nguoi_dung, db.session, name="Người dùng"))
admin.add_view(ModelView(Ve_may_bay, db.session, name="Vé"))
admin.add_view(ModelView(Lich_bay, db.session, name="Lịch bay"))
admin.add_view(ModelView(Ghe, db.session, name="Ghế"))
admin.add_view(ModelView(San_bay, db.session, name="Sân bay"))
admin.add_view(ModelView(San_bay_trung_gian, db.session, name="Sân bay trung gian"))
