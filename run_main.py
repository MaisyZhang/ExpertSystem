import sys
from PyQt5.QtWidgets import *
import main_window, allRules, addRules, inference_engine

rules_filepath = 'rules.txt'


class showRules_window_ui(QMainWindow, allRules.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        allRules.Ui_MainWindow.__init__(self)
        self.setupUi(self)


class addRules_window_ui(QMainWindow, addRules.Ui_MainWindow):
    def __init__(self, rules_filepath):
        QMainWindow.__init__(self)
        addRules.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.rules_filepath = rules_filepath
        self.pushButton.clicked.connect(self.addRules_subwindow)
        self.pushButton_2.clicked.connect(self.close)

    def handle_click(self):
        if not self.isVisible():
            self.show()
            self.textEdit.clear()
            self.textEdit_2.clear()
            self.textEdit_3.clear()

    def addRules_subwindow(self):
        input_ = self.textEdit.toPlainText()
        temp_new_rule = []
        temp_new_rule.append('{')
        if_part = input_.split('\n')
        temp_new_rule.append('IF: {if_part}'.format(if_part=if_part))
        then_part = '\'' + self.textEdit_2.toPlainText() + '\''
        temp_new_rule.append('THEN: {then_part}'.format(then_part=then_part))
        desc_part = '\'' + self.textEdit_3.toPlainText() + '\''
        temp_new_rule.append('DESCRIPTION: {desc_part}'.format(desc_part=desc_part))
        temp_new_rule.append('}')
        RD = open(self.rules_filepath, 'a', encoding='UTF-8')
        for r in temp_new_rule:
            RD.write(r)
            RD.write('\n')

        RD.close()

        self.close()


class main_window_ui(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, rules_filepath):
        QMainWindow.__init__(self)
        main_window.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.rules_filepath = rules_filepath
        # 推理
        self.pushButton_4.clicked.connect(self.infer)
        # 查看规则库
        self.showRules_window = showRules_window_ui()
        self.pushButton_2.clicked.connect(self.showRules)
        # 退出程序
        self.pushButton_3.clicked.connect(self.exit)

    def infer(self):
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.textBrowser_3.clear()
        rules = inference_engine.read_rules(self.rules_filepath)
        input_facts = self.textEdit.toPlainText()
        input_facts = input_facts.split(' ')
        results, infer_rules, visited_rules = inference_engine.inference(rules, input_facts)
        if results is None:
            results = '不能推出任何结果！'
            self.textBrowser_3.append(results)
        else:
            # 推理过程
            for infer_r in infer_rules:
                self.textBrowser.append(infer_r)
            # 触发规则
            for rule in visited_rules:
                self.textBrowser_2.append(str(rule))
            # 推理结果
            self.textBrowser_3.append(results[-1])

    def showRules(self):
        self.showRules_window.show()
        self.showRules_window.textBrowser.clear()
        rules = inference_engine.read_rules(self.rules_filepath)
        for rule in rules:
            self.showRules_window.textBrowser.append(str(rule))

    def exit(self):
        self.close()


def main():
    app = QApplication(sys.argv)
    MAIN = main_window_ui(rules_filepath)
    addRules = addRules_window_ui(rules_filepath)
    MAIN.pushButton.clicked.connect(addRules.handle_click)
    MAIN.show()
    sys.exit(app.exec_())
    pass


if __name__ == '__main__':
    main()