# Kế hoạch làm bài Day 04 cho nhóm 4 người

## 1. Mục tiêu chung

Nhóm xây một Research Agent có thể:

- nhận yêu cầu của người dùng;
- chọn đúng tool và truyền đúng arguments;
- thực thi API/tool thật;
- lưu run JSON và transcript;
- cải thiện routing qua các version `v0`, `v1`, `v2`, `v3`;
- có ít nhất một tool mới do nhóm tự viết;
- có đúng 10 group eval cases: 5 single-turn và 5 multi-turn;
- có UI chạy được và hiển thị tool trace;
- hoàn thiện `artifacts/REPORT.md` dựa trên log thật.

Thư mục làm bài chính là:

```text
starter_v0/
```

Không commit `.env`, API key, `.venv`, cache hoặc output chứa secrets.

---

## 2. Phân công tổng quát

| Thành viên | Vai trò chính | Deliverable sở hữu | Ghi chú |
|---|---|---|---|
| Thành viên 1 — Lead / Prompt | Điều phối nhóm, chạy baseline, tối ưu prompt/tool routing, cập nhật version log | `artifacts/system_prompt.md`, `artifacts/tools.yaml`, `artifacts/version_log.csv`, `runs/` | Là người chịu trách nhiệm chính cho việc cải thiện routing qua v0→v3 |
| Thành viên 2 — Tool Developer | Thiết kế, code và test ít nhất một tool mới | `tools/<tool_moi>/`, phần registry trong `tools/__init__.py`, declaration tool mới | Trao đổi với Thành viên 1 trước khi sửa `tools.yaml` |
| Thành viên 3 — Eval / Report | Viết 10 group eval cases, phân tích run và viết report | `data/eval_group.json`, `analysis/`, `artifacts/REPORT.md` | Không sửa fixed base eval |
| Thành viên 4 — UI / Demo | Xây UI, lưu transcript, chuẩn bị kịch bản demo | `app.py`, `requirements.txt`, `transcripts/`, tài liệu demo | Tái sử dụng agent loop trong `chat.py` |

---

## 3. Quy trình làm việc theo từng bước

### Bước 1 — Setup chung
Mọi người cùng thực hiện:

```powershell
cd starter_v0
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Sau đó mỗi người điền key vào `.env` và chạy preflight:

```powershell
python scripts/preflight_provider.py --provider openai
```

### Bước 2 — Baseline v0
Thành viên 1 chạy baseline:

```powershell
python run_eval.py --provider openai --version v0 --suite base --eval-cases data/eval_base.json
```

Thành viên 1 phân tích run JSON để tìm lỗi về:
- tool routing sai
- argument sai
- thiếu clarify
- gọi tool thừa

### Bước 3 — Tối ưu prompt và tool declaration
Thành viên 1 sửa:
- `artifacts/system_prompt.md`
- `artifacts/tools.yaml`

Sau mỗi lần sửa, chạy lại eval để tạo `v1`, `v2`, `v3`.

### Bước 4 — Thêm tool mới
Thành viên 2 thực hiện:
1. tạo tool mới trong `tools/`
2. viết `TOOL.md`
3. đăng ký trong `tools/__init__.py`
4. khai báo trong `artifacts/tools.yaml`
5. smoke test tool trước khi dùng trong eval

### Bước 5 — Viết team eval cases
Thành viên 3 tạo đúng 10 case trong `data/eval_group.json`:
- 5 single-turn
- 5 multi-turn

### Bước 6 — Chạy team eval
Thành viên 3 hoặc Thành viên 1 chạy:

```powershell
python run_eval.py --provider openai --version v3 --suite group --eval-cases data/eval_group.json
```

### Bước 7 — Làm UI và demo
Thành viên 4 xây UI và đảm bảo:
- hiển thị request/response
- hiện trace từng tool
- lưu transcript
- có thể demo được cho mentor

### Bước 8 — Hoàn thiện report
Thành viên 3 viết `artifacts/REPORT.md` dựa trên dữ liệu thật từ run, transcript và version log.

---

## 4. Phân công chi tiết theo từng thành viên

### Thành viên 1 — Lead / Prompt
**Nhiệm vụ chính:**
- setup và kiểm tra provider
- chạy baseline v0
- sửa prompt/tool declaration
- chạy v1, v2, v3
- cập nhật `version_log.csv`

**Checklist:**
1. Cài môi trường và chạy preflight.
2. Chạy baseline `v0`.
3. Đọc run JSON, tìm lỗi và chọn hypothesis.
4. Sửa prompt/tool declaration.
5. Chạy lại eval tạo `v1`, `v2`, `v3`.
6. Ghi kết quả vào version log.

---

### Thành viên 2 — Tool Developer
**Nhiệm vụ chính:**
- làm tool mới
- test tool thật
- đăng ký tool

**Checklist:**
1. Chọn tool mới cần viết.
2. Tạo folder tool trong `tools/`.
3. Viết `TOOL.md` và implementation.
4. Đăng ký trong `tools/__init__.py`.
5. Thêm khai báo vào `artifacts/tools.yaml`.
6. Chạy smoke test.

---

### Thành viên 3 — Eval / Report
**Nhiệm vụ chính:**
- viết eval cases
- phân tích run
- viết report

**Checklist:**
1. Tạo `data/eval_group.json` với đúng 10 case.
2. Chạy suite group.
3. Phân tích fail case và kết quả.
4. Viết `artifacts/REPORT.md`.
5. Chuẩn bị bằng chứng cho demo.

---

### Thành viên 4 — UI / Demo
**Nhiệm vụ chính:**
- xây UI
- lưu transcript
- chuẩn bị demo live

**Checklist:**
1. Tạo `app.py` hoặc UI cho lab.
2. Dùng lại agent loop từ `chat.py`.
3. Hiển thị request, response, tool trace và version.
4. Lưu transcript.
5. Chuẩn bị 3–5 kịch bản demo.

---

## 5. Timeline đề xuất

### Giai đoạn 1 – Setup (15–20 phút)
- Cả nhóm cùng chạy setup và preflight.

### Giai đoạn 2 – Baseline (30–45 phút)
- Thành viên 1 chạy v0.
- Thành viên 3 đọc kết quả và chuẩn bị eval cases.
- Thành viên 2 kiểm tra tool hiện có.
- Thành viên 4 bắt đầu UI.

### Giai đoạn 3 – Tối ưu version (60–90 phút)
- Thành viên 1 sửa prompt/tool declaration và chạy v1/v2/v3.
- Thành viên 2 làm tool mới nếu cần.
- Thành viên 3 phân tích kết quả và viết report.
- Thành viên 4 hoàn thiện UI.

### Giai đoạn 4 – Demo và nộp (30–45 phút)
- Cả nhóm chạy thử lại.
- Kiểm tra không có secret/key trong bài nộp.
- Chuẩn bị bản demo và báo cáo.

---

## 6. Quy tắc làm việc chung

- Mỗi người có trách nhiệm rõ và có deliverable riêng.
- Không sửa cùng lúc cùng một file nếu không cần thiết.
- Mỗi thay đổi phải có bằng chứng từ run/eval.
- Khi hoàn thành một phần, báo cho lead để tổng hợp.
- Không đẩy `.env`, API key, `.venv` hoặc secret lên Git.

---

## 7. Deliverables cuối cùng

- `starter_v0/artifacts/system_prompt.md`
- `starter_v0/artifacts/tools.yaml`
- `starter_v0/artifacts/version_log.csv`
- `starter_v0/artifacts/REPORT.md`
- `starter_v0/data/eval_group.json`
- `starter_v0/runs/*.json`
- `starter_v0/transcripts/*.transcript.json`
- UI chạy được và demo được

$data.results | Where-Object { -not $_.result.passed } | ConvertTo-Json -Depth 8
```

## Bước 2 — cải tiến `v1`

Hypothesis đề xuất: agent sai vì prompt yêu cầu tự đoán và không hỏi lại.

Chỉ sửa:

```text
artifacts/system_prompt.md
artifacts/tools.yaml
```

Các boundary cần diễn đạt rõ:

- thiếu account handle thì gọi `clarify`;
- thiếu URL thì gọi `clarify`;
- gửi/đăng/publish phải hỏi xác nhận yes/no trước;
- không tự bịa handle hoặc URL;
- có thể gọi nhiều tool nếu request có nhiều intent;
- không gọi research tool cho câu hỏi ngoài phạm vi.

Chạy:

```powershell
python run_eval.py --provider openai --version v1 --suite base --eval-cases data/eval_base.json
```

## Bước 3 — cải tiến `v2`

Hypothesis đề xuất: routing/arguments sai vì mô tả tool còn mơ hồ.

Làm rõ trong `artifacts/tools.yaml`:

- `timeline`: dùng khi người dùng yêu cầu bài của một tài khoản cụ thể; `screenname` không có `@`;
- `social_search`: dùng cho tìm bài theo chủ đề/từ khóa; “top/phổ biến” → `search_type=Top`;
- `lookup`: dùng web; “hôm nay” → `topic=news`, `timeframe=day`; “tuần này” → `timeframe=week`;
- `fetch`: chỉ dùng khi có URL cụ thể;
- `format`: chỉ format các items đã có, không dùng để research;
- `clarify`: dùng khi thiếu field bắt buộc hoặc cần xác nhận.

Chạy:

```powershell
python run_eval.py --provider openai --version v2 --suite base --eval-cases data/eval_base.json
```

## Bước 4 — cải tiến `v3`

Chờ kết quả group eval và feedback demo. Tập trung vào:

- correction ở multi-turn ghi đè thông tin cũ;
- thông tin không bị sửa vẫn được giữ lại;
- chỉ xử lý latest user turn;
- gọi đủ nhiều tool khi request có nhiều intent;
- không gọi tool thừa.

Chạy:

```powershell
python run_eval.py --provider openai --version v3 --suite base --eval-cases data/eval_base.json
python run_eval.py --provider openai --version v3 --suite group --eval-cases data/eval_group.json
```

## Bước 5 — version log

Mở:

```text
artifacts/version_log.csv
```

Mỗi version phải có:

```text
version,author,changed_artifact,artifact_version,prompt_hash,tools_hash,reason,hypothesis,metric_name,metric_before,metric_after,run_file
```

`artifact_version`, `prompt_hash`, `tools_hash` và `run_file` phải lấy từ run thật, không tự đặt.

## Bàn giao

- run JSON của `v0`, `v1`, `v2`, `v3`;
- bảng metric trước/sau;
- danh sách failed cases đáng chú ý;
- `version_log.csv` đầy đủ;
- commit/PR không chứa `.env`.

---

# 6. Thành viên 2 — Tool Developer

## Trách nhiệm

1. Thiết kế ít nhất một tool mới do nhóm tự viết.
2. Viết `TOOL.md` và implementation.
3. Đăng ký tool.
4. Phối hợp với Thành viên 1 để thêm declaration.
5. Smoke-test tool trực tiếp.
6. Cung cấp evidence cho report và demo.

## Tool gợi ý: `extract_keywords`

Tool nhận text và trả về các keyword phổ biến. Tool này:

- không cần API key;
- dễ test;
- có thể demo sau khi fetch nội dung;
- không trùng hoàn toàn với tool `format`.

Cấu trúc:

```text
tools/
  extract_keywords/
    TOOL.md
    tool.py
```

## Contract đề xuất

Input:

```json
{
  "text": "Nội dung cần phân tích",
  "max_keywords": 8
}
```

Output:

```json
{
  "tool": "extract_keywords",
  "keywords": [
    {"keyword": "agent", "count": 4}
  ],
  "error": null
}
```

## File `TOOL.md`

Nội dung cần mô tả:

- tool làm gì;
- khi nào dùng;
- khi nào không dùng;
- input/output;
- có side effect hay không.

## Đăng ký implementation

Trong `tools/__init__.py`:

```python
from .extract_keywords.tool import extract_keywords
```

Thêm vào registry:

```python
TOOL_FUNCTIONS = {
    # các tool hiện có...
    "extract_keywords": extract_keywords,
}
```

Phối hợp với Thành viên 1 để thêm declaration vào:

```text
artifacts/tools.yaml
```

Không tự sửa cùng lúc với Thành viên 1. Có thể gửi đoạn YAML qua PR hoặc tin nhắn để Lead tích hợp.

## Smoke test

```powershell
cd starter_v0
.\.venv\Scripts\Activate.ps1
python -c "from tools import TOOL_FUNCTIONS as T; r=T['extract_keywords'](text='AI agents use tools. Tools help AI agents research.', max_keywords=3); print(r)"
```

PASS khi:

- registry tìm thấy tool;
- không có exception;
- `keywords` không rỗng;
- số keyword không vượt `max_keywords`;
- output đúng contract.

## Test syntax toàn project

```powershell
python -m compileall agent.py chat.py run_eval.py tools
```

## Bàn giao

- `tools/extract_keywords/TOOL.md`;
- `tools/extract_keywords/tool.py`;
- registry đã cập nhật;
- declaration YAML đã được Lead tích hợp;
- câu lệnh và output smoke-test;
- ít nhất một group eval case sử dụng tool mới;
- commit/PR riêng.

---

# 7. Thành viên 3 — Group Eval, Analysis và Report

## Trách nhiệm

1. Viết đúng 10 group eval cases.
2. Bảo đảm 5 single-turn và 5 multi-turn.
3. Không sửa `data/eval_base.json`.
4. Phân tích run `v0`–`v3`.
5. Viết `artifacts/REPORT.md`.

## Bước 1 — đọc schema mẫu

```powershell
cd starter_v0
Get-Content -Raw .\samples\eval_group.schema.example.json
```

## Quy tắc `eval_group.json`

File phải có đúng 10 case:

- 5 case dùng `query`;
- 5 case dùng `turns`;
- mọi case có `"phase": "B"`;
- phần tử cuối trong `turns` là user turn đang được chấm;
- mỗi case có `metadata.what_it_tests`;
- dùng `tool_calls` hoặc `no_tool=true`.

`failure_type` chỉ được dùng:

```text
wrong_tool
wrong_arg_value
wrong_boundary
unnecessary_tool
out_of_scope
missing_info
```

## Kiểm tra số lượng và cấu trúc

```powershell
$data = Get-Content -Raw .\data\eval_group.json | ConvertFrom-Json
"Total: $($data.cases.Count)"
"Single-turn: $(($data.cases | Where-Object { $_.query }).Count)"
"Multi-turn: $(($data.cases | Where-Object { $_.turns }).Count)"
```

Kết quả bắt buộc:

```text
Total: 10
Single-turn: 5
Multi-turn: 5
```

Kiểm tra phase:

```powershell
$data.cases | Where-Object { $_.phase -ne 'B' } | Format-Table id,phase
```

Không được có output.

Kiểm tra turn cuối:

```powershell
$data.cases | Where-Object { $_.turns } | ForEach-Object {
    [PSCustomObject]@{
        id = $_.id
        last_role = $_.turns[-1].role
        last_content = $_.turns[-1].content
    }
} | Format-Table -Wrap
```

`last_role` phải là `user`.

## Gợi ý phân bố 10 cases

| Case | Loại | Nội dung kiểm tra |
|---|---|---|
| G01 | Single | Phân biệt timeline và social search |
| G02 | Single | Mapping “hôm nay” sang news/day |
| G03 | Single | Thiếu URL phải clarify |
| G04 | Single | No-tool cho request ngoài phạm vi |
| G05 | Single | Tool mới của nhóm |
| G06 | Multi | Giữ limit từ lượt trước |
| G07 | Multi | User sửa account handle |
| G08 | Multi | Bổ sung URL sau clarification |
| G09 | Multi | Chuyển từ social sang web lookup |
| G10 | Multi | Xác nhận trước action |

## Chạy group eval

Sau khi Lead đã có version cần test:

```powershell
python run_eval.py --provider openai --version v2 --suite group --eval-cases data/eval_group.json
```

Final:

```powershell
python run_eval.py --provider openai --version v3 --suite group --eval-cases data/eval_group.json
```

## Parse runs thành CSV

```powershell
python scripts/parse_runs.py runs/ --output analysis/all_runs.csv
```

## Viết report

Mở:

```text
artifacts/REPORT.md
```

### Phần A

- tên nhóm và thành viên;
- agent giải quyết vấn đề gì;
- danh sách core tool và tool mới;
- 3–5 câu hỏi mẫu;
- 3–5 kịch bản demo;
- link UI nếu có.

### Phần B

- bảng metrics `v0`–`v3`;
- hypothesis của từng version;
- failure analysis có case ID và evidence;
- mô tả 10 group eval cases;
- live chat evidence;
- smoke-test tool mới;
- reflection: điều gì cải thiện, điều gì chưa tốt.

Không điền metrics theo cảm giác. Mọi số liệu phải lấy từ run JSON.

## Bàn giao

- `data/eval_group.json` đúng 10 cases;
- `analysis/all_runs.csv`;
- `artifacts/REPORT.md`;
- bảng case fail và nhận xét;
- commit/PR riêng.

---

# 8. Thành viên 4 — UI, Transcript và Demo

## Trách nhiệm

1. Xây UI bằng Streamlit.
2. Tái sử dụng `run_model_tool_loop` trong `chat.py`.
3. Hiển thị request, response, tool trace, args, result/error và version.
4. Lưu transcript.
5. Chuẩn bị 3–5 kịch bản demo.
6. Kiểm tra UI local và link tạm nếu cần.

## Bước 1 — cài Streamlit

```powershell
cd starter_v0
.\.venv\Scripts\Activate.ps1
python -m pip install "streamlit>=1.30.0"
```

Thêm dòng sau vào `requirements.txt`:

```text
streamlit>=1.30.0
```

## Bước 2 — tạo `app.py`

UI phải import và dùng:

```python
from chat import run_model_tool_loop
```

Không viết một agent loop riêng.

UI tối thiểu phải có:

- ô nhập request;
- lựa chọn provider `openai`;
- version, mặc định `v3`;
- câu trả lời cuối;
- status;
- từng round;
- tool name;
- arguments;
- tool result hoặc error;
- artifact version/prompt hash/tools hash;
- lưu transcript JSON;
- không hiển thị API key.

Các helper có thể tái sử dụng:

```python
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import build_artifact_version, artifact_version_dict
from chat import run_model_tool_loop
```

## Bước 3 — chạy UI

```powershell
streamlit run app.py
```

PASS khi:

- terminal không có exception;
- mở được `http://localhost:8501`;
- gửi được request;
- thấy response;
- thấy tool trace và args;
- tool error được hiển thị rõ;
- transcript được lưu.

## Bước 4 — chạy CLI live chat để tạo evidence

```powershell
python chat.py --provider openai --version v3
```

Thử tối thiểu:

1. Research bình thường:

```text
Tìm tin AI nổi bật hôm nay và tóm tắt 3 kết quả.
```

2. Thiếu thông tin:

```text
Tóm tắt 5 tweet mới nhất giúp mình.
```

Sau khi agent hỏi, trả lời:

```text
Của Sam Altman.
```

3. Boundary hành động:

```text
Đăng bản tin này lên Telegram giúp mình.
```

Agent phải hỏi xác nhận, không tự gửi.

Transcript nằm trong:

```text
transcripts/*.transcript.json
```

## Bước 5 — public link tạm, chỉ khi cần

Sau khi UI chạy:

```powershell
winget install --id Cloudflare.cloudflared
cloudflared tunnel --url http://localhost:8501
```

Lấy URL `trycloudflare.com`, test từ thiết bị khác và gửi link cho Thành viên 3 điền Report A.

Không nhập dữ liệu nhạy cảm vào UI public. Tắt tunnel sau demo.

## Bàn giao

- `app.py`;
- `requirements.txt` có Streamlit;
- ảnh hoặc video ngắn chứng minh UI chạy;
- transcript của ba tình huống;
- 3–5 kịch bản demo;
- URL demo nếu dùng tunnel;
- commit/PR riêng.

---

# 9. Thứ tự phối hợp để không bị chờ nhau

| Thời điểm | Thành viên 1 | Thành viên 2 | Thành viên 3 | Thành viên 4 |
|---|---|---|---|---|
| Giai đoạn 1 | Chạy `v0`, đọc lỗi | Thiết kế tool mới | Đọc schema, phác thảo 10 cases | Cài Streamlit, đọc `chat.py` |
| Giai đoạn 2 | Làm và chạy `v1` | Code + smoke-test tool | Hoàn thành 10 cases | Tạo UI khung và trace |
| Giai đoạn 3 | Tích hợp tool, chạy `v2` | Fix theo review | Chạy group eval, viết Report A | Test UI và demo scenarios |
| Giai đoạn 4 | Làm `v3`, version log | Bổ sung evidence tool | Hoàn thiện Report B | Tạo transcript, tunnel/demo |
| Final gate | Review và merge | Review tool files | Kiểm tra deliverables | Kiểm tra UI/link |

Điểm đồng bộ:

1. Thành viên 1 chạy `v0` trước khi bất kỳ ai sửa prompt.
2. Thành viên 2 báo tên và schema tool mới trước khi Thành viên 3 viết case G05.
3. Thành viên 3 hoàn tất group eval trước vòng `v3`.
4. Thành viên 4 chỉ khóa UI sau khi prompt/tools `v3` đã ổn định.

---

# 10. Checklist họp nhóm ngắn

Mỗi lần cập nhật, từng người báo theo mẫu:

```text
Đã làm:
- ...

Evidence:
- command: ...
- output/file: ...

Đang vướng:
- ...

Việc tiếp theo:
- ...

Branch/commit:
- ...
```

Không báo “đã xong” nếu chưa có command output, run JSON, transcript, screenshot UI hoặc commit tương ứng.

---

# 11. Final gate trước khi nộp

Chạy từ `starter_v0`:

```powershell
python -m compileall agent.py chat.py run_eval.py app.py providers tools scripts
```

Kiểm tra group eval:

```powershell
$data = Get-Content -Raw .\data\eval_group.json | ConvertFrom-Json
"Total=$($data.cases.Count)"
"Single=$(($data.cases | Where-Object { $_.query }).Count)"
"Multi=$(($data.cases | Where-Object { $_.turns }).Count)"
```

Kiểm tra artifacts:

```powershell
Get-Item `
  .\artifacts\system_prompt.md, `
  .\artifacts\tools.yaml, `
  .\artifacts\version_log.csv, `
  .\artifacts\REPORT.md, `
  .\data\eval_group.json, `
  .\app.py
```

Kiểm tra evidence:

```powershell
Get-ChildItem .\runs\*.json
Get-ChildItem .\transcripts\*.transcript.json
```

Kiểm tra Git và secrets:

```powershell
git status --short
git ls-files | Select-String -Pattern '(^|/)\.env$|\.venv|__pycache__'
```

Lệnh thứ hai không được liệt kê `.env`, `.venv` hoặc cache.

Kiểm tra ít nhất các deliverable sau:

- [ ] Provider preflight PASS.
- [ ] `lookup`, `fetch`, `timeline`, `social_search` smoke-test PASS.
- [ ] Có run hợp lệ cho `v0`, `v1`, `v2`, `v3`.
- [ ] Mỗi version là một thay đổi/hypothesis thật.
- [ ] `version_log.csv` có đủ evidence và hash.
- [ ] Có ít nhất một tool mới do nhóm viết.
- [ ] Tool mới có `TOOL.md`, implementation, registry và declaration.
- [ ] Tool mới smoke-test PASS.
- [ ] `eval_group.json` có đúng 5 single-turn và 5 multi-turn.
- [ ] Group eval đã chạy bằng `v3`.
- [ ] UI chạy được và hiển thị trace.
- [ ] Có ít nhất ba live-chat scenarios và transcript.
- [ ] Report A và Report B hoàn chỉnh.
- [ ] Không có API key hoặc `.env` trong Git.
- [ ] Tất cả PR đã merge vào branch `viet`.

Lead chạy lần cuối:

```powershell
git switch viet
git pull --ff-only origin viet
git status
```

Sau đó chạy lại preflight, base eval/group eval cần thiết và UI trên chính branch `viet` để xác nhận bản tích hợp cuối hoạt động.
