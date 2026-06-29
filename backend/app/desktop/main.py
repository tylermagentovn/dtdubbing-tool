import customtkinter as ctk

from app.desktop.app_shell import AppShell

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


def main() -> None:
    app = AppShell()
    app.mainloop()


if __name__ == "__main__":
    main()
