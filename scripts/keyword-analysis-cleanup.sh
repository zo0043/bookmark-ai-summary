#!/bin/bash
# 关键词分析系统清理脚本
# 使用方法: ./scripts/keyword-analysis-cleanup.sh [选项]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# 默认配置
DRY_RUN=false
BACKUP_BEFORE_CLEAN=true
DAYS_TO_KEEP_BACKUP=30
MIN_REPORT_SIZE=100  # 最小报告大小（字节）
EMPTY_REPORT_ONLY=true

# 显示帮助信息
show_help() {
    cat << EOF
关键词分析系统清理脚本

用法: $0 [选项]

选项:
    -h, --help              显示此帮助信息
    -n, --dry-run           预览模式，不执行实际删除操作
    --no-backup            清理前不创建备份
    --backup-days N        保留 N 天的备份文件 (默认: 30)
    --min-size N           删除小于 N 字节的报告 (默认: 100)
    --all-reports          删除所有报告，不仅限于空报告
    --force                强制清理，跳过确认

示例:
    $0                     # 清理空报告和旧备份
    $0 -n                  # 预览将要清理的内容
    $0 --all-reports       # 清理所有小报告
    $0 --min-size 50       # 删除小于50字节的报告
    $0 --no-backup         # 清理前不备份
EOF
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -n|--dry-run)
            DRY_RUN=true
            shift
            ;;
        --no-backup)
            BACKUP_BEFORE_CLEAN=false
            shift
            ;;
        --backup-days)
            DAYS_TO_KEEP_BACKUP="$2"
            shift 2
            ;;
        --min-size)
            MIN_REPORT_SIZE="$2"
            shift 2
            ;;
        --all-reports)
            EMPTY_REPORT_ONLY=false
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        *)
            echo -e "${RED}未知选项: $1${NC}"
            echo "使用 -h 或 --help 查看帮助信息"
            exit 1
            ;;
    esac
done

# 确认函数
confirm_action() {
    if [ "$FORCE" = true ]; then
        return 0
    fi

    if [ "$DRY_RUN" = true ]; then
        return 0
    fi

    echo -e "${YELLOW}确认执行此操作吗? (y/N)${NC}"
    read -r response
    case "$response" in
        [yY][eE][sS]|[yY])
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# 创建备份
create_backup() {
    if [ "$BACKUP_BEFORE_CLEAN" = false ]; then
        return 0
    fi

    echo -e "${BLUE}创建备份...${NC}"
    local backup_dir="backups/keyword-analysis-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$backup_dir"

    # 备份索引文件
    if [ -f "data/keyword_index.json" ]; then
        cp "data/keyword_index.json" "$backup_dir/"
        echo -e "${GREEN}✅ 已备份关键词索引${NC}"
    fi

    # 备份分析索引
    if [ -f "keyword_analysis_summary.md" ]; then
        cp "keyword_analysis_summary.md" "$backup_dir/"
        echo -e "${GREEN}✅ 已备份分析索引${NC}"
    fi

    # 备份报告目录
    if [ -d "data/keyword_analysis" ]; then
        cp -r "data/keyword_analysis" "$backup_dir/"
        echo -e "${GREEN}✅ 已备份分析报告${NC}"
    fi

    echo -e "${GREEN}备份完成: $backup_dir${NC}"
}

# 清理空报告
clean_empty_reports() {
    echo -e "${BLUE}检查空报告文件...${NC}"

    if [ ! -d "data/keyword_analysis" ]; then
        echo -e "${YELLOW}⚠️  分析报告目录不存在${NC}"
        return 0
    fi

    local empty_count=0
    local total_size=0

    while IFS= read -r -d '' file; do
        local file_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)

        if [ "$EMPTY_REPORT_ONLY" = true ]; then
            # 只删除空文件
            if [ "$file_size" -eq 0 ]; then
                echo "  删除空报告: $(basename "$file")"
                ((empty_count++))

                if [ "$DRY_RUN" = false ]; then
                    rm "$file"
                fi
            fi
        else
            # 删除小于指定大小的文件
            if [ "$file_size" -lt "$MIN_REPORT_SIZE" ]; then
                echo "  删除小报告: $(basename "$file") ($file_size 字节)"
                ((empty_count++))
                ((total_size += file_size))

                if [ "$DRY_RUN" = false ]; then
                    rm "$file"
                fi
            fi
        fi
    done < <(find "data/keyword_analysis" -name "*.md" -type f -print0)

    if [ "$empty_count" -gt 0 ]; then
        echo -e "${GREEN}✅ 清理完成 $empty_count 个报告文件${NC}"
        if [ "$EMPTY_REPORT_ONLY" = false ] && [ "$total_size" -gt 0 ]; then
            echo -e "${GREEN}   释放空间: $((total_size/1024)) KB${NC}"
        fi
    else
        echo -e "${GREEN}✅ 没有需要清理的报告文件${NC}"
    fi
}

# 清理旧备份
clean_old_backups() {
    echo -e "${BLUE}清理旧备份文件...${NC}"

    if [ ! -d "backups" ]; then
        echo -e "${GREEN}✅ 备份目录不存在，无需清理${NC}"
        return 0
    fi

    local backup_count=0
    local total_size=0

    while IFS= read -r -d '' backup; do
        local backup_size=$(du -s "$backup" 2>/dev/null | cut -f1)
        echo "  删除旧备份: $(basename "$backup") ($(($backup_size/1024)) MB)"
        ((backup_count++))
        ((total_size += backup_size))

        if [ "$DRY_RUN" = false ]; then
            rm -rf "$backup"
        fi
    done < <(find "backups" -name "keyword-analysis-*" -type d -mtime +$DAYS_TO_KEEP_BACKUP -print0)

    if [ "$backup_count" -gt 0 ]; then
        echo -e "${GREEN}✅ 清理完成 $backup_count 个旧备份${NC}"
        echo -e "${GREEN}   释放空间: $((total_size/1024/1024)) MB${NC}"
    else
        echo -e "${GREEN}✅ 没有超过 $DAYS_TO_KEEP_BACKUP 天的备份文件${NC}"
    fi
}

# 清理临时文件
clean_temp_files() {
    echo -e "${BLUE}清理临时文件...${NC}"

    local temp_count=0

    # 清理 Python 缓存文件
    while IFS= read -r -d '' file; do
        echo "  删除缓存文件: $(basename "$file")"
        ((temp_count++))

        if [ "$DRY_RUN" = false ]; then
            rm "$file"
        fi
    done < <(find . -name "__pycache__" -type d -print0; find . -name "*.pyc" -type f -print0)

    # 清理日志文件（可选）
    if [ -f "keyword_analysis.log" ]; then
        local log_size=$(stat -f%z "keyword_analysis.log" 2>/dev/null || stat -c%s "keyword_analysis.log" 2>/dev/null)
        if [ "$log_size" -gt 10485760 ]; then  # 10MB
            echo "  清理大日志文件: keyword_analysis.log ($(($log_size/1024/1024)) MB)"
            ((temp_count++))

            if [ "$DRY_RUN" = false ]; then
                # 保留最后1000行
                tail -1000 "keyword_analysis.log" > "keyword_analysis.log.tmp"
                mv "keyword_analysis.log.tmp" "keyword_analysis.log"
            fi
        fi
    fi

    if [ "$temp_count" -gt 0 ]; then
        echo -e "${GREEN}✅ 清理完成 $temp_count 个临时文件${NC}"
    else
        echo -e "${GREEN}✅ 没有需要清理的临时文件${NC}"
    fi
}

# 优化索引文件
optimize_index() {
    echo -e "${BLUE}优化索引文件...${NC}"

    if [ ! -f "data/keyword_index.json" ]; then
        echo -e "${YELLOW}⚠️  索引文件不存在${NC}"
        return 0
    fi

    # 检查索引完整性
    if python -c "import json; data=json.load(open('data/keyword_index.json')); print('OK')" 2>/dev/null; then
        echo -e "${GREEN}✅ 索引文件格式正确${NC}"

        # 重新格式化索引文件
        if [ "$DRY_RUN" = false ]; then
            python -c "
import json
with open('data/keyword_index.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
with open('data/keyword_index.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
print('索引文件已重新格式化')
"
        fi
    else
        echo -e "${RED}❌ 索引文件损坏，需要重建${NC}"
        echo "建议运行: python -m bookmark_ai_summary.run_keyword_analysis --force-rebuild"
    fi
}

# 显示清理统计
show_stats() {
    echo -e "${BLUE}清理统计信息:${NC}"

    if [ -d "data/keyword_analysis" ]; then
        local report_count=$(find "data/keyword_analysis" -name "*.md" -type f 2>/dev/null | wc -l)
        echo "当前分析报告数量: $report_count"
    fi

    if [ -f "data/keyword_index.json" ]; then
        local index_size=$(stat -f%z "data/keyword_index.json" 2>/dev/null || stat -c%s "data/keyword_index.json" 2>/dev/null)
        echo "索引文件大小: $((index_size/1024)) KB"
    fi

    if [ -d "backups" ]; then
        local backup_count=$(find "backups" -name "keyword-analysis-*" -type d 2>/dev/null | wc -l)
        echo "备份文件数量: $backup_count"
    fi
}

# 主函数
main() {
    echo -e "${BLUE}=== 关键词分析系统清理工具 ===${NC}"
    echo "项目路径: $PROJECT_ROOT"
    echo "清理时间: $(date)"
    echo

    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}🔍 预览模式 - 不会执行实际删除操作${NC}"
        echo
    fi

    # 显示当前统计
    show_stats
    echo

    # 确认清理操作
    if [ "$DRY_RUN" = false ]; then
        echo -e "${BLUE}将要执行以下清理操作:${NC}"
        echo "1. 创建数据备份"
        echo "2. 清理${EMPTY_REPORT_ONLY:+空}${EMPTY_REPORT_ONLY:-小}报告文件"
        echo "3. 清理 ${DAYS_TO_KEEP_BACKUP} 天前的备份文件"
        echo "4. 清理临时文件"
        echo "5. 优化索引文件格式"
        echo

        if ! confirm_action; then
            echo -e "${YELLOW}操作已取消${NC}"
            exit 0
        fi
    else
        echo -e "${BLUE}预览以下清理操作:${NC}"
        echo "1. 将创建数据备份"
        echo "2. 将清理${EMPTY_REPORT_ONLY:+空}${EMPTY_REPORT_ONLY:-小}报告文件"
        echo "3. 将清理 ${DAYS_TO_KEEP_BACKUP} 天前的备份文件"
        echo "4. 将清理临时文件"
        echo "5. 将优化索引文件格式"
        echo
    fi

    # 执行清理操作
    create_backup
    clean_empty_reports
    clean_old_backups
    clean_temp_files
    optimize_index

    echo
    if [ "$DRY_RUN" = true ]; then
        echo -e "${BLUE}=== 预览完成 ===${NC}"
        echo "使用不带 -n 参数运行以执行实际清理"
    else
        echo -e "${GREEN}=== 清理完成 ===${NC}"
    fi

    echo
    show_stats
}

# 运行主函数
main "$@"