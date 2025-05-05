# Clash Rule Provider Merger

<div align="center">
  <p>
    <a href="#english">English</a> | 
    <a href="#中文">中文</a> | 
    <a href="#한국어">한국어</a>
  </p>
</div>

---

<a name="english"></a>
## [English]

Clash Rule Provider Merger is a GUI tool for merging and sorting Clash rule provider YAML files.

### Key Features

- Merge multiple YAML files (2 or more)
- Automatic duplicate removal
- Alphabetical and numerical sorting
- Automatic update of header information (NAME, AUTHOR, REPO, etc.)
- Preview of merged results
- Multi-language support (English, Chinese, Korean)
- User-friendly interface

### How to Use

1. Select your preferred language from the top of the screen (English, Chinese, Korean).
2. Click the `Add Files` button to select the YAML files to merge. You can select multiple files at once.
3. If needed, use the `Remove Selected` button to remove files from the list or the `Clear All` button to reset the list.
4. Select the output file location.
5. Click the `Merge YAML Files` button to automatically merge and save the files.
6. Check the merged result in the preview window.
7. View the current operation status in the status bar at the bottom.

### Interface Features

- **Split Screen**: The top section contains the file list and settings, while the bottom section shows the preview area.
- **Multiple Selection**: Select and remove multiple files simultaneously.
- **Status Bar**: Displays the number of loaded files, operation status, etc.
- **Monospaced Font**: The preview uses a highly readable monospaced font.
- **Grouped UI**: Related functions are organized in groups.

### System Requirements

- Python 3.6 or higher
- PyQt5 and PyYAML libraries

### Installation

```bash
pip install PyQt5 PyYAML
python yaml_merger.py
```

---

<a name="中文"></a>
## [中文]

Clash Rule Provider Merger 是一个用于合并和排序 Clash 规则提供程序 YAML 文件的图形界面工具。

### 主要功能

- 合并多个 YAML 文件（2个或更多）
- 自动删除重复项
- 按字母和数字顺序排序
- 自动更新头部信息（NAME, AUTHOR, REPO 等）
- 合并结果预览
- 多语言支持（英文、中文、韩文）
- 用户友好界面

### 使用方法

1. 在屏幕顶部选择您偏好的语言（英文、中文、韩文）。
2. 点击`添加文件`按钮选择要合并的 YAML 文件。您可以一次选择多个文件。
3. 如果需要，使用`删除所选文件`按钮从列表中删除文件，或使用`清除所有`按钮重置列表。
4. 选择输出文件位置。
5. 点击`合并 YAML 文件`按钮自动合并并保存文件。
6. 在预览窗口中查看合并结果。
7. 在底部状态栏查看当前操作状态。

### 界面功能

- **分屏显示**：顶部包含文件列表和设置，底部显示预览区域。
- **多选功能**：同时选择和删除多个文件。
- **状态栏**：显示已加载文件数量、操作状态等。
- **等宽字体**：预览使用高可读性的等宽字体。
- **分组界面**：相关功能按组整理。

### 系统要求

- Python 3.6 或更高版本
- PyQt5 和 PyYAML 库

### 安装方法

```bash
pip install PyQt5 PyYAML
python yaml_merger.py
```

---

<a name="한국어"></a>
## [한국어]

Clash Rule Provider Merger는 Clash 규칙 제공자 YAML 파일을 병합하고 정렬하는 GUI 도구입니다.

### 주요 기능

- 여러 개의 YAML 파일 병합 (2개 이상)
- 중복 항목 자동 제거
- 알파벳 및 숫자 순서로 정렬
- 헤더 정보(NAME, AUTHOR, REPO 등) 자동 업데이트
- 병합 결과 미리보기 제공
- 다국어 지원 (영어, 중국어, 한국어)
- 사용자 친화적인 인터페이스

### 사용 방법

1. 화면 상단에서 원하는 언어를 선택합니다 (영어, 중국어, 한국어).
2. `파일 추가` 버튼을 클릭하여 병합할 YAML 파일을 선택합니다. 한 번에 여러 파일 선택이 가능합니다.
3. 필요한 경우 `선택 파일 제거` 버튼으로 목록에서 파일을 제거하거나 `모두 지우기` 버튼으로 목록을 초기화할 수 있습니다.
4. 출력 파일 위치를 선택합니다.
5. `YAML 파일 병합` 버튼을 클릭하면 자동으로 파일을 병합하고 저장합니다.
6. 미리보기 창에서 병합 결과를 확인할 수 있습니다.
7. 하단 상태 표시줄에서 현재 작업 상태를 확인할 수 있습니다.

### 인터페이스 기능

- **분할 화면**: 상단은 파일 목록과 설정, 하단은 미리보기 영역으로 분할됩니다.
- **다중 선택**: 여러 파일을 동시에 선택하여 제거할 수 있습니다.
- **상태 표시줄**: 현재 로드된 파일 수, 작업 상태 등을 표시합니다.
- **고정폭 폰트**: 미리보기는 가독성 높은 고정폭 폰트로 표시됩니다.
- **그룹화된 UI**: 관련 기능들이 그룹으로 정리되어 있습니다.

### 시스템 요구사항

- Python 3.6 이상
- PyQt5 및 PyYAML 라이브러리

### 설치 방법

```bash
pip install PyQt5 PyYAML
python yaml_merger.py
``` 
