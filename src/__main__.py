from ui.main_window import MainWindow
from xor_ops import encrypt_string, decrypt_string

def main():
    decrypt_string("380429412409351335413d002404", "Password1")
    root = MainWindow()
    root.mainloop()

if __name__ == "__main__":
    main()