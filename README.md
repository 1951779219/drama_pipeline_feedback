# 短剧制作流水线 · 问题反馈

用于收集短剧制作流水线的 BUG、功能建议和使用问题，方便按模块跟进处理。

- [软件源码与使用说明](https://github.com/1951779219/drama_pipeline_app)
- [版本下载与更新记录](https://github.com/1951779219/drama_pipeline_release/releases)
- [提交反馈](https://github.com/1951779219/drama_pipeline_feedback/issues/new/choose)

## 如何使用

1. 先搜索 [已有 Issues](https://github.com/1951779219/drama_pipeline_feedback/issues)，查看是否已有同类问题。
2. 点击“New issue”，选择错误报告或功能建议模板。
3. 错误报告填写软件版本、出问题的模块、复现步骤、期望结果和实际结果，并附上相关错误日志或截图。
4. 提交后，在该 Issue 中补充信息、查看回复和处理进展。

可反馈的模块包括启动与授权、下载、合成、人声分离、混音导出、上传、联机模式、自动监测和软件更新。Issue 创建后，GitHub Actions 会自动分类并标记优先级。

## 提交前处理日志

请隐藏 API Key、访问令牌、账号密码、Cookie 和私人路径，只提供复现问题所需的日志片段。这里是公开反馈区，提交的内容所有人都能看到。

## 仓库内容

- `.github/ISSUE_TEMPLATE/`：反馈表单。
- `.github/workflows/issue_triage.yml`：自动分类工作流。
- `tools/github_issue_triage.py`：分类脚本。

本仓库用于反馈和分类；运行软件请查看上面的源码仓库或版本下载入口。


## 许可

本仓库的自有代码和文档按 [MIT License](LICENSE) 提供。应用发行包中的第三方组件、工具和模型仍遵循各自许可。
