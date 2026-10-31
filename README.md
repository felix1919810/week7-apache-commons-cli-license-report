# Apache Commons CLI 软件许可测试报告

《开源创新思维》第七周作业，题目日期：2026-10-29；实际测试日期：2026-10-31。

学号：f25015421；姓名：陈彦喆；班级：f250117。

## 提交文档

[下载 Word 测试报告](<f25015421-陈彦喆-Apache Commons CLI-软件许可测试报告.docx>)

报告沿用课程模板，含封面、正文、评价表共 5 页，已通过 Word 渲染逐页检查。报告涵盖项目介绍、工具安装、真实输出、结果分析、风险、测试策略及充分性判断。

## 实测结论

被测对象为 Apache Commons CLI 1.11.0 官方源码发行包，工具为 Apache Rat 0.18。

- 源码包 131 个文件，全部与 XML 资源清单对账一致，扫描前后源码 SHA-256 未变化。
- 120 个普通文件均匹配 Apache License 2.0，包含全部 87 个 Java 文件；Unapproved 为 0。
- 3 个通知类文件和 8 个二进制分类文件不等于完成了许可证匹配。人工检查确认 LICENSE.txt 和 NOTICE.txt 存在且内容与项目一致。
- 8 个二进制分类中有一个可读 shell 脚本 `src/site/resources/download_cli.cgi`，未见文件级许可头。仅更改副本后缀仍归为 BINARY，需进一步确认来源与适用授权。
- 独立对照：原始许可头通过（退出码 0），移除许可头失败（退出码 1），恢复后通过（退出码 0）。原始源码没有被修改。

结论限于源码许可头与声明文件检查，不涵盖完整传递依赖、二进制发行包、图片来源、商标使用或法律合规认定。测试由 AI 助手在本机实际执行并整理，保留原始证据供复核。

## 原始证据

- `evidence/rat-baseline.txt`：完整人类可读输出。
- `evidence/rat-baseline.xml`：完整机器可读输出。
- `evidence/runs.json`：基线命令、时间戳、退出码和耗时。
- `evidence/downloads.json`：下载来源、完整哈希和校验结果。
- `evidence/source-manifest.json`：131 个源码文件的 SHA-256。
- `evidence/verification.json`：路径覆盖核验和独立对照实验。
- `evidence/rat-*.xml` 及 `*.stdout.txt`、`*.stderr.txt`：各轮原始报告和日志。
- `SHA256SUMS.txt`：本次提交文档及配套文件的校验值（不含该清单自身）。

`cgi-text-review` 退出码 1 是由于没有普通文件和已识别许可类别，触发默认计数下限；它不是识别到未批准许可。SLF4J 日志提供器警告也不等于基线扫描失败。

## 复现

环境：Windows 64位、Python 3.10 或以上、可访问 Apache 归档及 Adoptium 下载服务的网络。脚本仅使用 Python 标准库；无需 Maven。首次准备会下载便携 Java、Rat 和固定版本源码并校验哈希。

为保留仓库中的首次实测证据，建议在单独目录运行：

```powershell
New-Item -ItemType Directory -Path replay
Copy-Item prepare_test.py,run_scan.py,verify_scan.py replay
python replay/prepare_test.py
python replay/run_scan.py
python replay/verify_scan.py
```

输出保存在 `replay/evidence`，对照副本保存在 `replay/controls`；脚本不执行被测项目代码、不修改其原始内容。Java 下载选择当时可用的 Temurin 17 JRE，实际版本、下载地址和哈希均记录；本报告使用 17.0.20.1+1。Rat 固定为 0.18，源码固定为 1.11.0。复现时间戳和耗时自然会变化。

## 来源

- [Apache Commons CLI](https://commons.apache.org/proper/commons-cli/)
- [Apache Rat 命令行说明](https://creadur.apache.org/rat/apache-rat/)
- [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- 固定源码和工具下载地址见 `evidence/downloads.json`。

仓库只提交作业报告、分析证据与复现脚本，不包含下载的 JRE、Rat 二进制包或被测项目源码；这些内容由复现脚本从官方来源取得。
