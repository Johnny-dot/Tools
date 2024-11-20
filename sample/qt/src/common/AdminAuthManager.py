# AuthManager.py
from PySide6.QtWidgets import QInputDialog, QMessageBox, QLineEdit

class AdminAuthManager:
    def __init__(self):
        self.is_admin = False
        self.admin_password = "123456"

    def prompt_admin_access(self, parent):
        """显示管理员密码输入框"""
        password, ok = QInputDialog.getText(parent, "管理员验证", "请输入管理员密码：", QLineEdit.Password)
        if ok and self.validate_password(password):
            self.is_admin = True
        else:
            QMessageBox.warning(parent, "验证失败", "密码错误，无法进入管理员模式！")

    def validate_password(self, password):
        """验证输入的密码是否正确"""
        return password == self.admin_password

    def is_admin_authenticated(self):
        """检查是否已验证为管理员"""
        return self.is_admin

# 模块级单例
AuthManager = AdminAuthManager()
