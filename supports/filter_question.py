# py supports/filter_question.py source/...
import os
import re
import sys

OUTPUT_FILENAME = "cau-hoi-tong-hop.md"


def gop_va_loc_trung(input_folder):
    # 1. Xác định tên môn và file kết quả cố định ngay trong thư mục môn
    folder_name = os.path.basename(os.path.normpath(input_folder))
    output_filepath = os.path.join(input_folder, OUTPUT_FILENAME)

    # Xóa file cũ trước khi tạo file mới
    if os.path.exists(output_filepath):
        os.remove(output_filepath)

    # 2. Bắt đầu đọc và lọc trùng
    cau_hoi_duy_nhat = {}
    tong_cau_goc = 0

    for filename in sorted(os.listdir(input_folder)):
        if filename.endswith(".md"):
            filepath = os.path.join(input_folder, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

                blocks = re.split(r"^(\d+)\.\s+", content, flags=re.MULTILINE)

                for i in range(1, len(blocks), 2):
                    tong_cau_goc += 1
                    q_body = blocks[i + 1].strip()

                    if not q_body:
                        continue

                    match = re.search(r"\n([A-D]\.)", q_body, re.IGNORECASE)

                    if match:
                        split_idx = match.start()
                        noi_dung_cau_hoi = q_body[:split_idx].strip()
                        normalized_question = re.sub(r"\s+", " ", noi_dung_cau_hoi).lower()
                        answer_match = re.search(r"(?:^|\n)\s*(?:đáp\s*án|answer)\s*:\s*([^\n]+)", q_body, re.IGNORECASE)
                        if answer_match:
                            answer_keys = sorted(set(letter.upper() for letter in re.findall(r"[A-Fa-f]", answer_match.group(1))))
                            normalized_answer = ",".join(answer_keys)
                        else:
                            normalized_answer = ""
                        key = (normalized_question, normalized_answer)

                        if key not in cau_hoi_duy_nhat:
                            cau_hoi_duy_nhat[key] = q_body
                    else:
                        pass  # Bỏ qua thông báo lỗi nhỏ để màn hình Terminal gọn gàng

    # 3. Ghi kết quả ra file
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(f"# TỔNG HỢP CÂU HỎI MÔN {folder_name.upper()} \n\n")
        for stt, q_body in enumerate(cau_hoi_duy_nhat.values(), 1):
            f.write(f"{stt}. {q_body}\n\n")

    # 4. In thông báo
    print("-" * 50)
    print("✅ ĐÃ XỬ LÝ HOÀN TẤT!")
    print(f"📁 Thư mục nguồn: {input_folder}")
    print(f"📝 Tổng số câu đọc được: {tong_cau_goc} câu")
    print(f"✨ Số câu sau khi lọc trùng: {len(cau_hoi_duy_nhat)} câu")
    print(f"🗑️ Số câu trùng lặp đã xóa: {tong_cau_goc - len(cau_hoi_duy_nhat)} câu")
    print(f"💾 File kết quả: {output_filepath}")
    print("-" * 50)


# ================= ĐIỂM BẮT ĐẦU CHẠY CODE =================
if __name__ == "__main__":
    # Kiểm tra xem người dùng có gõ thư mục truyền vào không
    if len(sys.argv) < 2:
        print("❌ Lỗi: Bạn chưa nhập đường dẫn thư mục cần xử lý!")
        print("💡 Cách dùng: python loc_cau_hoi.py <đường_dẫn_thư_mục>")
        print("Ví dụ: python loc_cau_hoi.py source/mln111")
        sys.exit(1)

    # Lấy tham số người dùng gõ vào sau chữ "python loc_cau_hoi.py"
    thu_muc_dau_vao = sys.argv[1]

    # Kịch bản thông minh: Nếu người dùng chỉ gõ tên môn học (vd: "mln122") thay vì gõ cả đường dẫn "source/mln122"
    if not os.path.exists(thu_muc_dau_vao):
        thu_muc_thay_the = os.path.join("source", thu_muc_dau_vao)
        if os.path.exists(thu_muc_thay_the):
            thu_muc_dau_vao = thu_muc_thay_the
        else:
            print(f"❌ Không tìm thấy thư mục: {thu_muc_dau_vao}")
            sys.exit(1)

    gop_va_loc_trung(thu_muc_dau_vao)
