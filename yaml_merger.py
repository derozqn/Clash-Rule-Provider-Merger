import sys
import os
import yaml
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
                            QWidget, QFileDialog, QLabel, QMessageBox, QListWidget,
                            QAbstractItemView, QGroupBox, QComboBox, QStatusBar, QLineEdit,
                            QProgressDialog)
from PyQt5.QtCore import Qt, QSettings, QThread, pyqtSignal

TRANSLATIONS = {
    "ko_KR": {
        "title": "Clash Rule Provider Merger",
        "file_list_group": "병합할 파일",                                               
        "file_list_label": "병합할 YAML 파일 목록:",
        "add_file_btn": "파일 추가",
        "remove_file_btn": "선택 파일 제거",
        "clear_all_btn": "모두 지우기",
        "output_group": "출력 설정",
        "output_label": "출력 파일 이름:",
        "merge_btn": "YAML 파일 병합",
        "status_ready": "준비됨",
        "status_merged": "병합 완료",
        "status_files_loaded": "파일 로드됨: {0}개",
        "error_load_file": "YAML 파일을 불러오는 중 오류가 발생했습니다: {0}",
        "error_merge": "YAML 파일 병합 중 오류가 발생했습니다: {0}",
        "warning_min_files": "병합할 YAML 파일을 2개 이상 선택해주세요.",
        "warning_output_file": "출력 파일 이름을 입력해주세요.",
        "success_merge": "YAML 파일({0}개)이 성공적으로 병합되었습니다: {1}",
        "language": "언어",
        "file_dialog_title": "YAML 파일 선택",
        "progress_title": "병합 진행 중",
        "progress_message": "파일 병합 중...",
        "cancel_button": "취소"
    },
    "zh_CN": {
        "title": "Clash Rule Provider Merger",
        "file_list_group": "要合并的文件",
        "file_list_label": "YAML 文件列表:",
        "add_file_btn": "添加文件",
        "remove_file_btn": "删除所选文件",
        "clear_all_btn": "清除所有",
        "output_group": "输出设置",
        "output_label": "输出文件名称:",
        "merge_btn": "合并 YAML 文件",
        "status_ready": "就绪",
        "status_merged": "合并完成",
        "status_files_loaded": "已加载文件: {0}个",
        "error_load_file": "加载YAML文件时出错: {0}",
        "error_merge": "合并YAML文件时出错: {0}",
        "warning_min_files": "请选择至少2个YAML文件进行合并。",
        "warning_output_file": "请输入输出文件名称。",
        "success_merge": "成功合并YAML文件({0}个): {1}",
        "language": "语言",
        "file_dialog_title": "选择YAML文件",
        "progress_title": "合并进行中",
        "progress_message": "正在合并文件...",
        "cancel_button": "取消"
    },
    "en_US": {
        "title": "Clash Rule Provider Merger",
        "file_list_group": "Files to Merge",
        "file_list_label": "YAML Files List:",
        "add_file_btn": "Add Files",
        "remove_file_btn": "Remove Selected",
        "clear_all_btn": "Clear All",
        "output_group": "Output Settings",
        "output_label": "Output File Name:",
        "merge_btn": "Merge YAML Files",
        "status_ready": "Ready",
        "status_merged": "Merged Successfully",
        "status_files_loaded": "Files loaded: {0}",
        "error_load_file": "Error loading YAML file: {0}",
        "error_merge": "Error merging YAML files: {0}",
        "warning_min_files": "Please select at least 2 YAML files to merge.",
        "warning_output_file": "Please enter an output file name.",
        "success_merge": "Successfully merged {0} YAML files: {1}",
        "language": "Language",
        "file_dialog_title": "Select YAML Files",
        "progress_title": "Merging in Progress",
        "progress_message": "Merging files...",
        "cancel_button": "Cancel"
    }
}

class MergeWorker(QThread):
    finished = pyqtSignal(dict, str)
    error = pyqtSignal(Exception)
    progress = pyqtSignal(int)
    
    def __init__(self, file_contents, output_path):
        super().__init__()
        self.file_contents = file_contents
        self.output_path = output_path
        
    def run(self):
        try:
            # 10% 진행 상태 - 시작
            self.progress.emit(10)
            
            # Merge payload items
            merged = self.file_contents[0].copy()
            merged_payload = []
            all_files_have_payload = all('payload' in yaml_file for yaml_file in self.file_contents)
            
            if all_files_have_payload:
                unique_domains = set()
                total_files = len(self.file_contents)
                
                # 40% 진행 상태 - 항목 수집 시작
                self.progress.emit(20)
                
                # 각 파일의 항목 수집
                for i, yaml_file in enumerate(self.file_contents):
                    for item in yaml_file['payload']:
                        item_str = str(item)
                        if item_str not in unique_domains:
                            unique_domains.add(item_str)
                            merged_payload.append(item)
                    
                    # 파일별 진행 상태 업데이트 (20%~50%)
                    progress = 20 + int((i + 1) / total_files * 30)
                    self.progress.emit(progress)
                
                # 60% 진행 상태 - 정렬 시작
                self.progress.emit(60)
                
                # 항목 정렬
                merged_payload.sort(key=lambda x: str(x).lower())
                merged['payload'] = merged_payload
                
                # 70% 진행 상태 - 통계 계산 시작
                self.progress.emit(70)
                
                # 통계 정보 계산
                domain_count = sum(1 for item in merged_payload if isinstance(item, str) and item.startswith('DOMAIN,'))
                domain_suffix_count = sum(1 for item in merged_payload if isinstance(item, str) and item.startswith('DOMAIN-SUFFIX,'))
                domain_keyword_count = sum(1 for item in merged_payload if isinstance(item, str) and item.startswith('DOMAIN-KEYWORD,'))
                ip_cidr_count = sum(1 for item in merged_payload if isinstance(item, str) and item.startswith('IP-CIDR,'))
                process_name_count = sum(1 for item in merged_payload if isinstance(item, str) and item.startswith('PROCESS-NAME,'))
                
                merged['DOMAIN'] = domain_count
                merged['DOMAIN-SUFFIX'] = domain_suffix_count
                merged['DOMAIN-KEYWORD'] = domain_keyword_count
                if ip_cidr_count > 0:
                    merged['IP-CIDR'] = ip_cidr_count
                if process_name_count > 0:
                    merged['PROCESS-NAME'] = process_name_count
                
                merged['TOTAL'] = len(merged_payload)
                
                from datetime import datetime
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                merged['UPDATED'] = current_time
                
                # 80% 진행 상태 - 메타데이터 설정 시작
                self.progress.emit(80)
                
                # 출력 파일 이름으로 NAME 설정
                file_name = os.path.basename(self.output_path)
                if file_name.endswith('.yaml') or file_name.endswith('.yml'):
                    file_name = os.path.splitext(file_name)[0]
                merged['NAME'] = file_name
                
                # REPO 값 설정
                merged['REPO'] = "https://github.com/derozqn/Clash-Rule-Provider-Merger"
                
                # 90% 진행 상태 - 파일 쓰기 시작
                self.progress.emit(90)
                
                # 헤더 작성 순서 지정
                header_order = ['NAME', 'REPO', 'UPDATED', 'DOMAIN', 'DOMAIN-KEYWORD', 'DOMAIN-SUFFIX']
                if ip_cidr_count > 0:
                    header_order.append('IP-CIDR')
                if process_name_count > 0:
                    header_order.append('PROCESS-NAME')
                header_order.append('TOTAL')
                
                # 지정된 순서로 헤더 작성
                header_lines = []
                for key in header_order:
                    if key in merged:
                        header_lines.append(f"# {key}: {merged[key]}")
                
                with open(self.output_path, 'w', encoding='utf-8') as f:
                    # 헤더 정보(통계) 작성
                    for line in header_lines:
                        f.write(line + '\n')
                    
                    # payload 섹션 작성
                    f.write("payload:\n")
                    # 각 항목 작성
                    for item in merged['payload']:
                        f.write(f"  - {item}\n")
                
                # 100% 진행 상태 - 완료
                self.progress.emit(100)
                
                # 성공 시그널 발생
                self.finished.emit(merged, self.output_path)
        
        except Exception as e:
            # 오류 시그널 발생
            self.error.emit(e)

class YAMLMerger(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_paths = []
        self.file_contents = []
        self.output_path = None
        self.settings = QSettings("ClashRuleProviderMerger", "ClashRuleProviderMerger")
        self.current_language = self.settings.value("language", "en_US")
        self.merge_worker = None
        self.progress_dialog = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.tr("title"))
        self.setGeometry(100, 100, 500, 500)
        
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        language_layout = QHBoxLayout()
        language_label = QLabel(self.tr("language") + ":")
        self.language_combo = QComboBox()
        self.language_combo.addItem("English", "en_US")
        self.language_combo.addItem("中文", "zh_CN")
        self.language_combo.addItem("한국어", "ko_KR")
        
        index = self.language_combo.findData(self.current_language)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
            
        self.language_combo.currentIndexChanged.connect(self.change_language)
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combo)
        language_layout.addStretch()
        
        main_layout.addLayout(language_layout)
        
        file_group = QGroupBox(self.tr("file_list_group"))
        file_group.setObjectName("file_list_group")
        file_layout = QVBoxLayout()
        
        file_list_label = QLabel(self.tr("file_list_label"))
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.file_list.setAlternatingRowColors(True)
        
        file_btn_layout = QVBoxLayout()
        add_file_btn = QPushButton(self.tr("add_file_btn"))
        add_file_btn.clicked.connect(self.add_file)
        remove_file_btn = QPushButton(self.tr("remove_file_btn"))
        remove_file_btn.clicked.connect(self.remove_file)
        clear_all_btn = QPushButton(self.tr("clear_all_btn"))
        clear_all_btn.clicked.connect(self.clear_all_files)
        
        file_btn_layout.addWidget(add_file_btn)
        file_btn_layout.addWidget(remove_file_btn)
        file_btn_layout.addWidget(clear_all_btn)
        
        file_layout.addWidget(file_list_label)
        file_layout.addWidget(self.file_list)
        file_layout.addLayout(file_btn_layout)
        file_group.setLayout(file_layout)
        
        output_group = QGroupBox(self.tr("output_group"))
        output_group.setObjectName("output_group")
        output_layout = QVBoxLayout()
        
        self.output_label = QLabel(self.tr("output_label"))
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setPlaceholderText("output.yaml")
        self.output_path_edit.textChanged.connect(self.update_output_path)
        
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_path_edit, 1)
        output_group.setLayout(output_layout)
        
        merge_btn = QPushButton(self.tr("merge_btn"))
        merge_btn.setMinimumHeight(40)
        merge_btn.clicked.connect(self.merge_yaml_files)
        
        main_layout.addWidget(file_group)
        main_layout.addWidget(output_group)
        main_layout.addWidget(merge_btn)
        
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage(self.tr("status_ready"))
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def tr(self, key, *args):
        text = TRANSLATIONS.get(self.current_language, {}).get(key, key)
        if args:
            text = text.format(*args)
        return text
    
    def change_language(self):
        self.current_language = self.language_combo.currentData()
        self.settings.setValue("language", self.current_language)
        
        self.setWindowTitle(self.tr("title"))
        
        for widget in self.findChildren(QGroupBox):
            if "file_list_group" in widget.objectName() or widget.title() == "병합할 파일" or widget.title() == "要合并的文件" or widget.title() == "Files to Merge":
                widget.setTitle(self.tr("file_list_group"))
            elif "output_group" in widget.objectName() or widget.title() == "출력 설정" or widget.title() == "输出设置" or widget.title() == "Output Settings":
                widget.setTitle(self.tr("output_group"))
        
        for widget in self.findChildren(QLabel):
            if widget == self.output_label:
                widget.setText(self.tr("output_label"))
            elif widget.text() == "병합할 YAML 파일 목록:" or widget.text() == "YAML 文件列表:" or widget.text() == "YAML Files List:":
                widget.setText(self.tr("file_list_label"))
        
        for widget in self.findChildren(QPushButton):
            if widget.text() == "파일 추가" or widget.text() == "添加文件" or widget.text() == "Add Files":
                widget.setText(self.tr("add_file_btn"))
            elif widget.text() == "선택 파일 제거" or widget.text() == "删除所选文件" or widget.text() == "Remove Selected":
                widget.setText(self.tr("remove_file_btn"))
            elif widget.text() == "모두 지우기" or widget.text() == "清除所有" or widget.text() == "Clear All":
                widget.setText(self.tr("clear_all_btn"))
            elif widget.text() == "YAML 파일 병합" or widget.text() == "合并 YAML 文件" or widget.text() == "Merge YAML Files":
                widget.setText(self.tr("merge_btn"))
        
        if len(self.file_paths) > 0:
            self.statusbar.showMessage(self.tr("status_files_loaded", len(self.file_paths)))
        else:
            self.statusbar.showMessage(self.tr("status_ready"))
    
    def add_file(self):
        options = QFileDialog.Options()
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, 
            self.tr("file_dialog_title"), 
            "", 
            "YAML Files (*.yaml *.yml);;All Files (*)", 
            options=options
        )
        
        if file_paths:
            for file_path in file_paths:
                if file_path not in self.file_paths:
                    self.file_paths.append(file_path)
                    self.file_list.addItem(os.path.basename(file_path))
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = yaml.safe_load(f)
                            self.file_contents.append(content)
                    except Exception as e:
                        QMessageBox.critical(self, 'Error', self.tr("error_load_file", str(e)))
                        self.file_paths.pop()
                        self.file_list.takeItem(self.file_list.count() - 1)
            
            self.statusbar.showMessage(self.tr("status_files_loaded", len(self.file_paths)))
    
    def remove_file(self):
        selected_items = self.file_list.selectedIndexes()
        if not selected_items:
            return
            
        indexes = sorted([item.row() for item in selected_items], reverse=True)
        
        for index in indexes:
            self.file_list.takeItem(index)
            self.file_paths.pop(index)
            self.file_contents.pop(index)
        
        self.statusbar.showMessage(self.tr("status_files_loaded", len(self.file_paths)))
    
    def clear_all_files(self):
        self.file_list.clear()
        self.file_paths = []
        self.file_contents = []
        self.statusbar.showMessage(self.tr("status_ready"))
    
    def update_output_path(self):
        file_name = self.output_path_edit.text().strip()
        if file_name:
            if not (file_name.endswith('.yaml') or file_name.endswith('.yml')):
                file_name += '.yaml'
            
            self.output_path = os.path.join(os.getcwd(), file_name)
        else:
            self.output_path = None
    
    def merge_yaml_files(self):
        if len(self.file_paths) < 2:
            QMessageBox.warning(self, 'Warning', self.tr("warning_min_files"))
            return
            
        if not self.output_path or not self.output_path_edit.text().strip():
            QMessageBox.warning(self, 'Warning', self.tr("warning_output_file"))
            return
            
        # 진행 대화상자 생성
        self.progress_dialog = QProgressDialog(self.tr("progress_message"), self.tr("cancel_button"), 0, 100, self)
        self.progress_dialog.setWindowTitle(self.tr("progress_title"))
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setValue(0)
        self.progress_dialog.show()
        
        # 백그라운드 작업자 생성 및 시작
        self.merge_worker = MergeWorker(self.file_contents, self.output_path)
        self.merge_worker.finished.connect(self.on_merge_finished)
        self.merge_worker.error.connect(self.on_merge_error)
        self.merge_worker.progress.connect(self.update_progress)
        self.merge_worker.start()
        
    def update_progress(self, value):
        if self.progress_dialog and not self.progress_dialog.wasCanceled():
            self.progress_dialog.setValue(value)
            
    def on_merge_finished(self, merged_content, output_path):
        if self.progress_dialog:
            self.progress_dialog.setValue(100)
            self.progress_dialog = None
            
        self.statusbar.showMessage(self.tr("status_merged"))
                
        QMessageBox.information(
            self, 
            'Success', 
            self.tr("success_merge", len(self.file_paths), os.path.basename(output_path))
        )
            
    def on_merge_error(self, exception):
        if self.progress_dialog:
            self.progress_dialog.hide()
            self.progress_dialog = None
            
        QMessageBox.critical(self, 'Error', self.tr("error_merge", str(exception)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    merger = YAMLMerger()
    merger.show()
    sys.exit(app.exec_()) 
