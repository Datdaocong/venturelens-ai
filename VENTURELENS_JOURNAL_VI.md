# 🚀 Nhật ký dự án VentureLens (Tiếng Việt)

## 1. Ý tưởng ban đầu

Mục tiêu ban đầu:

> Tạo AI phân tích startup idea

### ❌ Vấn đề:
- chỉ dùng LLM
- output nghe hay nhưng không có cơ sở

### 💡 Nhận ra:
Nếu chỉ dùng LLM → chỉ là chatbot, không phải hệ thống phân tích

---

## 2. Chuyển sang dùng dữ liệu

Dataset gồm:
- description
- industry
- funding
- success_score
- outcome_label

### Thay đổi tư duy

Từ:
Idea → LLM

Sang:
Idea → Data → Signals → Output

---

## 3. Retrieval (TF-IDF)

Dùng TF-IDF để tìm startup tương tự

### ❌ Lỗi:
- match từ chung
- dataset lỗi

### Fix:
- clean data
- chuẩn hóa pipeline

---

## 4. Xây pipeline

Idea  
→ Retrieval  
→ Scoring  
→ Risk  
→ Scenario  
→ Recommendation  
→ Report  

---

## 5. Làm RAG

Thêm:
- rag_context_builder

### Vai trò:
- lấy startup tương tự
- build evidence

### Insight:
LLM chỉ là người viết, không phải bộ não

---

## 6. Sửa scoring

### ❌ Lỗi:
Idea linh tinh vẫn 100 điểm

### Nguyên nhân:
- không có penalty
- không giới hạn score

### ✅ Fix:
- thêm penalty
- cap theo similarity
- điều kiện số peer

---

## 7. Risk analyzer

Rule-based:

- failure cao → risk cao  
- similarity thấp → risk cao  

---

## 8. Scenario simulator

Nâng cấp thành structured:

- title  
- description  
- trigger  
- warning  
- action  

---

## 9. UI

Hiển thị:
- score  
- radar chart  
- peer signals  
- scenarios  
- recommendations  

---

## 10. Kiến trúc

Chia thành:

- Data layer  
- Logic layer  
- Presentation layer  

---

## 11. Bài học

1. Không dùng LLM một mình  
2. Retrieval là cốt lõi  
3. Scoring phải “khó tính”  
4. Structure quan trọng hơn model  

---

## 12. Hướng phát triển

- embeddings  
- baseline theo ngành  
- ranking percentile  
- cải thiện UI  

---

## 🎯 Câu dùng khi phỏng vấn

“Tôi xây dựng một hệ thống phân tích startup chuyển từ LLM-based sang RAG pipeline, kết hợp dữ liệu thật, scoring, risk analysis và scenario simulation.”