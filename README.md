
# Danh mục Chứng quyền có đảm bảo (CW) theo mô hình Black-Scholes, bao gồm:

---

# 📌 I. Giới thiệu nhanh

✅ **Covered Warrant là gì?**

Là chứng khoán do CTCK phát hành, cho phép người nắm giữ mua (Call CW) hoặc bán (Put CW) cổ phiếu cơ sở với giá xác định trong tương lai. Cần định giá hợp lý để tránh mua quá đắt/thiếu định giá.

---

# 📌 II. Mô hình định giá Black-Scholes (cho CW kiểu Châu Âu)

✅ **Công thức Black-Scholes:**

- Với CW mua (Call):

C = S · N(d₁) − K · e^(−rT) · N(d₂)

- Với CW bán (Put):

P = K · e^(−rT) · N(−d₂) − S · N(−d₁)

Trong đó:

d₁ = [ln(S/K) + (r + σ²/2) · T] / (σ · √T)  
d₂ = d₁ − σ · √T

---

### **Giải thích các biến:**

- S: Giá cổ phiếu hiện tại  
- K: Giá thực hiện  
- T: Thời gian đến ngày đáo hạn (tính theo năm)  
- r: Lãi suất phi rủi ro  
- σ: Độ biến động (volatility) của cổ phiếu  
- N(d): Hàm phân phối chuẩn tích lũy (CDF)

---

# 📌 III. Các hệ số nhạy cảm (Greek Letters)

✅ **Delta** – Đo độ nhạy của giá CW với giá tài sản cơ sở:

Delta = N(d₁) (Call), −N(−d₁) (Put)

✅ **Gamma** – Đo độ thay đổi của Delta:

Gamma = e^(−d₁² / 2) / [√(2π) · S · σ · √T]

---

# 📌 IV. Mở rộng với đặc điểm của CW tại Việt Nam

Tại Việt Nam, CW có những đặc điểm như:

- Tỷ lệ chuyển đổi (conversion ratio) không phải 1:1  
- Hiệu ứng pha loãng không tồn tại như quyền chọn thực  
- Giới hạn giá nên cần điều chỉnh giá lý thuyết:

Giá lý thuyết CW = (C · R) / (Tỷ lệ chuyển đổi)

Trong đó:  
- C là giá quyền theo mô hình Black-Scholes  
- R là hệ số điều chỉnh hoặc chiết khấu từ tổ chức phát hành
-----------------------------
PHẦN 2

📊 1. Ý nghĩa các chỉ số

Chỉ số	Giải thích
Return	Tỷ suất sinh lời cổ phiếu trong 5 phiên gần nhất
Risk	Độ biến động giá (Standard Deviation – càng cao, càng biến động mạnh)
Score	Điểm tổng hợp (kết hợp Return, CW change, Stability), dùng để xếp hạng

🔍 2. Phân tích điểm nổi bật

Mã	Return	Risk	Nhận xét
VI	+8.86%	0.98	Return cao nhất 🔥 nhưng Risk cũng cao nhất. Rủi ro lớn.
BI, SAB	-4.7%, -2.5%	0.08 - 0.12	Dù âm nhẹ nhưng ổn định, Risk thấp ✅
VC, GAS	-6.3%, -7.5%	0.48 - 0.65	Risk cao → biến động mạnh, nhiều rủi ro
HP	-10.6%	0.08	Lỗ nặng nhưng ổn định bất ngờ. Có thể do mất niềm tin từ thị trường

⚠️ 3. Ý nghĩa Risk

Risk thấp (0.05 – 0.2): Cổ phiếu ổn định, phù hợp đầu tư CW an toàn hoặc bán quyền
Risk trung bình (0.2 – 0.5): Cân nhắc tùy khẩu vị rủi ro
Risk cao (0.5 – 1.0): Biến động lớn, thích hợp cho CW ngắn hạn hoặc lướt sóng

✅ 4. Nên đầu tư CW cổ phiếu nào?

Nên cân nhắc đầu tư	Vì sao?
SA	Return gần 0, rủi ro thấp, phù hợp nếu CW có giá rẻ hoặc tỷ lệ đòn bẩy tốt
BI	Ổn định nhất, score cao, tốt cho chiến lược phòng thủ
VI	Lợi nhuận cao, nhưng cần stop-loss rõ ràng vì Risk rất lớn
VN	Trung tính, phù hợp đầu tư ngắn hạn nếu CW đang chiết khấu
