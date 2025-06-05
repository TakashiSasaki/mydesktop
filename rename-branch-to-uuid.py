import subprocess
import uuid
import sys
import os
import argparse # コマンドライン引数処理のために追加

def run_git_command(command_list):
    """指定されたgitコマンドリストを実行し、標準出力、標準エラー、リターンコードを返します。"""
    try:
        process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=os.getcwd())
        stdout, stderr = process.communicate()
        return stdout.strip(), stderr.strip(), process.returncode
    except FileNotFoundError:
        print("エラー: gitコマンドが見つかりません。gitがインストールされ、パスが通っていることを確認してください。", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"gitコマンド実行中に予期せぬエラーが発生しました ({' '.join(command_list)}): {e}", file=sys.stderr)
        sys.exit(1)

def is_git_repository():
    """カレントディレクトリがgitリポジトリであるかを確認します。"""
    stdout, stderr, returncode = run_git_command(["git", "rev-parse", "--git-dir"])
    if returncode == 0 and stdout: # stdoutに.gitディレクトリのパス(相対または絶対)が返る
        return True
    else:
        # print(f"Gitリポジトリの確認エラー: {stderr}", file=sys.stderr) # デバッグ用
        return False

def get_current_branch_name():
    """現在のブランチ名を取得します。"""
    stdout, stderr, returncode = run_git_command(["git", "branch", "--show-current"])
    if returncode == 0 and stdout:
        return stdout
    
    stdout_fallback, stderr_fallback, returncode_fallback = run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if returncode_fallback == 0 and stdout_fallback:
        if stdout_fallback == "HEAD":
            print("警告: HEADがデタッチ状態です。特定のブランチにはいません。", file=sys.stderr)
            return None
        return stdout_fallback
    
    combined_stderr = f"試行1 (git branch --show-current):\n{stderr}\n\n試行2 (git rev-parse --abbrev-ref HEAD):\n{stderr_fallback}"
    print(f"現在のブランチ名の取得に失敗しました。\n{combined_stderr}", file=sys.stderr)
    return None

def generate_uuidv4():
    """UUIDv4を生成します。"""
    return str(uuid.uuid4())

def rename_branch(old_name, new_name, dry_run=True):
    """ブランチ名を変更します。dry_runがTrueの場合は実際の変更を行いません。"""
    if dry_run:
        print(f"[ドライラン] ブランチ '{old_name}' を '{new_name}' に名前変更する予定です。")
        # ドライランの場合、gitコマンドの事前チェックとしてブランチの存在確認などは行わない
        # (行う場合は read-only の git show-ref --verify refs/heads/old_name など)
        return True # ドライランなので成功したとみなす（実際のエラーは発生しない）
    else:
        print(f"ブランチ名を '{old_name}' から '{new_name}' に変更しようとしています...")
        stdout, stderr, returncode = run_git_command(["git", "branch", "-m", old_name, new_name])
        if returncode == 0:
            print(f"ブランチ名が '{new_name}' に正常に変更されました。")
            if stdout: print(f"  Gitからの標準出力: {stdout}")
            # 成功時でも informational なメッセージが stderr に出ることがある (Gitのバージョンや設定による)
            if stderr: print(f"  Gitからの標準エラー出力: {stderr}")
            return True
        else:
            print(f"エラー: ブランチ名の変更に失敗しました ('{old_name}' -> '{new_name}').", file=sys.stderr)
            if stdout: print(f"  標準出力:\n{stdout}", file=sys.stderr)
            if stderr: print(f"  標準エラー:\n{stderr}", file=sys.stderr)
            # 考えられるエラーケース
            if "already exists" in stderr:
                print("  詳細: 新しいブランチ名 '{new_name}' は既に存在します。", file=sys.stderr)
            elif "branch name invalid" in stderr:
                 print(f"  詳細: 新しいブランチ名 '{new_name}' は無効な名前です。", file=sys.stderr)
            elif f"branch '{old_name}' not found" in stderr:
                 print(f"  詳細: 元のブランチ名 '{old_name}' が見つかりません。", file=sys.stderr)
            return False

def main():
    parser = argparse.ArgumentParser(
        description="現在のブランチが 'master' または 'main' の場合、UUIDv4の名前に変更します。\n"
                    "デフォルトではドライランモードで実行され、実際の変更は行いません。",
        formatter_class=argparse.RawTextHelpFormatter # ヘルプメッセージの改行を保持
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="実際にブランチ名の変更を実行します。このオプションがない場合はドライランモードになります。"
    )
    args = parser.parse_args()

    is_dry_run = not args.execute

    if is_dry_run:
        print("--- ドライランモードで実行します ---")
        print("実際のファイルシステムやGitリポジトリへの変更は行われません。")
        print("実行される予定の操作が表示されます。実際に変更を行うには --execute オプションを使用してください。\n")
    else:
        print("--- 実行モードで実行します ---")
        print("警告: これから実際のGitブランチ名の変更を行います。\n")

    print("Gitリポジトリの確認を開始します...")
    if not is_git_repository():
        print("エラー: カレントディレクトリは有効なGitリポジトリではありません。", file=sys.stderr)
        sys.exit(1)
    print("カレントディレクトリはGitリポジトリです。")

    print("\n現在のブランチ名を取得しています...")
    current_branch = get_current_branch_name()

    if current_branch is None:
        print("エラー: 現在のブランチ名を取得できなかったため、処理を中止します。", file=sys.stderr)
        sys.exit(1)
    
    print(f"現在のブランチ名は: '{current_branch}' です。")

    target_branches = ["master", "main"]
    if current_branch in target_branches:
        print(f"ブランチ '{current_branch}' は変更対象です ({', '.join(target_branches)} のいずれか)。")
        
        new_branch_name_uuid = generate_uuidv4()
        print(f"新しいブランチ名としてUUIDv4を生成しました: '{new_branch_name_uuid}'")
        
        rename_successful = rename_branch(current_branch, new_branch_name_uuid, dry_run=is_dry_run)
        
        if rename_successful:
            if is_dry_run:
                print(f"\n[ドライラン] 処理シミュレーション完了。ブランチ '{current_branch}' は '{new_branch_name_uuid}' に名前が変更される予定でした。")
            else:
                print(f"\n処理完了: ブランチ '{current_branch}' は '{new_branch_name_uuid}' に名前が変更されました。")
        else:
            # rename_branchがFalseを返すのは実行モードで失敗した場合のみ
            print(f"\n処理失敗: ブランチ '{current_branch}' の名前変更に失敗しました。", file=sys.stderr)
            sys.exit(1) # 実行モードでの失敗はエラーとして終了

    else:
        print(f"\n現在のブランチ '{current_branch}' は '{', '.join(target_branches)}' のいずれでもないため、名前は変更されません。")

    if is_dry_run:
        print("\n--- ドライランモード終了 ---")
    else:
        print("\n--- 実行モード終了 ---")


if __name__ == "__main__":
    main()