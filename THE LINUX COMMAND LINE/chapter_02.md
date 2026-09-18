# Chương 02: NAVIGATION(Điều hướng)

## Tóm tắt nhanh

Học cách di chuyển/điều hướng qua lại giữa các thư mục là kỹ năng cơ bản đầu tiên cần nắm.

3 lệnh nền tảng cần học:

- `pwd`: Kiểm tra xem bạn đang đứng ở thư mục nào.

- `cd` : Chuyển sang thư mục khác.

- `ls` : Xem trong thư mục hiện tại có những tệp/thư mục nào.

## Khái niệm chính

### Filesystem Tree

Hệ điều hành Linux được tổ chức thư mục theo kiểu phân cấp, nhưng khác với Windows, mọi thư mục trong hệ thống đều là thư mục con dưới cấp của một thư mục chung, dù hệ thống có bao nhiêu ổ đĩa đi nữa. Thư mục chung đó gọi là ROOT (/). Các thiết bị lưu trữ được mount vào những vị trí khác nhau trên cây thư mục, tùy theo quyết định của admin — người chịu trách nhiệm quản trị và duy trì hệ thống đó.

### Current Working Directory

Thư mục mà ta đang "đứng" trong đó được gọi là thư mục làm việc hiện tại (current working directory). Để hiển thị thư mục làm việc hiện tại, ta dùng lệnh pwd (print working directory).

```shell
[me@linuxbox ~]$ pwd
/home/me
```

Khi log in vào hệ thống lần đầu (hoặc mở một terminal emulator), thư mục làm việc mặc định sẽ là thư mục home của user đó. Mỗi user được cấp một thư mục home riêng, và đây là nơi duy nhất mà một người dùng thường (regular user) được phép ghi file vào.

### Listing the Contents of a Directory

Để liệt kê các file và thư mục trong thư mục làm việc hiện tại, ta dùng lệnh `ls`.

```shell
[me@linuxbox ~]$ ls
Desktop Documents Music Pictures Public Templates Videos
```

### Changing the Current Working Directory

Để thay đổi thư mục làm việc, dùng lệnh `cd`. khi gõ `cd` theo sau là một dấu cách và pathname của thư mục làm việc muốn tới. Có 2 loại Pathname đường dẫn tuyệt đối (absolute pathname) hoặc đường dẫn tương đối (relative pathname)

#### Đường dẫn tuyệt đối (Absolute Pathnames)

Một đường dẫn tuyệt đối bắt đầu từ thư mục root và đi theo từng nhánh cây cho đến khi hoàn thành đường đi tới thư mục hoặc file mong muốn. *Ví dụ, trên hệ thống linux có một thư mục chứa hầu hết các chương trình được cài đặt. Đường dẫn của thư mục đó là /usr/bin*.

```Shell
[me@linuxbox ~]$ cd /usr/bin
[me@linuxbox bin]$ pwd
/usr/bin
[me@linuxbox bin]$ ls
... Danh sách rất nhiều file ...
```

Bây giờ ta có thể thấy rằng ta đã đổi thư mục làm việc hiện tại thành /usr/bin và nó chứa đầy file. Bạn có để ý dấu nhắc lệnh (shell prompt) đã thay đổi không? Để tiện lợi, dấu nhắc lệnh thường được thiết lập để tự động hiển thị tên của thư mục làm việc.

#### Đường dẫn tương đối (Relative Pathnames)

Đường dẫn tương đối bắt đầu từ thư mục làm việc hiện tại. Nó sử dụng một vài ký hiệu đặc biệt để biểu diễn vị trí tương đối trong filesystem tree. Các ký hiệu đặc biệt đó là `.` (dot) và `..` (dot dot).

Ký hiệu `.` đại diện cho thư mục làm việc hiện tại, còn ký hiệu `..` đại diện cho thư mục cha (parent directory) của thư mục làm việc hiện tại. Ví dụ, hãy đổi thư mục làm việc thành /usr/bin một lần nữa.

```shell
[me@linuxbox ~]$ cd /usr/bin
[me@linuxbox bin]$ pwd
/usr/bin
```

Bây giờ,  muốn đổi thư mục làm việc thành thư mục cha của /usr/bin, tức là /usr. Ta có thể làm điều đó bằng hai cách khác nhau, hoặc dùng đường dẫn tuyệt đối:

```shell
... đường dẫn tuyệt đối ...
[me@linuxbox bin]$ cd /usr
[me@linuxbox usr]$ pwd
/usr
```

```shell
... đường dẫn tương đối ...

[me@linuxbox bin]$ cd ..
[me@linuxbox usr]$ pwd
/usr
```

> [!TIP]
> Trong hầu hết các trường hợp, có thể bỏ qua ./ — nó được ngầm hiểu là có mặt. Gõ:

```shell
[me@linuxbox usr]$ cd bin
```

Nếu ta không chỉ định đường dẫn đến một thứ gì đó, thư mục làm việc hiện tại sẽ được ngầm hiểu là điểm bắt đầu.

#### Một vài phím tắt hữu ích (Some Helpful Shortcuts)

Bảng 2-1 cho thấy một số cách hữu ích để nhanh chóng đổi thư mục làm việc hiện tại.

**Bảng 2-1: Các phím tắt cho lệnh cd**

| Phím tắt | Kết quả |
|---|---|
| cd | Đổi thư mục làm việc thành thư mục home của bạn. |
| cd - | Đổi thư mục làm việc thành thư mục làm việc trước đó. |
| cd ~user_name | Đổi thư mục làm việc thành thư mục home của user_name. Ví dụ, cd ~bob sẽ đổi thư mục thành thư mục home của người dùng bob. |

## Tổng kết chương

- Filesystem Linux được tổ chức theo dạng cây phân cấp, bắt đầu từ một thư mục gốc duy nhất gọi là **ROOT (`/`)**, khác với Windows có nhiều ổ đĩa riêng biệt.
- **Current Working Directory** là thư mục đang "đứng", kiểm tra bằng lệnh `pwd`.
- `ls` dùng để liệt kê nội dung (file/thư mục) bên trong thư mục làm việc hiện tại.
- `cd` dùng để di chuyển giữa các thư mục, kết hợp với 2 loại pathname:
  - **Tuyệt đối**: luôn bắt đầu từ `/`, không phụ thuộc vị trí hiện tại.
  - **Tương đối**: bắt đầu từ vị trí hiện tại, dùng `.` (thư mục hiện tại) và `..` (thư mục cha).
- Một vài shortcut hữu ích: `cd` (về home), `cd -` (về thư mục trước đó), `cd ~user_name` (về home của user khác).

