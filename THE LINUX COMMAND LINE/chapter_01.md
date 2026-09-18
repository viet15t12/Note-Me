# Chương 01: WHAT IS THE SHELL

## Tóm tắt nhanh

- Môi trường dòng lệnh ở linux gọi là `Shell`.
- `Shell` là chương trình nhận command từ keyboard hoặc script, sau đó yêu cầu OS (kernel) thực thi và trả kết quả về cho người dùng.
- Chương trình `Shell` mặc định của hầu hết các linux distro là **Bash**

## Khái niệm chính

### Terminal Emulators

- **Terminal Emulator** là program chạy trên GUI giả lập Terminal, giúp người dùng có thể giao tiếp với `Shell` khi sử dụng giao diện GUI.

```shell
Người dùng → Terminal Emulator → Shell → Kernel (OS)
```

- Có nhiều chương trình **Terminal Emulator** khác nhau, cung cấp các tính năng khác nhau.

### Shell Prompt

đây là shell Prompt `[me@linuxbox ~]$`

- Đây là chuỗi ký tự shell hiển thị ra để báo Shell đã sẵn sàng nhận lệnh.
- Cấu trúc Shell Prompt bắt đầu bằng tên user đang đăng nhập + @ + tên máy (hostname) + thư mục hiện tại, sau đó là ký tự thể hiện quyền user.
  - `$` là quyền user thường
  - `#` là quyền user quản trị, quyền `ROOT`

khi truyền 1 lệnh vô nghĩa vào `Shell`, nó sẽ báo cho ta biết và cho phép nhập lệnh lại

- **EX**

```shell
    [me@linuxbox ~]$ kaekfjaeifj
    bash: kaekfjaeifj: command not found
    [me@linuxbox ~]$
```

### Một số lệnh cơ bản

- `date` — hiển thị ngày giờ hiện tại của hệ thống.

```shell
  [me@linuxbox ~]$ date
```

- `uptime` — hiển thị hệ thống đã chạy (uptime) bao lâu, số user đang đăng nhập, và load average (số tiến trình trung bình đang chờ xử lý trong các khoảng thời gian gần đây).

```shell
  [me@linuxbox ~]$ uptime
```

- `df` — hiển thị dung lượng đĩa còn trống trên các phân vùng (filesystem).

```shell
  [me@linuxbox ~]$ df
```

- `free` — hiển thị dung lượng RAM còn trống/đã dùng.

```shell
  [me@linuxbox ~]$ free
```

### Virtual Terminal / Virtual Console

- Ngay cả khi không mở terminal emulator nào, hệ thống vẫn có sẵn nhiều phiên terminal chạy ngầm phía sau giao diện đồ họa — gọi là **virtual terminal/console**.
- Truy cập bằng `CTRL-ALT-F1` → `F6` (tùy distro), chuyển qua lại bằng `ALT-F1` → `F6`.
- Quay lại giao diện đồ họa thường bằng `ALT-F7`.

## Kết thúc phiên Terminal

Có 3 cách:

1. Đóng cửa sổ terminal emulator.
2. Gõ lệnh `exit` tại shell prompt.
3. Nhấn `CTRL-D`.

```shell
[me@linuxbox ~]$ exit
```

## Tổng kết chương

- Shell là lớp trung gian giữa người dùng và kernel (OS), nhận lệnh và trả kết quả theo cơ chế **REPL** (Read - Eval - Print - Loop).
- Terminal Emulator chỉ đóng vai trò hiển thị (I/O), không tự hiểu lệnh — việc parse và thực thi lệnh là do Shell đảm nhiệm.
- Shell Prompt (`[me@linuxbox ~]$`) là dấu hiệu cho biết Shell đang chờ input, đồng thời tiết lộ 3 thông tin: user đang đăng nhập, hostname, và quyền hạn hiện tại (`$` thường / `#` root).
- Đã biết dùng một số lệnh cơ bản để lấy thông tin hệ thống: `date`, `uptime`, `df`, `free`.
- Biết cách thoát một phiên terminal bằng 3 cách khác nhau.

