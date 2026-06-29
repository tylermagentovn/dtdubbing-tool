+ Build hệ thống các tool phục vụ cho DTDUBBING
+ Chạy trên subdomain : tool.dtdubbing.com
+ Sẽ phải đăng nhập mới sử dụng được tool (dùng user, pass cố định không cần dùng DB)
+ Giao diện ngoài cùng sẽ là list các tool
+ Tool chủ yếu sẽ hoạt động frontend là typescript còn backend sẽ là python vì chủ yếu dùng đến ffmpeg, cấu trúc thư mục rõ ràng để tách biệt các tool với nhau nhưng vẫn sử dụng cấu trúc chung.
+ Ứng dụng đầu tiên sẽ là Tách SRT 
Mô tả ứng dụng : 
Chúng tôi có 1 file srt phim, tuy nhiên file video đã bị tách thành các ep khác nhau, vì vậy bây giờ chúng tôi muốn tham chiếu thời lượng của các tập video để chia srt phù hợp tương ứng cho từng tập.
