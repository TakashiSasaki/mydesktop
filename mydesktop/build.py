# File: mydesktop/build.py
# Description: Use PyInstaller to build a standalone executable from the `mydesktop` package.

import os
import sys
from PyInstaller.__main__ import run


def main() -> None:
    """
    Build a standalone executable using PyInstaller.
    This will execute: pyinstaller --onefile --name mydesktop path/to/mydesktop/__main__.py [additional args…]
    """
    # 1) パッケージ mydesktop の __main__.py までの絶対パスを計算する
    here = os.path.dirname(__file__)  # mydesktop フォルダ
    target = os.path.join(here, "__main__.py")

    # 2) PyInstaller に渡す引数のリストを作成
    #    --onefile   : 単一の実行ファイルをつくる
    #    --name      : 出力バイナリ名を "mydesktop" にする
    args = [
        "--onefile",
        "--name", "mydesktop",
        target,
    ] + sys.argv[1:]  # 必要に応じてコマンドライン引数を追加で受け取る

    # 3) PyInstaller を実行
    run(args)


if __name__ == "__main__":
    main()
