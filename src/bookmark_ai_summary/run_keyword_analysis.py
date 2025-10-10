#!/usr/bin/env python3
# 使用方法:
# 基本运行（增量更新）:
#   python -m bookmark_ai_summary.run_keyword_analysis
#
# 强制重建索引:
#   python -m bookmark_ai_summary.run_keyword_analysis --force-rebuild
#
# 自定义最小频次:
#   python -m bookmark_ai_summary.run_keyword_analysis --min-frequency 5

import argparse
import logging
from keyword_analyzer import process_keyword_analysis

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    parser = argparse.ArgumentParser(
        description="关键词分析系统 - 自动提取书签关键词并生成深度分析报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 增量更新（推荐）
  python -m bookmark_ai_summary.run_keyword_analysis

  # 强制重建全部索引
  python -m bookmark_ai_summary.run_keyword_analysis --force-rebuild

  # 仅分析频次≥5的关键词
  python -m bookmark_ai_summary.run_keyword_analysis --min-frequency 5

输出文件:
  - data/keyword_index.json          # 关键词倒排索引
  - data/keyword_analysis/*.md        # 各关键词分析报告
  - keyword_analysis_summary.md       # 分析报告索引
        """
    )

    parser.add_argument(
        '--force-rebuild',
        action='store_true',
        help='强制重建关键词索引（默认为增量更新）'
    )

    parser.add_argument(
        '--min-frequency',
        type=int,
        default=3,
        metavar='N',
        help='最小关键词频次，低于此值不生成报告（默认: 3）'
    )

    args = parser.parse_args()

    logging.info("启动关键词分析系统")
    logging.info(f"参数: force_rebuild={args.force_rebuild}, min_frequency={args.min_frequency}")

    try:
        process_keyword_analysis(
            force_rebuild=args.force_rebuild,
            min_frequency=args.min_frequency
        )
        logging.info("✅ 关键词分析完成！")
        logging.info("查看结果:")
        logging.info("  - 分析报告索引: keyword_analysis_summary.md")
        logging.info("  - 详细报告目录: data/keyword_analysis/")

    except Exception as e:
        logging.error(f"❌ 关键词分析失败: {e}")
        logging.exception(e)
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
