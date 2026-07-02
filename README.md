# Skill Poster Workflow

输入主题词和结构化文案，自动生成统一风格的知识卡片海报 PNG。

适合：小红书、公众号配图、朋友圈、知识 IP 内容批量生产。

## 文件说明

- `poster_generator.py`：海报生成主程序
- `content_template.json`：单张海报示例文案
- `topics.csv`：批量生成模板
- `prompt_template.md`：让 AI 生成结构化文案的提示词
- `requirements.txt`：Python 依赖

## 快速开始

```bash
pip install -r requirements.txt
python poster_generator.py --json content_template.json
```

批量生成：

```bash
python poster_generator.py --csv topics.csv
```

生成图片会保存到：

```bash
output/
```

## 推荐工作流

主题词 → AI 生成 JSON 文案 → 程序自动排版 → 导出 1080×1440 PNG
