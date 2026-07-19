import sys

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Change 1
old1 = "Lớp live qua Zoom ba buổi tối mỗi tuần, học viên từ khắp các tỉnh thành và cả nước ngoài. Bận lịch buổi nào xem lại record buổi đó, mentor theo sát qua nhóm học tập."
new1 = "Lớp học trực tiếp qua Zoom vào ba buổi tối mỗi tuần, phù hợp với học viên ở khắp các tỉnh thành và cả nước ngoài. Nếu bận, bạn có thể xem lại bản ghi của buổi học; đồng thời, mentor luôn đồng hành và hỗ trợ sát sao qua nhóm học tập."
text = text.replace(old1, new1)

# Change 2
old2a = "Không học để biết.</span><span style=\"display:block\">Học để"
new2a = "Không học chỉ để biết.</span><span style=\"display:block\">Học để"
text = text.replace(old2a, new2a)
# also replace in the plain text span
text = text.replace(">Không học để biết.</span>", ">Không học chỉ để biết.</span>")
text = text.replace("nhận việc thật, làm được việc thật", "nhận việc thật và làm được việc thật")

old2b = "Mỗi module tập trung vào một domain thực tế với project và bài exam đánh giá năng lực. Đặc biệt, bạn sẽ được tham gia nhóm mentorship chuyên sâu theo đúng định hướng ngành nghề của mình."
new2b = "Mỗi module tập trung vào một lĩnh vực thực tế, đi kèm project và bài đánh giá năng lực. Đặc biệt, bạn sẽ được tham gia nhóm mentorship chuyên sâu, bám sát định hướng ngành nghề mà mình theo đuổi."
text = text.replace(old2b, new2b)

# Change 3 (Hành trình)
old3a = "Hành trình khoá 2026 · Lưu lại chặng đường hành trình của bản thân bạn"
new3a = "Hành trình khóa 2026 · Lưu lại từng dấu mốc của riêng bạn"
text = text.replace(old3a, new3a)

text = text.replace("trải từ <span style", "diễn ra từ <span style")

old3c = "Vòng ngoài khắc đúng 100 vạch, mỗi vạch là một buổi live. Chín vạch vàng ở cung tháng 8 là warm-up Python và SQL, khúc đậm cuối năm là Module 4 Agentic AI, còn chấm tròn và ô vuông đánh dấu seminar, project, kỳ thi của từng module. Ngày giờ cụ thể của từng buổi nằm trong lộ trình chi tiết."
new3c = "Vòng ngoài gồm đúng 100 vạch, mỗi vạch tương ứng với một buổi học live. Chín vạch vàng trong tháng 8 đại diện cho giai đoạn warm-up Python và SQL; phần đậm ở cuối năm là Module 4 - Agentic AI. Các chấm tròn và ô vuông đánh dấu seminar, project và kỳ thi của từng module. Ngày giờ cụ thể của mỗi buổi được cập nhật trong lộ trình chi tiết."
text = text.replace(old3c, new3c)

old3d_1 = "9 buổi Python &amp; SQL live Zoom cho học viên Early-bird."
new3d_1 = "9 buổi học Python và SQL trực tiếp qua Zoom dành cho học viên Early Bird."
text = text.replace(old3d_1, new3d_1)

old3e = "Seminar DA in Sales mở đầu lộ trình 8 module."
new3e = "Seminar “DA in Sales” mở đầu lộ trình gồm 8 module."
text = text.replace(old3e, new3e)

old3f_1 = "Module 4 - AI cho DA qua 4 domain: Game, EdTech, Marketing, HR."
new3f_1 = "Module 4 tập trung vào ứng dụng AI cho Data Analytics qua 4 domain: Game, EdTech, Marketing và HR."
text = text.replace(old3f_1, new3f_1)

old3g_1 = "Hai phần thi cuối; lớp luyện PL-300 &amp; AWS xếp lịch riêng."
new3g_1 = "Hai phần thi cuối khóa; lịch luyện thi PL-300 và AWS được sắp xếp riêng."
text = text.replace(old3g_1, new3g_1)

old_exam = "Final Exam &amp; chứng chỉ"
new_exam = "Final Exam &amp; Chứng chỉ"
text = text.replace(old_exam, new_exam)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Done updates")
