<!-- ppt-master-schema: spec-lock/v1 -->
# Execution Lock

## canvas
- viewBox: 0 0 1280 720
- format: PPT 16:9

## communication
- primary_language: zh-CN
- audience: 大赛评审（现场答辩）
- objective: 3 分钟内让评审认可作品的 8 项数字全部实测可溯、链路可一键复验
- core_message: 最小数据叙事闭环——零依赖 CLI 产出 8 项实测指标，报告与 PPT 数字全部一键可溯
- consumption_mode: presentation

## mode
- mode: pyramid

## visual_style
- visual_style: dark-tech

## colors
- background: #0B1220
- secondary_bg: #111A2E
- primary: #38BDF8
- accent: #22D3EE
- secondary_accent: #F59E0B
- body_text: #E2E8F0
- secondary_text: #94A3B8
- divider: #1E293B

## typography
- font_family: 'Microsoft YaHei', 'Noto Sans SC', 'PingFang SC', Arial, sans-serif
- title_family: 'Microsoft YaHei', 'Noto Sans SC', 'PingFang SC', Arial, sans-serif
- body_family: 'Microsoft YaHei', 'Noto Sans SC', 'PingFang SC', Arial, sans-serif
- data_family: Consolas, 'JetBrains Mono', 'Courier New', monospace
- body: 30
- title: 54
- subtitle: 36
- annotation: 20

## icons
- library: tabler-outline
- stroke_width: 2
- inventory: tabler-outline/terminal-2, tabler-outline/table, tabler-outline/chart-bar, tabler-outline/circle-check, tabler-outline/refresh, tabler-outline/target-arrow

## page_rhythm
- P01: anchor
- P02: breathing
- P03: dense
- P04: breathing
- P05: anchor

## pptx_structure
- mode: flat

## forbidden
- `mask`, `<style>`, `class`, external CSS, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<set>`, `<script>` / event attributes, `<iframe>`
- HTML named entities in text; write typography as raw Unicode and escape XML reserved characters
