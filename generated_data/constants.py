ROOM_NAMES = [
    "Phòng Khám 01", "Phòng Khám 02", "Phòng Khám 03", "Phòng Khám 04", "Phòng Cấp cứu", "Phòng Tiểu phẫu", "Phòng Đại phẫu", "Phòng Hồi sức", "Phòng Hậu phẫu",
    "Phòng Điều trị 101", "Phòng Điều trị 102", "Phòng Điều trị 103", "Phòng Điều trị 201", "Phòng Điều trị 202", "Phòng Điều trị 203", "Phòng Điều trị 301", "Phòng Điều trị 302", "Phòng Điều trị 303",
    "Phòng Theo dõi", "Phòng Cách ly", "Phòng Thủ thuật", "Phòng Nội soi", "Phòng Siêu âm", "Phòng X-quang", "Phòng CT", "Phòng MRI", "Phòng Lấy mẫu", "Phòng Hóa trị", "Phòng Xạ trị",
    "Phòng Truyền dịch", "Phòng Chăm sóc đặc biệt", "Phòng Chăm sóc giảm nhẹ", "Phòng Tư vấn", "Phòng Hội chẩn", "Phòng Đợi", "Phòng Hành chính", "Phòng Điều dưỡng", "Phòng Trực bác sĩ", "Phòng Trực điều dưỡng",
    "Phòng Vật tư", "Phòng Dược", "Phòng Thanh toán", "Phòng Bảo hiểm", "Phòng Lưu bệnh án", "Phòng Kỹ thuật",
]

CHAMBER_NAMES = [
    # Buồng điều trị nội trú
    "Buồng 01-101", "Buồng 02-102", "Buồng 03-103", "Buồng 04-104", "Buồng 05-105", "Buồng 06-106", "Buồng 07-107", "Buồng điều trị ngoại trú", "Buồng điều trị cách ly COVID",
    # Buồng mổ / hậu phẫu
    "Buồng mổ A", "Buồng mổ B", "Buồng mổ C", "Buồng mổ D", "Buồng mổ YC", "Chờ mổ", "Hậu phẫu 1", "Hậu phẫu 2", "Hậu phẫu 3", "Hồi tỉnh", "Hồi sức tích cực 1", "Cấp cứu",
    # Buồng cách ly
    "Cách ly 1",
    "Cách ly 2",
    "Cách ly 3",
    # Buồng theo chuyên khoa
    "Buồng Hóa trị", "Buồng Xạ trị", "Buồng Chăm sóc giảm nhẹ", "Buồng Nội khoa", "Buồng Ngoại khoa", "Buồng Ung bướu", "Buồng Huyết học", "Buồng Miễn dịch", "Buồng Hóa sinh", "Buồng Nội tiết", "Buồng Tim mạch", "Buồng Hô hấp", "Buồng Tiêu hóa", "Buồng Thần kinh", "Buồng Thận nhân tạo",
    # Khu thuốc
    "Kho thuốc viên", "Kho thuốc ống", "Kho thuốc hướng thần", "Kho thuốc gây nghiện", "Kho thuốc ung thư", "Kho thuốc YHHN", "Kho thuốc Corticoid", "Kho thuốc phóng xạ", "Kho thuốc bảo quản lạnh", "Kho sinh phẩm", "Kho dịch truyền", "Kho thuốc thử nghiệm lâm sàng",
    # Khu xét nghiệm
    "Khu Hóa sinh",
    "Khu Huyết học",
    "Khu Miễn dịch",
    "Khu Nước tiểu",
    # Khu nghiên cứu
    "Lưu TNLS FLAURA2",
    "Lưu TNLS AEGEAN",
    "Phòng lưu nhà thuốc",
    # Mã buồng thực tế
    "B1","BCL01","BCL02","BCL03","BCL04","BCL05","BCL06","BCL07","BCL08","BCL09","BCL10","BLC11","NTBN",
    # Phòng đánh số
    "201","202","203","204","205","206","207","208","209","210","211","212","215","216","217","218","219","220","221","222","223","224","225","301","302","303","304","305","306","307","308","309","310","311","315","316","317","318","319","320","321","322","323","324","325","400","400A","401","402","403","404","405","406","407","408","409","410","411","412","413","414","415","416","417","418","419","420","421","422","423","424","425",
    "501","502","503","504","505","506","507","508","509","510","511","512","513","514","515","516","517","518","519","520","521","522","523","524","525","603","604","605","606","607","608","609","610","611","615","616","617",
]

SERVICE_NAMES = ["Khối hồng cầu từ 250 ml máu toàn phần", "Khối hồng cầu từ 350 ml máu toàn phần", "Khối hồng cầu lọc bạch cầu",
                 "Khối hồng cầu rửa", "Khối tiểu cầu 4 đơn vị", "Khối tiểu cầu gạn tách", "Huyết tương tươi đông lạnh 200 ml",
                 "Huyết tương tươi đông lạnh 250 ml", "Tủa lạnh", "Bạch cầu hạt", "Máu toàn phần", "Điều chế khối tiểu cầu gạn tách 120 ml",
                 "Điều chế khối tiểu cầu gạn tách 250 ml", "Truyền khối hồng cầu", "Truyền huyết tương", "Truyền tiểu cầu",
                 "Khám chuyên khoa Ung bướu", "Khám Nội tổng quát", "Khám Ngoại tổng quát", "Khám gây mê trước mổ", "Khám dinh dưỡng",
                 "Tư vấn điều trị hóa chất", "Tư vấn xạ trị", "Chụp X-quang ngực", "Chụp CT ngực", "Chụp CT bụng", "Chụp MRI sọ não",
                 "Siêu âm ổ bụng", "Siêu âm tuyến giáp", "Điện tim", "Nội soi dạ dày", "Nội soi đại tràng", "Xét nghiệm công thức máu",
                 "Xét nghiệm sinh hóa máu", "Xét nghiệm đông máu", "Xét nghiệm CRP", "Xét nghiệm HbA1c", "Định lượng AFP", "Định lượng CEA",
                 "Định lượng CA 19-9", "Định lượng CA 15-3", "Định lượng CA 125", "Định lượng PSA", "Giải phẫu bệnh", "Hóa mô miễn dịch",
                 "Sinh thiết kim", "Sinh thiết mở", "Chọc hút tế bào", "Hóa trị chu kỳ", "Xạ trị ngoài", "Xạ trị áp sát", "Điều trị miễn dịch",
                 "Điều trị nhắm trúng đích", "Truyền dịch", "Tiêm tĩnh mạch", "Tiêm bắp", "Thay băng vết mổ", "Chăm sóc PICC",
                 "Đặt catheter tĩnh mạch trung tâm", "Đặt sonde dạ dày", "Đặt sonde tiểu", "Thở oxy", "Theo dõi sau mổ", "Theo dõi hóa trị",
                 "Theo dõi xạ trị", "Phẫu thuật cắt u", "Phẫu thuật sinh thiết", "Phẫu thuật nội soi", "Gây mê nội khí quản", "Gây tê tủy sống",
                 "Chăm sóc giảm nhẹ", "Tư vấn tâm lý", "Vận chuyển người bệnh", "Cấp cứu nội viện", "Khám tái khám", "Khám theo yêu cầu"]

DEPARTMENT_NAMES = [
    "Đơn Vị Nghiên Cứu Lâm Sàng",
    "Khoa Khám bệnh",
    "Khoa Khám bệnh theo yêu cầu",
    "Phòng Cấp Cứu",
    "ĐN Cách ly và điều trị người bệnh Covid-19",
    "ĐN Điều trị cách ly",
    "Khoa Dinh dưỡng",
    "Khoa Y học hạt nhân",
    "Khoa Gây Mê",
    "Khoa Gây mê hồi sức",
    "Khoa Giải phẫu bệnh - Tế bào",
    "Khoa Xét nghiệm",
    "Khoa Chẩn đoán hình ảnh",
    "Ban Giám Đốc",
    "Ban Quản lý tòa nhà",
    "Chăm sóc viên",
    "Khoa Dược",
    "Khoa Kiểm soát nhiễm khuẩn",
    "Khoa Vật lý xạ trị",
    "Phòng Chỉ đạo tuyến",
    "Phòng Công nghệ thông tin",
    "Phòng Điều dưỡng",
    "Phòng Hành chính quản trị",
    "Phòng Hợp tác quốc tế & Nghiên cứu khoa học",
    "Phòng Kế hoạch tổng hợp",
    "Phòng Quản lý chất lượng và Công tác xã hội",
    "Phòng Tài chính kế toán",
    "Phòng Tổ chức cán bộ - BV",
    "Phòng Vật tư thiết bị y tế",
    "Khoa Nội soi - Thăm dò chức năng",
    "Khoa Nội tổng hợp",
    "Khoa Nội Tiêu hóa theo yêu cầu",
    "Khoa Nội vú phụ khoa đầu cổ theo yêu cầu",
    "Khoa Nội Tổng hợp điều trị ban ngày theo yêu cầu",
    "Khoa Nội phổi - vú",
    "Khoa Nội Tổng hợp theo yêu cầu",
    "Khoa Ngoại theo yêu cầu",
    "Khoa Xạ trị",
    "Xạ trị ngoại trú 1",
    "Xạ trị ngoại trú 2",
    "Ngoại Tổng hợp",
    "Ngoại Đầu cổ",
    "Khoa Xạ trị yêu cầu",
    "Khoa Chăm sóc giảm nhẹ",
    "Ngoại Vú-phụ khoa",
]

ROOM_SUFFIXES = ["01", "02", "03", "A", "B", "Khu A", "Khu B"]

ICD10_CODES = [
    "C00.0", "C01", "C02.9", "C04.9", "C06.9",
    "C09.9", "C11.9", "C15.9", "C16.9", "C18.9",
    "C20", "C22.0", "C25.9", "C32.9", "C34.9",
    "C43.9", "C50.9", "C53.9", "C54.1", "C56",
    "C61", "C64", "C67.9", "C71.9", "C73",
    "C76.0", "C77.9", "C78.0", "C79.5", "C80.9",
    "D00.0", "D05.1", "D06.9", "D10.9", "D12.6",
    "D24", "D32.9", "D36.0", "D37", "D38.1",
    "D39.7", "D44.0", "I10", "I21.9", "I25.1",
    "I50.9", "J18.9", "J44.9", "K25.9", "K35.8",
    "K40.9", "K52.9", "K74.6", "K92.2", "M17.9",
    "N18.5", "N20.0", "N39.0", "R50.9", "R59.9"
]

ICD10_NAMES = [
    "Ung môi", "Ung lưỡi", "Ung lưỡi không đặc hiệu", "Ung sàn miệng", "Ung miệng", "Ung amidan", "Ung vòm họng", "Ung thực quản", "Ung dạ dày", "Ung đại tràng", "Ung trực tràng", "Ung gan nguyên phát", "Ung tụy", "Ung thanh quản", "Ung phổi", "U hắc tố ác tính", "Ung vú",
    "Ung cổ tử cung", "Ung nội mạc tử cung", "Ung buồng trứng", "Ung tuyến tiền liệt", "Ung thận", "Ung bàng quang", "Ung não", "Ung tuyến giáp", "Ung đầu mặt cổ", "Di căn hạch", "Di căn phổi", "Di căn xương", "Ung thư chưa xác định",
    "Carcinoma tại chỗ môi", "Carcinoma tại chỗ vú",
    "Carcinoma tại chỗ cổ tử cung", "U lành tuyến nước bọt", "Polyp đại tràng", "U lành vú", "U lành màng não", "U lành mô liên kết", "Khối u chưa rõ tính chất", "Khối u trung thất", "Khối u cơ quan sinh dục nữ", "U tuyến giáp",
    "Tăng huyết áp", "Nhồi máu cơ tim cấp", "Bệnh tim thiếu máu cục bộ", "Suy tim", "Viêm phổi", "Bệnh phổi tắc nghẽn mạn tính", "Loét dạ dày", "Viêm ruột thừa cấp", "Thoát vị bẹn", "Viêm đại tràng", "Xơ gan", "Xuất huyết tiêu hóa",
    "Thoái hóa khớp gối", "Suy thận mạn giai đoạn cuối", "Sỏi thận", "Nhiễm trùng đường tiết niệu", "Sốt không rõ nguyên nhân", "Hạch to"
]

DOCUMENT_TYPES = [
    "Giấy ra viện",
    "Đơn thuốc ngoại trú",
    "Phiếu điều trị",
    "Phiếu chăm sóc",
    "Phiếu truyền dịch",
    "Phiếu xét nghiệm",
    "Phiếu hóa trị",
    "Phiếu xạ trị",
    "Biên bản hội chẩn",
    "Phiếu phẫu thuật",
    "Phiếu thủ thuật",
    "Giấy cam kết điều trị",
    "Giấy chỉ định",
    "Phiếu theo dõi dấu hiệu sinh tồn",
    "Phiếu dinh dưỡng",
]

SIGN_ROLES = [
    "Bác sĩ điều trị",
    "Trưởng khoa",
    "Điều dưỡng",
    "Người lập phiếu",
    "Kế toán",
    "Dược sĩ",
]

SIGN_STATUSES = ["Chưa ký", "Đã ký", "Từ chối ký", "Đã hủy"]

CARE_LEVELS = ["Chăm sóc cấp I", "Chăm sóc cấp II", "Chăm sóc cấp III", "Chăm sóc đặc biệt", "Theo dõi sau mổ", "Theo dõi tích cực", "Chăm sóc giảm nhẹ", "Chăm sóc toàn diện"]

HOSPITAL_NAMES = [
    "Bệnh viện Bạch Mai",
    "Bệnh viện Hữu nghị Việt Đức",
    "Bệnh viện K",
    "Bệnh viện Chợ Rẫy",
    "Bệnh viện Đại học Y Hà Nội",]

# Bootstrap Server
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

# Auto create topics (nếu broker cho phép)
KAFKA_AUTO_CREATE_TOPICS = True

# Topic tương ứng với từng bảng
KAFKA_TOPICS = {
    "tb_dm_benhvien": "tb_dm_benhvien",
    "tb_department": "tb_department",
    "tb_room": "tb_room",
    "tb_chamber": "tb_chamber",
    "tb_nhanvien": "tb_nhanvien",
    "tb_dm_icd10": "tb_dm_icd10",
    "tb_dm_servicesubgroup": "tb_dm_servicesubgroup",
    "tb_service": "tb_service",
    "tb_medicalrecord": "tb_medicalrecord",
    "tb_medicalrecord_khambenh": "tb_medicalrecord_khambenh",
    "tb_treatment": "tb_treatment",
    "tb_servicedata_pttt": "tb_servicedata_pttt",
    "tb_mediboxdocument": "tb_mediboxdocument",
    "tb_mediboxdocument_sign": "tb_mediboxdocument_sign",
    "tb_nhanvienactivity": "tb_nhanvienactivity",}