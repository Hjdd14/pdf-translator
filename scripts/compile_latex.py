#!/usr/bin/env python3
"""
LaTeX编译辅助脚本 - 用于PDF翻译skill
将翻译后的LaTeX源文件编译为中文PDF

用法:
    python compile_latex.py <input.tex> [--output-dir <dir>] [--runs <n>]

依赖:
    - XeLaTeX (需要安装TeX Live或MiKTeX)
    - ctex宏包 (中文支持)
"""

import argparse
import os
import subprocess
import sys
import shutil
from pathlib import Path


def check_xelatex():
    """检查xelatex是否可用"""
    try:
        result = subprocess.run(
            ["xelatex", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return False


def check_ctex():
    """检查ctex宏包是否可用"""
    try:
        # 创建一个临时测试文件
        test_tex = r"""\documentclass{article}
\usepackage{ctex}
\begin{document}
\end{document}
"""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test.tex")
            with open(test_file, "w", encoding="utf-8") as f:
                f.write(test_tex)

            result = subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "-output-directory", tmpdir, test_file],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=tmpdir
            )
            return result.returncode == 0
    except Exception:
        return False


def compile_latex(tex_file, output_dir=None, runs=2):
    """
    编译LaTeX文件为PDF

    Args:
        tex_file: LaTeX源文件路径
        output_dir: 输出目录（默认与源文件同目录）
        runs: 编译次数（默认2次，确保交叉引用正确）

    Returns:
        (success: bool, pdf_path: str, log: str)
    """
    tex_path = Path(tex_file).resolve()

    if not tex_path.exists():
        return False, None, f"文件不存在: {tex_path}"

    if output_dir is None:
        output_dir = tex_path.parent
    else:
        output_dir = Path(output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

    # 检查xelatex
    if not check_xelatex():
        return False, None, (
            "错误: 未找到xelatex命令。\n"
            "请安装TeX Live (https://tug.org/texlive/) 或 MiKTeX (https://miktex.org/)\n"
            "Windows用户也可使用 chocolatey: choco install miktex"
        )

    all_logs = []

    for run in range(runs):
        print(f"第 {run + 1}/{runs} 次编译...")

        try:
            result = subprocess.run(
                [
                    "xelatex",
                    "-interaction=nonstopmode",
                    "-output-directory", str(output_dir),
                    str(tex_path)
                ],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(output_dir)
            )

            all_logs.append(result.stdout)

            if result.returncode != 0:
                # 检查log文件中的错误
                log_file = output_dir / (tex_path.stem + ".log")
                if log_file.exists():
                    log_content = log_file.read_text(encoding="utf-8", errors="replace")
                    errors = extract_errors(log_content)
                    if errors:
                        return False, None, f"编译失败:\n{errors}"

                return False, None, f"编译失败 (退出码: {result.returncode})\n{result.stdout[-500:]}"

            print(f"  第 {run + 1} 次编译成功")

        except subprocess.TimeoutExpired:
            return False, None, "编译超时（120秒），请检查LaTeX文件是否有无限循环"
        except Exception as e:
            return False, None, f"编译异常: {str(e)}"

    # 检查PDF是否生成
    pdf_path = output_dir / (tex_path.stem + ".pdf")
    if pdf_path.exists():
        pdf_size = pdf_path.stat().st_size
        print(f"\n编译完成: {pdf_path}")
        print(f"PDF大小: {pdf_size / 1024:.1f} KB")
        return True, str(pdf_path), "\n".join(all_logs)
    else:
        return False, None, "编译成功但未找到PDF文件"


def extract_errors(log_content):
    """从LaTeX log文件中提取错误信息"""
    errors = []
    lines = log_content.split("\n")

    for i, line in enumerate(lines):
        if line.startswith("!"):
            # 收集错误信息及其上下文
            error_lines = [line]
            for j in range(i + 1, min(i + 5, len(lines))):
                if lines[j].strip():
                    error_lines.append(lines[j])
                else:
                    break
            errors.append("\n".join(error_lines))

    return "\n\n".join(errors[:5]) if errors else ""


def clean_aux_files(output_dir, tex_stem):
    """清理编译产生的辅助文件"""
    aux_extensions = [".aux", ".log", ".out", ".toc", ".lof", ".lot",
                      ".bbl", ".blg", ".idx", ".ind", ".ilg", ".nav",
                      ".snm", ".vrb", ".fls", ".fdb_latexmk", ".synctex.gz"]

    cleaned = []
    for ext in aux_extensions:
        aux_file = Path(output_dir) / (tex_stem + ext)
        if aux_file.exists():
            aux_file.unlink()
            cleaned.append(str(aux_file))

    return cleaned


def main():
    parser = argparse.ArgumentParser(description="LaTeX编译辅助脚本")
    parser.add_argument("tex_file", help="LaTeX源文件路径")
    parser.add_argument("--output-dir", "-o", help="输出目录（默认与源文件同目录）")
    parser.add_argument("--runs", "-r", type=int, default=2, help="编译次数（默认2）")
    parser.add_argument("--clean", action="store_true", help="编译后清理辅助文件")
    parser.add_argument("--check", action="store_true", help="仅检查环境，不编译")

    args = parser.parse_args()

    # 环境检查模式
    if args.check:
        print("=== LaTeX环境检查 ===")

        print("\n检查xelatex...")
        if check_xelatex():
            print("  [OK] xelatex可用")
        else:
            print("  [错误] xelatex不可用，请安装TeX Live或MiKTeX")

        print("\n检查ctex宏包...")
        if check_ctex():
            print("  [OK] ctex宏包可用")
        else:
            print("  [错误] ctex宏包不可用")

        print("\n检查Python依赖...")
        for pkg in ["pdfplumber", "pdf2image"]:
            try:
                __import__(pkg)
                print(f"  [OK] {pkg}")
            except ImportError:
                print(f"  [警告] {pkg} 未安装，运行: pip install {pkg}")

        return

    # 编译模式
    success, pdf_path, log = compile_latex(
        args.tex_file,
        output_dir=args.output_dir,
        runs=args.runs
    )

    if success:
        print(f"\n成功: {pdf_path}")

        if args.clean:
            tex_stem = Path(args.tex_file).stem
            out_dir = args.output_dir or str(Path(args.tex_file).parent)
            cleaned = clean_aux_files(out_dir, tex_stem)
            if cleaned:
                print(f"\n已清理 {len(cleaned)} 个辅助文件")
    else:
        print(f"\n失败: {log}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
