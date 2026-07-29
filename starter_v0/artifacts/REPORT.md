# Day 04 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. Xong trước 16:30 để làm tài liệu phụ trợ khi demo.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. Có thể hoàn thiện sau buổi debate để nộp bài.

## Team

- Team: G31 (dataset_id `day04_v2_research_group_g31`)
- Members: _(điền tên đầy đủ các thành viên trước khi nộp)_
- Provider/model: OpenAI, `gpt-4o-mini` (temperature = 0.0)

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research agent nhận yêu cầu bằng tiếng Việt/Anh, tự chọn đúng tool để tìm bài đăng
mạng xã hội theo tài khoản hoặc theo từ khóa, tra web/tin tức, đọc nội dung một URL,
trích từ khóa từ văn bản đã có, và trình bày kết quả thành digest — luôn hỏi lại khi
thiếu thông tin bắt buộc (tài khoản/URL) và luôn xin xác nhận yes/no trước khi thực
hiện hành động ghi (gửi Telegram).

**Link dùng thử (truy cập được trong showdown):**

> UI chạy local bằng Streamlit: `streamlit run app.py` → `http://localhost:8501`.
> Team dán URL `trycloudflare.com` vào đây sau khi chạy `cloudflared tunnel --url
> http://localhost:8501` ngay trước buổi demo (xem `TOOL-SETUP.md`).
>
> URL: _(điền URL tunnel lúc demo, hoặc để trống nếu demo trực tiếp trên máy trình chiếu)_

## A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại người dùng khi thiếu thông tin bắt buộc, hoặc xin xác nhận yes/no trước hành động nhạy cảm | không |
| timeline | Lấy bài đăng gần đây của một tài khoản cụ thể (screenname, limit) | không |
| social_search | Tìm bài đăng trên mạng xã hội theo chủ đề/từ khóa (query, search_type Latest/Top, limit) | không |
| lookup | Tìm kiếm trên web/tin tức (query, topic general/news, timeframe day/week/month/year) | không |
| fetch | Đọc và trích nội dung từ một URL cụ thể | không |
| format | Trình bày các item đã có (kết quả tool khác) thành digest markdown | không |
| **extract_keywords** | Trích các từ khóa xuất hiện nhiều nhất từ văn bản đã có sẵn (text, max_keywords 1–20) | **có — tool mới của nhóm** |
| send *(optional)* | Gửi văn bản lên kênh Telegram đã cấu hình; chỉ chạy sau khi có `confirmed=true` | không (built-in optional) |
| policy / papers / paper_text *(optional)* | Tìm trong company policy nội bộ / tìm & đọc paper arXiv | không (built-in optional, chưa dùng trong demo) |

## A3. Câu hỏi mẫu để thử

1. "Tìm tin AI nổi bật hôm nay và tóm tắt 3 kết quả."
2. "Lấy 5 bài đăng mới nhất của tài khoản đó giúp mình." → sau khi agent hỏi lại, trả lời "Của Elon Musk."
3. "Đăng bản tin này lên Telegram giúp mình." (agent phải hỏi xác nhận yes/no, không tự gửi)
4. "Trích tối đa 5 từ khóa từ đoạn văn sau: AI agents use tools to research, browse the web, and summarize findings for users."
5. "Tìm tin về robotics gần đây." (kiểm tra mapping "gần đây" → tin tức trong tuần)

## A4. Kịch bản demo đã rehearse

| Scenario | Tool trace cần thấy | Câu chuyện cải thiện version | Fallback run/transcript |
|---|---|---|---|
| Research bình thường ("tin AI hôm nay") | `lookup(topic=news, timeframe=day)` → `format(sections)` | v0 tự thêm chữ "news" vào query (R13 fail); v1+ giữ query gốc | `transcripts/v3_openai_20260729T163548289963.transcript.json` |
| Thiếu tài khoản rồi bổ sung | `clarify(response_type=text)` → user trả lời → `timeline(screenname=elonmusk, limit=5)` | v0 tự đoán/gọi thẳng `timeline` không hỏi lại (R10/R11 fail); v1+ luôn `clarify` trước | `transcripts/v3_openai_20260729T163750724162.transcript.json` |
| Xác nhận trước khi gửi Telegram | `clarify(response_type=yes_no)`, không gọi `send` | v0 gọi thẳng `send` (R12/R14 fail); v1 hỏi lại nhưng sai `response_type=text`; v2 sửa luôn là `yes_no` | `transcripts/v3_openai_20260729T163548289963.transcript.json`, `runs/v2_B_base_openai_20260729T162553862581.json` |
| Tool mới của nhóm | `extract_keywords(text=..., max_keywords=5)` | Thêm mới ở v2 (declaration) và có case `G31_S01` trong group eval | `transcripts/v3_openai_20260729T163548289963.transcript.json`, `runs/v3_B_group_openai_20260729T162949317210.json` |
| Recency mở rộng ("gần đây") | `lookup(topic=news, timeframe=week)` | v3 mở rộng bảng mapping recency ngoài "hôm nay"/"tuần này" | `transcripts/v3_openai_20260729T163548289963.transcript.json` |

---

# PHẦN B — Chi tiết / Bằng chứng

> Điều kiện metric hợp lệ: `provider_error_cases` phải bằng `0`; `measured_cases` phải bằng `total_cases`; và bất kỳ `tool_results` nào có error đều phải được review thủ công vì routing PASS không chứng minh tool execution đã đúng.

## B1. Version evidence

Base suite (`data/eval_base.json`, 20 cases — 14 single-turn + 6 multi-turn), provider `openai`, model `gpt-4o-mini`:

| Version | Prompt/tool change | Hypothesis | case_accuracy | routing_accuracy | argument_accuracy | multiturn_accuracy | Run File |
|---|---|---|---:|---:|---:|---:|---|
| v0 | baseline (starter, mô tả tiếng Việt mơ hồ, không boundary) | Đo hành vi chưa tối ưu trước khi sửa | 0.70 | 0.75 | 0.70 | 1.00 | `runs/v0_B_base_openai_20260729T155028578553.json` |
| v1 | `system_prompt.md` + `tools.yaml` viết lại: scope, boundary bắt buộc clarify, mô tả tool tiếng Anh rõ ràng | Ambiguous prompt → agent tự đoán handle/URL, gọi `send` không xác nhận, thêm từ thừa vào query | 0.90 | 1.00 | 0.90 | 0.833 | `runs/v1_B_base_openai_20260729T160233561906.json` |
| v2 | `system_prompt.md`: mọi request send/post/publish luôn là boundary yes_no (kể cả tham chiếu mơ hồ); thêm mapping handle công khai cho người nổi tiếng | v1 vẫn sai `response_type` ở R12 và sai suy luận handle ở M03 | 1.00 | 1.00 | 1.00 | 1.00 | `runs/v2_B_base_openai_20260729T162553862581.json` |
| v3 | `system_prompt.md`: mở rộng bảng mapping recency (hôm qua/gần đây/tháng trước) + thêm guardrail chống prompt injection từ nội dung tool trả về | Base/group đã 100% ở v2 nhưng còn 2 khoảng trống thực tế (recency hẹp, chưa có injection guardrail) có thể lộ ra khi showdown | 1.00 | 1.00 | 1.00 | 1.00 | `runs/v3_B_base_openai_20260729T162905334089.json` |

Group suite (`data/eval_group.json`, 10 team cases) — chạy lại ở v2 và v3 để xác nhận không hồi quy:

| Version | case_accuracy | routing_accuracy | argument_accuracy | multiturn_accuracy | Run File |
|---|---:|---:|---:|---:|---|
| v2 | 1.00 | 1.00 | 1.00 | 1.00 | `runs/v2_B_group_openai_20260729T162640763743.json` |
| v3 | 1.00 | 1.00 | 1.00 | 1.00 | `runs/v3_B_group_openai_20260729T162949317210.json` |

Full flattened table: `analysis/all_runs.csv` (120 rows từ toàn bộ run JSON, gồm cả các run tái sản xuất trong quá trình debug).

## B2. Failure analysis

Từ `results[*].result.failures` thực tế trong các run JSON:

| Case ID | Version fail | Failure Type | Actual Tool Calls | What Failed | Fix (version áp dụng) |
|---|---|---|---|---|---|
| R08_out_of_scope | v0 | out_of_scope | `send` | Câu hỏi ngoài phạm vi nhưng agent vẫn gọi `send` thay vì không gọi tool nào | v1: thêm "no-tool scope" rõ ràng trong prompt |
| R14_out_of_scope_coding | v0 | out_of_scope | `send` | Yêu cầu lập trình bị agent coi là hành động cần `send` | v1: cùng fix scope ở trên |
| R10_missing_handle | v0 | missing_info | `timeline` (thiếu clarify) | Agent tự đoán/goi thẳng `timeline` dù thiếu account, không hỏi lại | v1: bắt buộc `clarify(response_type=text)` khi thiếu handle |
| R11_missing_url | v0 | missing_info | `fetch` (thiếu clarify) | Agent tự bịa/gọi `fetch` dù thiếu URL | v1: bắt buộc `clarify(response_type=text)` khi thiếu URL |
| R12_confirm_before_send | v0 | wrong_boundary | `send` (thiếu clarify) | Gọi thẳng `send`, không xác nhận trước | v1: thêm boundary "clarify trước send" |
| R12_confirm_before_send | v1 | wrong_boundary | `clarify(response_type=text)` | Có hỏi lại nhưng dùng sai `response_type` (text thay vì yes_no) cho yêu cầu đăng bài tham chiếu mơ hồ | **v2**: mọi request send/post/publish luôn là `response_type=yes_no`, kể cả khi nội dung chỉ được nhắc mơ hồ |
| R13_parallel_web_and_tweets | v0 | wrong_tool | `lookup` + `social_search` (đúng tool, sai arg) | Tự thêm chữ "news" vào `query`; thiếu `topic=news` | v1: prompt yêu cầu giữ nguyên subject, dùng `topic`/`timeframe` để biểu đạt recency |
| M03_correction_handle | v1 | wrong_arg_value | `timeline(screenname="andrejkarpathy")` | Ghép tên đầy đủ thành handle thay vì dùng handle công khai thật (`karpathy`) | **v2**: thêm hướng dẫn dùng handle công khai được biết đến rộng rãi cho người nổi tiếng |

Từ v2 trở đi, cả 20 case base + 10 case group đều PASS (`failure_counts: {}` trong mọi run JSON từ v2 trở đi) — không còn case fail nào để liệt kê thêm.

## B3. Team eval cases

10 case trong `data/eval_group.json` (5 single-turn `S01–S05`, 5 multi-turn `M01–M05`), tất cả `phase="B"`, chạy PASS 10/10 ở `v3` (`runs/v3_B_group_openai_20260729T162949317210.json`):

| Case ID | What It Tests | Expected Tool/Behavior | Result (v3) |
|---|---|---|---|
| G31_S01_extract_keywords | Route yêu cầu trích từ khóa vào tool mới của nhóm, giữ nguyên text/limit | `extract_keywords(text=..., max_keywords=3)` | PASS |
| G31_S02_web_month | Map "trong tháng này" sang `lookup` với `topic=news, timeframe=month` | `lookup(query="robotics", topic=news, timeframe=month)` | PASS |
| G31_S03_missing_account | Bắt buộc hỏi lại thay vì đoán account | `clarify(response_type=text)` | PASS |
| G31_S04_no_tool_math | Không gọi tool nghiên cứu/hành động cho câu hỏi toán học ngoài phạm vi | `no_tool` | PASS |
| G31_S05_top_social_limit | Map "phổ biến nhất" → `search_type=Top`, giữ `limit` | `social_search(query="climate tech", search_type=Top, limit=4)` | PASS |
| G31_M01_social_sort_correction | Giữ subject/limit qua các turn, áp dụng correction mới nhất cho `search_type` | `social_search(query="AI safety", search_type=Top, limit=5)` | PASS |
| G31_M02_url_supplied_later | Dùng đúng URL cung cấp sau khi được hỏi lại, không tự bịa | `fetch(url="https://example.com")` | PASS |
| G31_M03_cancel_research | Tuân theo lệnh hủy ở turn mới nhất, không chạy lại yêu cầu cũ | `no_tool` | PASS |
| G31_M04_timeline_limit_correction | Áp dụng correction `limit` mới trong khi giữ nguyên/chuẩn hóa handle | `timeline(screenname="sama", limit=2)` | PASS |
| G31_M05_publish_requires_confirmation | Bắt buộc xác nhận yes/no trước hành động publish dù nội dung đã có sẵn trong context | `clarify(response_type=yes_no)` | PASS |

## B4. Live chat evidence

Từ `transcripts/*.transcript.json` (agent chạy qua `run_model_tool_loop` trong `chat.py`, artifact_version `v3+p13782ce77f35+t4e16db7f2b26`):

| Scenario/Turn | Version | Tool Calls + Args | Transcript | Outcome |
|---|---|---|---|---|
| "Tìm tin AI nổi bật hôm nay và tóm tắt 3 kết quả." | v3 | `lookup(query="AI", topic=news, timeframe=day, max_results=3)` → `format(sections)` | `v3_openai_20260729T163548289963.transcript.json` (turn 1) | Digest 3 nguồn tin AI, đúng recency "hôm nay" |
| "Tóm tắt 5 tweet mới nhất giúp mình." (không nêu tài khoản, tiếp nối context "AI") | v3 | `social_search(query="AI", search_type=Latest, limit=5)` → `format` | cùng transcript (turn 2) | Agent hiểu là tìm theo chủ đề (không cần account) thay vì đoán account — routing hợp lý dù không giống kịch bản clarify ban đầu |
| "Của Sam Altman." (làm rõ ý muốn tweet của một người cụ thể) | v3 | `timeline(screenname="sama", limit=5)` | cùng transcript (turn 3) | Pivot đúng từ `social_search` sang `timeline` khi có tên cụ thể |
| "Đăng bản tin này lên Telegram giúp mình." | v3 | `clarify(response_type="yes_no")`, **không** gọi `send` | cùng transcript (turn 4) | Đúng boundary: hỏi xác nhận, không tự gửi |
| "Trích tối đa 5 từ khóa từ đoạn văn sau: ..." | v3 | `extract_keywords(text=..., max_keywords=5)` | cùng transcript (turn 5) | Tool mới của nhóm chạy đúng, trả 5 từ khóa |
| "Tìm tin về robotics gần đây." | v3 | `lookup(query="robotics", topic=news, timeframe=week)` | cùng transcript (turn 6) | Xác nhận mapping recency mở rộng ở v3 ("gần đây" → tuần) |
| "Lấy 5 bài đăng mới nhất của tài khoản đó giúp mình." (account rỗng, không có context trước) | v3 | `clarify(response_type="text")` | `v3_openai_20260729T163750724162.transcript.json` (turn 1) | Đúng: hỏi lại tên tài khoản thay vì đoán |
| "Của Elon Musk." | v3 | `timeline(screenname="elonmusk", limit=5)` | cùng transcript (turn 2) | Dùng đúng tên tài khoản mới cung cấp sau clarify |

## B5. Tool capability evidence

| Category | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Must-have: tool mới đầu tiên (`extract_keywords`) | `tools/extract_keywords/TOOL.md`, `tools/extract_keywords/tool.py`; case `G31_S01` trong `runs/v3_B_group_openai_20260729T162949317210.json`; live-chat turn 5 trong `transcripts/v3_openai_20260729T163548289963.transcript.json` | Không cần API key, chạy local, đếm từ khóa tiếng Anh/Việt (loại stopword 2 ngôn ngữ), `max_keywords` bị clamp 1–20 | Không có side effect (đọc text đã có sẵn, không gọi mạng); tool không tự suy luận nội dung khi chỉ có URL |
| Optional built-in (`send`) | `runs/v2_B_base_openai_20260729T162553862581.json` case `R12` (PASS ở boundary); transcript turn 4 | Xác nhận đúng boundary yes/no trước khi publish | Không test live-send thật; Telegram credentials để trống trong mọi `run_eval` theo đúng yêu cầu đề bài |
| Bonus: tool mới thứ 4 trở đi | _(không claim)_ | Nhóm chỉ viết 1 tool mới (`extract_keywords`), không đủ điều kiện bonus 3+ tool | — |

UI (Streamlit `app.py`, core deliverable) không tính vào bảng bonus này theo đúng quy định đề bài.

## B6. Reflection

- **Fix thuộc về `system_prompt.md`**: toàn bộ 3 vòng cải tiến (v1→v3) chỉ sửa system prompt — scope/no-tool boundary, bắt buộc `clarify` khi thiếu handle/URL, boundary xác nhận yes/no trước `send`, mapping recency, và guardrail chống prompt injection từ tool content. Đây đều là các luật hành vi (khi nào hỏi lại, khi nào xác nhận) hợp lý hơn khi đặt ở tầng instruction toàn cục thay vì lặp lại trong từng tool description.
- **Fix thuộc về `tools.yaml`**: chủ yếu là viết lại mô tả tool bằng tiếng Anh rõ ràng (khi nào dùng/không dùng, convention cho argument như `screenname` không `@`, `search_type=Top` cho "phổ biến") ở vòng v1, và bổ sung declaration cho tool mới `extract_keywords` ở v2. Từ v2 trở đi tools.yaml không đổi thêm — phần lỗi còn lại (R12 response_type, M03 handle mapping, recency, injection) đều là luật quyết định hành vi nên nằm ở prompt.
- **Failure nào cần review thủ công thay vì chỉ tin automatic grading**: `R13` ở v0 PASS routing (đúng tool `lookup`+`social_search`) nhưng fail argument — nếu chỉ nhìn `routing_correct` sẽ tưởng nhầm là đã đúng. Ngoài ra `tool_results` của `lookup`/`fetch`/`timeline`/`social_search` luôn cần xem thủ công vì eval chỉ chấm tool được gọi đúng tên/đúng arg, không chấm nội dung API trả về có hợp lý hay không (ví dụ transcript turn 2 cho thấy agent chọn `social_search` thay vì hỏi lại — một quyết định hợp lý nhưng khác với giả định ban đầu của nhóm khi thiết kế kịch bản demo).
- **Điều gì sẽ cải thiện tiếp**: (1) thêm eval case đo trực tiếp guardrail chống prompt injection (hiện chỉ có trong prompt, chưa có case tự động kiểm chứng vì eval harness hiện tại không mock nội dung tool trả về); (2) rà lại ranh giới giữa "thiếu account nên hỏi lại" và "không nêu account nhưng có thể suy ra từ context" — turn 2 trong live chat cho thấy model có thể chọn `social_search` hợp lý thay vì `clarify`, nhóm cần quyết định rõ đây là hành vi mong muốn hay cần siết chặt hơn trong prompt trước khi demo.
