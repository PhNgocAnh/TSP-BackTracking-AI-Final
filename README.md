# 🧭 Giải bài toán TSP bằng Thuật toán Quay lui (Backtracking)

**TSP (Travelling Salesman Problem)**  
> Một người bán hàng cần đi qua tất cả các thành phố đúng một lần,  
> rồi quay trở lại điểm xuất phát, sao cho tổng chi phí di chuyển là nhỏ nhất.

**Thuật toán Quay lui (Backtracking)**  
> Giải quyết vấn đề bằng cách thử lần lượt các tùy chọn khác nhau.  
> Nếu một tùy chọn không mang lại hiệu quả hoặc dẫn đến ngõ cụt,  
> giải thuật sẽ quay lại lựa chọn trước đó và thử một tùy chọn khác  
> cho đến khi tìm thấy giải pháp hoặc tất cả các khả năng đã được sử dụng hết.

---

## 📐 Mô hình bài toán TSP

- **Đầu vào**:
  - Ma trận khoảng cách `n x n` giữa các thành phố.
- **Yêu cầu**:
  - Tìm chu trình Hamiltonian với tổng chi phí nhỏ nhất.
- **Giả định**:
  - Đồ thị đầy đủ, tức là giữa mỗi cặp thành phố đều có một cạnh trực tiếp với một trọng số nhất định (khoảng cách), để tất cả các thành phố đều có kết nối với nhau.

---

## 🔍 Ý tưởng thuật toán

1. **Bắt đầu** từ thành phố đầu tiên (thành phố số `0`).
2. **Dùng đệ quy** để thử lần lượt các thành phố kế tiếp **chưa được thăm**:
   - Đánh dấu thành phố hiện tại là đã thăm.
   - Tính chi phí tạm thời của đường đi.
   - Tiếp tục thử các thành phố tiếp theo.
3. Khi đã đi qua **tất cả các thành phố**:
   - Kiểm tra xem có thể **quay lại thành phố đầu tiên** không.
   - Tính tổng chi phí chu trình.
   - Nếu chu trình hợp lệ và có chi phí **thấp hơn hiện tại**, thì cập nhật kết quả.
4. **Backtrack**: Quay lui để thử đường đi khác (bỏ đánh dấu thành phố vừa thăm).
5. **Giới hạn thời gian**: Nếu thời gian thực thi vượt quá `time_limit`, thuật toán sẽ dừng để tránh treo máy.

## 📥 Cách cài đặt

1. **Tải mã nguồn** và **giải nén** vào thư mục bất kỳ trên máy của bạn.
2. Mở thư mục bằng Visual Studio Code
3. **Chạy file `main.py`** để khởi động ứng dụng:

## 📝 Ghi chú
- Thư mục `testcase` chứa các file thử nghiệm của nhóm.


