#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TraeReset entrypoint."""

import sys
import traceback
from tkinter import messagebox

from traereset_core import configure_platform
from traereset_ui import App


if __name__ == "__main__":
    try:
        configure_platform()
        app = App()
        app.mainloop()
    except Exception:
        error = traceback.format_exc()
        try:
            messagebox.showerror("启动失败", f"程序异常:\n{error}")
        except Exception:
            pass
        sys.exit(1)
