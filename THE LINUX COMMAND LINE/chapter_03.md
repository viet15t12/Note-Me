# Chương 03: EXPLORING THE SYSTEM

## Tóm tắt nhanh

`ls`   : Liệt kê nội dung thư mục.
`file` : Xác định loại tập tin.
`less` : Xem nội dung tập tin.

## Khái niệm chính

### More Fun with ls

`ls` Là một trong những lệnh được soài nhiều nhất.

Lệnh này giúp xem nội dung bên trong các thư mục chỉ định, đồng thời xác định nhiều thuộc tính quan trọng của tập tin và thư mục.

```shell
[me@linuxbox ~]$ ls
Desktop  Documents  Music  Pictures  Public  Templates  Videos
```

> [!NOTE]
> Chạy `ls` không kèm đối số sẽ liệt kê nội dung của **Current Working Directory**.

```shell
[me@linuxbox ~]$ ls /usr
bin  games  include  lib  local  sbin  share  src
```

> [!TIP]
> Khi chỉ định một đường dẫn (`/usr`), `ls` sẽ liệt kê nội dung của thư mục đó thay vì Current Working Directory.

```shell
[me@linuxbox ~]$ ls ~ /usr
/home/me:
Desktop  Documents  Music  Pictures  Public  Templates  Videos

/usr:
bin  games  include  lib  local  sbin  share  src
```

> [!TIP]
> Có thể truyền **nhiều đối số** (nhiều thư mục) cùng lúc cho `ls`. Kết quả hiển thị lần lượt từng thư mục kèm tiêu đề phân biệt (`~` là ký hiệu viết tắt cho thư mục home).

```shell
[me@linuxbox ~]$ ls -l
total 56
drwxrwxr-x 2 me me 4096 2025-10-26 17:20 Desktop
drwxrwxr-x 2 me me 4096 2025-10-26 17:20 Documents
drwxrwxr-x 2 me me 4096 2025-10-26 17:20 Music
drwxrwxr-x 2 me me 4096 2025-10-26 17:20 Pictures
drwxrwxr-x 2 me me 4096 2025-10-26 17:20 Public
drwxrwxr-x 2 me me 4096 2025-10-26 17:20 Templates
drwxrwxr-x 2 me me 4096 2025-10-26 17:20 Videos
```

> [!IMPORTANT]
> Tùy chọn `-l` (long format) hiển thị **thông tin chi tiết**: quyền truy cập, số liên kết cứng, chủ sở hữu, nhóm, kích thước (byte), ngày giờ sửa đổi và tên tập tin/thư mục.

#### Options and Arguments

Các lệnh trong Linux thường đi kèm với các **tùy chọn (options)** để thay đổi cách hoạt động, cùng các **đối số (arguments)** là đối tượng mà lệnh sẽ tác động.

**VD:** lệnh `ls` được truyền hai tùy chọn: `l` để hiển thị kết quả ở định dạng dài (long format), và `t` để sắp xếp kết quả theo thời gian sửa đổi của tập tin.

```shell
[me@linuxbox ~]$ ls -lt
```

Chúng ta sẽ thêm tùy chọn dài `--reverse` để đảo ngược thứ tự sắp xếp.

```shell
[me@linuxbox ~]$ ls -lt --reverse
```

> [!NOTE]
> Các tùy chọn của lệnh có **phân biệt chữ hoa/chữ thường**.

Lệnh `ls` còn có rất nhiều tùy chọn khả dụng.

| Tùy chọn | Tùy chọn dài | Mô tả |
|---|---|---|
| `-a` | `--all` | Liệt kê tất cả tập tin, kể cả những tập tin có tên bắt đầu bằng dấu chấm — vốn thường không được hiển thị (tức là các tập tin **ẩn**). |
| `-A` | `--almost-all` | Giống `-a` nhưng **không** liệt kê `.` (Current Working Directory) và `..` (thư mục cha). |
| `-d` | `--directory` | Thông thường, nếu chỉ định một thư mục, `ls` sẽ liệt kê **nội dung** của thư mục đó chứ không phải bản thân thư mục. Dùng tùy chọn này kết hợp với `-l` để xem thông tin chi tiết về chính thư mục đó thay vì nội dung bên trong. |
| `-F` | `--classify` | Thêm một ký tự vào cuối mỗi tên được liệt kê, nhanh chóng nhận biết loại của nó mà không cần nhìn màu sắc.. |
| `-h` | `--human-readable` | Trong định dạng liệt kê dài, hiển thị kích thước tập tin theo dạng **dễ đọc** (ví dụ: K, M, G) thay vì tính bằng byte. |
| `-l` | | Hiển thị kết quả ở **định dạng dài** (long format). |
| `-r` | `--reverse` | Hiển thị kết quả theo **thứ tự ngược lại**. Thông thường, `ls` hiển thị kết quả theo thứ tự bảng chữ cái tăng dần. |
| `-S` | | Sắp xếp kết quả theo **kích thước tập tin**. |
| `-t` | | Sắp xếp theo **thời gian sửa đổi**. |

#### A Longer Look at Long Format

Tùy chọn `-l` khiến `ls` hiển thị kết quả theo **định dạng dài (long format)**. Định dạng này chứa rất nhiều thông tin hữu ích. Dưới đây là thư mục Examples từ một hệ thống Ubuntu đời đầu:

```shell
-rw-r--r-- 1 root root 3576296 2017-04-03 11:05 Experience ubuntu.ogg
-rw-r--r-- 1 root root 1186219 2017-04-03 11:05 kubuntu-leaflet.png
-rw-r--r-- 1 root root   47584 2017-04-03 11:05 logo-Edubuntu.png
-rw-r--r-- 1 root root   44355 2017-04-03 11:05 logo-Kubuntu.png
-rw-r--r-- 1 root root   34391 2017-04-03 11:05 logo-Ubuntu.png
-rw-r--r-- 1 root root   32059 2017-04-03 11:05 oo-cd-cover.odf
-rw-r--r-- 1 root root  159744 2017-04-03 11:05 oo-derivatives.doc
-rw-r--r-- 1 root root   27837 2017-04-03 11:05 oo-maxwell.odt
-rw-r--r-- 1 root root   98816 2017-04-03 11:05 oo-trig.xls
-rw-r--r-- 1 root root  453764 2017-04-03 11:05 oo-welcome.odt
-rw-r--r-- 1 root root  358374 2017-04-03 11:05 ubuntu Sax.ogg
```

| Trường | Ý nghĩa |
|---|---|
| `-rw-r--r--` | **Quyền truy cập** vào tập tin. Ký tự đầu tiên cho biết **loại tập tin**. Trong số các loại khác nhau, dấu gạch ngang (`-`) ở đầu nghĩa là tập tin thông thường, còn `d` cho biết đó là thư mục. Ba ký tự tiếp theo là quyền truy cập dành cho **chủ sở hữu** tập tin, ba ký tự kế tiếp dành cho **thành viên của nhóm** sở hữu tập tin, và ba ký tự cuối cùng dành cho **tất cả những người còn lại**. |
| `1` | **Số liên kết cứng (hard links)** của tập tin. |
| `root` | **Tên người dùng** là chủ sở hữu tập tin. |
| `root` | **Tên nhóm** sở hữu tập tin. |
| `32059` | **Kích thước** của tập tin tính bằng byte. |
| `2017-04-03 11:05` | **Ngày giờ** sửa đổi lần cuối của tập tin. |
| `oo-cd-cover.odf` | **Tên** của tập tin. |
