import requests

# URL của API
url = 'https://qldtbeta.phenikaa-uni.edu.vn/sinhvienapi/api/SV_ThongTin/LayDSLichCaNhan?action=SV_ThongTin%2FLayDSLichCaNhan&type=GET&strQLSV_NguoiHoc_Id=175B3C1FD8354B3087AE9EE11DAD6AAF&strNgayBatDau=15%2F07%2F2024&strNgayKetThuc=21%2F07%2F2024&strChucNang_Id=B46109CD333D4E3DAC50D43E8607ED46&strNguoiThucHien_Id=175B3C1FD8354B3087AE9EE11DAD6AAF&_=1721268997629'

# Headers của yêu cầu
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',  # Thay YOUR_ACCESS_TOKEN bằng token của bạn
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Gửi yêu cầu GET
response = requests.get(url, headers=headers)

# Kiểm tra phản hồi
if response.status_code == 200:
    print('Yêu cầu thành công!')
    data = response.json()
    # In dữ liệu lịch cá nhân
    for item in data.get('Data', []):
        print(f"ID: {item.get('ID')}, IDLICHHOC: {item.get('IDLICHHOC')}, ...")
else:
    print('Yêu cầu thất bại!')
    print('Mã lỗi:', response.status_code)
    print('Nội dung:', response.text)
