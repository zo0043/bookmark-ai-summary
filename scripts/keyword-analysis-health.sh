#!/bin/bash
# 关键词分析系统健康检查脚本
# 使用方法: ./scripts/keyword-analysis-health.sh

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

echo -e "${BLUE}=== 关键词分析系统健康检查 ===${NC}"
echo "项目路径: $PROJECT_ROOT"
echo "检查时间: $(date)"
echo

# 检查函数
check_file() {
    local file="$1"
    local description="$2"

    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $description: 存在${NC}"
        return 0
    else
        echo -e "${RED}❌ $description: 不存在${NC}"
        return 1
    fi
}

check_directory() {
    local dir="$1"
    local description="$2"

    if [ -d "$dir" ]; then
        echo -e "${GREEN}✅ $description: 存在${NC}"
        return 0
    else
        echo -e "${RED}❌ $description: 不存在${NC}"
        return 1
    fi
}

check_env() {
    local var="$1"
    local description="$2"

    if [ -n "${!var}" ]; then
        echo -e "${GREEN}✅ $description: 已设置${NC}"
        return 0
    else
        echo -e "${RED}❌ $description: 未设置${NC}"
        return 1
    fi
}

check_python_module() {
    local module="$1"
    local description="$2"

    if python -c "import $module" 2>/dev/null; then
        echo -e "${GREEN}✅ $description: 可导入${NC}"
        return 0
    else
        echo -e "${RED}❌ $description: 导入失败${NC}"
        return 1
    fi
}

# 1. 检查环境配置
echo -e "${BLUE}1. 环境配置检查${NC}"
check_env "OPENAI_API_KEY" "OpenAI API Key"
if [ -n "$OPENAI_API_MODEL" ]; then
    echo -e "${GREEN}✅ OpenAI 模型: $OPENAI_API_MODEL${NC}"
else
    echo -e "${YELLOW}⚠️  OpenAI 模型: 使用默认值 (gpt-4)${NC}"
fi
echo

# 2. 检查 Python 环境
echo -e "${BLUE}2. Python 环境检查${NC}"
python_version=$(python --version 2>&1)
echo -e "${GREEN}✅ Python 版本: $python_version${NC}"

check_python_module "json" "json 模块"
check_python_module "pathlib" "pathlib 模块"
check_python_module "dataclasses" "dataclasses 模块"
echo

# 3. 检查项目结构
echo -e "${BLUE}3. 项目结构检查${NC}"
check_file "src/bookmark_ai_summary/keyword_analyzer.py" "关键词分析模块"
check_file "src/bookmark_ai_summary/run_keyword_analysis.py" "命令行入口"
check_file "requirements.lock" "依赖文件"
check_directory "data" "数据目录"
echo

# 4. 检查核心文件
echo -e "${BLUE}4. 核心文件检查${NC}"
check_file "data/keyword_index.json" "关键词索引文件"
check_directory "data/keyword_analysis" "分析报告目录"
check_file "keyword_analysis_summary.md" "分析索引文件"
echo

# 5. 检查索引文件完整性
echo -e "${BLUE}5. 索引文件完整性检查${NC}"
if [ -f "data/keyword_index.json" ]; then
    if python -c "import json; data=json.load(open('data/keyword_index.json')); print(f'关键词数量: {len(data)}'); print(f'文章总数: {sum(len(v) for v in data.values())}')" 2>/dev/null; then
        echo -e "${GREEN}✅ 索引文件格式正确${NC}"
    else
        echo -e "${RED}❌ 索引文件格式错误${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  索引文件不存在，请先运行分析${NC}"
fi
echo

# 6. 检查分析报告
echo -e "${BLUE}6. 分析报告检查${NC}"
if [ -d "data/keyword_analysis" ]; then
    report_count=$(find data/keyword_analysis -name "*.md" -type f 2>/dev/null | wc -l)
    if [ "$report_count" -gt 0 ]; then
        echo -e "${GREEN}✅ 分析报告数量: $report_count${NC}"

        # 显示最新的5个报告
        echo "最新报告:"
        find data/keyword_analysis -name "*.md" -type f -exec ls -lt {} + 2>/dev/null | head -6 | while read -r line; do
            if [[ "$line" != total* ]]; then
                echo "  $line"
            fi
        done
    else
        echo -e "${YELLOW}⚠️  未找到分析报告${NC}"
    fi
else
    echo -e "${RED}❌ 分析报告目录不存在${NC}"
fi
echo

# 7. 检查磁盘空间
echo -e "${BLUE}7. 磁盘空间检查${NC}"
if command -v df >/dev/null 2>&1; then
    data_size=$(du -sh data 2>/dev/null | cut -f1)
    echo -e "${GREEN}✅ 数据目录大小: $data_size${NC}"

    # 检查可用空间
    available_space=$(df . | tail -1 | awk '{print $4}')
    if [ "$available_space" -gt 1048576 ]; then  # 1GB
        echo -e "${GREEN}✅ 可用磁盘空间充足${NC}"
    else
        echo -e "${YELLOW}⚠️  可用磁盘空间不足 1GB${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  无法检查磁盘空间${NC}"
fi
echo

# 8. 检查网络连接
echo -e "${BLUE}8. 网络连接检查${NC}"
if command -v curl >/dev/null 2>&1; then
    if curl -s --max-time 5 https://api.openai.com/v1/models >/dev/null 2>&1; then
        echo -e "${GREEN}✅ OpenAI API 连接正常${NC}"
    else
        echo -e "${RED}❌ OpenAI API 连接失败${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  curl 不可用，无法检查网络连接${NC}"
fi
echo

# 9. 权限检查
echo -e "${BLUE}9. 权限检查${NC}"
if [ -w "data" ]; then
    echo -e "${GREEN}✅ 数据目录可写${NC}"
else
    echo -e "${RED}❌ 数据目录不可写${NC}"
fi

if [ -w "data/keyword_analysis" ] 2>/dev/null; then
    echo -e "${GREEN}✅ 分析报告目录可写${NC}"
else
    echo -e "${YELLOW}⚠️  分析报告目录不可写或不存存${NC}"
fi
echo

# 10. 性能建议
echo -e "${BLUE}10. 性能建议${NC}"

# 检查索引文件大小
if [ -f "data/keyword_index.json" ]; then
    index_size=$(stat -f%z "data/keyword_index.json" 2>/dev/null || stat -c%s "data/keyword_index.json" 2>/dev/null)
    if [ "$index_size" -gt 10485760 ]; then  # 10MB
        echo -e "${YELLOW}⚠️  索引文件较大 ($((index_size/1024/1024))MB)，建议定期清理${NC}"
    fi
fi

# 检查报告数量
if [ -d "data/keyword_analysis" ]; then
    report_count=$(find data/keyword_analysis -name "*.md" -type f 2>/dev/null | wc -l)
    if [ "$report_count" -gt 100 ]; then
        echo -e "${YELLOW}⚠️  分析报告数量较多 ($report_count 个)，建议考虑归档旧报告${NC}"
    fi
fi

echo -e "${GREEN}✅ 健康检查完成！${NC}"
echo

# 11. 快速修复建议
echo -e "${BLUE}11. 快速修复建议${NC}"

if [ ! -f "data/keyword_index.json" ]; then
    echo -e "${YELLOW}📝 索引文件不存在，运行以下命令创建：${NC}"
    echo "   python -m bookmark_ai_summary.run_keyword_analysis --force-rebuild"
    echo
fi

if [ ! -d "data/keyword_analysis" ] || [ -z "$(find data/keyword_analysis -name "*.md" 2>/dev/null)" ]; then
    echo -e "${YELLOW}📝 缺少分析报告，运行以下命令生成：${NC}"
    echo "   python -m bookmark_ai_summary.run_keyword_analysis"
    echo
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}📝 缺少 OpenAI API Key，设置环境变量：${NC}"
    echo "   export OPENAI_API_KEY=\"sk-your-api-key-here\""
    echo
fi

echo -e "${BLUE}=== 检查完成 ===${NC}"
echo "如需详细帮助，请查看: docs/keyword-analysis-quickstart.md"