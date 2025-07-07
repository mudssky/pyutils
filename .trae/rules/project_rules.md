# Python通用工具库项目规则

## 项目概述

本项目是一个Python通用方法库(pyutils)，旨在提供常用的Python工具函数和实用程序。项目采用现代Python开发最佳实践，确保代码质量、性能和可维护性。

## 代码风格规范

### Python代码规范

- **严格遵循PEP 8**：使用4个空格缩进，行长度限制为88字符
- **类型注解**：所有公共函数和方法必须包含完整的类型注解，使用现代Python类型系统
- **文档字符串**：所有公共函数、类和模块必须有详细的Google风格docstring
- **命名规范**：
  - 函数和变量使用snake_case
  - 类名使用PascalCase
  - 常量使用UPPER_CASE
  - 私有成员以单下划线开头
  - 模块名使用小写字母和下划线

### 代码质量工具链

- **Ruff**：统一的代码格式化、静态检查和导入排序工具
- **MyPy**：严格的类型检查，启用strict模式
- **Bandit**：安全漏洞检测
- **Pre-commit**：Git提交前自动检查
- **测试覆盖率**：要求≥90%的代码覆盖率，使用pytest-cov生成报告

## 项目结构规范

### 目录组织

```
项目根目录/
├── src/pyutils/              # 主要源代码目录
│   ├── __init__.py          # 包初始化文件，定义公共API
│   ├── array.py             # 数组操作工具
│   ├── async_utils.py       # 异步工具函数
│   ├── bytes.py             # 字节操作工具
│   ├── cli.py               # 命令行接口工具
│   ├── collection.py        # 集合操作工具
│   ├── date.py              # 日期时间工具
│   ├── encoding.py          # 编码解码工具
│   ├── function.py          # 函数操作工具
│   ├── math.py              # 数学计算工具
│   ├── object.py            # 对象操作工具
│   ├── string.py            # 字符串操作工具
│   ├── type_utils.py        # 类型检查工具
│   └── url.py               # URL处理工具
├── tests/                   # 测试代码目录
│   ├── __init__.py          # 测试包初始化
│   ├── test_array.py        # 数组工具测试
│   ├── test_async_utils.py  # 异步工具测试
│   ├── test_bytes.py        # 字节工具测试
│   ├── test_collection.py   # 集合工具测试
│   ├── test_date.py         # 日期工具测试
│   ├── test_encoding.py     # 编码工具测试
│   ├── test_function.py     # 函数工具测试
│   ├── test_math.py         # 数学工具测试
│   ├── test_object.py       # 对象工具测试
│   ├── test_pyutils.py      # 主模块测试
│   ├── test_string.py       # 字符串工具测试
│   ├── test_type_utils.py   # 类型工具测试
│   └── test_url.py          # URL工具测试
├── docs/                    # 文档目录
│   ├── _static/             # 静态资源
│   ├── conf.py              # Sphinx配置
│   ├── index.rst            # 文档首页
│   ├── modules.rst          # 模块索引
│   ├── pyutils.rst          # API文档
│   ├── installation.rst     # 安装指南
│   ├── usage.rst            # 使用指南
│   ├── contributing.rst     # 贡献指南
│   ├── changelog.rst        # 变更日志
│   └── Makefile             # 文档构建脚本
├── .github/                 # GitHub配置目录
│   ├── workflows/           # GitHub Actions工作流
│   │   ├── ci.yml          # 持续集成
│   │   ├── dependency-update.yml # 依赖更新
│   │   ├── pre-release.yml  # 预发布
│   │   ├── release.yml      # 正式发布
│   │   └── version-bump.yml # 版本更新
│   ├── ISSUE_TEMPLATE.md    # Issue模板
│   └── *.md                 # 其他GitHub配置文档
├── .trae/                   # Trae IDE配置
│   └── rules/
│       └── project_rules.md # 项目规则文档
├── .promptx/                # PromptX AI助手配置
│   └── resource/
├── ai_docs/                 # AI生成的文档
├── examples/                # 示例代码
├── scripts/                 # 构建和部署脚本
├── 配置文件:
├── pyproject.toml           # 项目配置和依赖管理
├── uv.lock                  # 依赖锁定文件
├── ruff.toml                # Ruff代码检查配置
├── pytest.ini              # pytest测试配置
├── tox.ini                  # tox多环境测试配置
├── .travis.yml              # Travis CI配置（历史）
├── .pre-commit-config.yaml  # Pre-commit钩子配置
├── .editorconfig            # 编辑器配置
├── .gitignore               # Git忽略文件
├── .gitmessage              # Git提交消息模板
├── .releaserc.json          # 语义化发布配置
├── 构建和工具文件:
├── Makefile                 # 项目构建脚本
├── make.ps1                 # PowerShell构建脚本
├── build.ps1                # PowerShell构建脚本
├── publish.ps1              # PowerShell发布脚本
├── package.json             # Node.js依赖（用于语义化发布）
├── requirements_dev.txt     # 开发依赖（历史文件）
├── 文档文件:
├── README.md                # 项目说明（Markdown）
├── README.rst               # 项目说明（reStructuredText）
├── AUTHORS.rst              # 作者信息
├── CONTRIBUTING.rst         # 贡献指南
├── CODE_OF_CONDUCT.rst      # 行为准则
├── HISTORY.rst              # 历史记录
├── LICENSE                  # 许可证
├── MANIFEST.in              # 打包清单
└── PROJECT_SUMMARY.md       # 项目总结
```

### 文件组织原则

#### 源代码组织
- **主要源代码**：所有源代码放在`src/pyutils/`目录下
- **模块化设计**：每个功能领域独立成模块（如array.py、string.py等）
- **公共API**：通过`__init__.py`暴露公共接口，遵循最小暴露原则
- **命名规范**：模块名使用小写字母和下划线，清晰表达功能

#### 测试代码组织
- **测试目录**：所有测试文件放在`tests/`目录下
- **测试命名**：测试文件以`test_`前缀命名，与对应模块保持一致
- **测试覆盖**：每个源代码模块都应有对应的测试文件
- **测试结构**：测试文件内部按功能分组，使用清晰的测试类和方法名

#### 文档组织
- **API文档**：使用Sphinx自动生成，配置在`docs/conf.py`
- **用户文档**：包含安装、使用、贡献等指南
- **变更记录**：维护详细的changelog.rst
- **示例代码**：在`examples/`目录提供实用示例

#### 配置文件管理
- **项目配置**：`pyproject.toml`作为主要配置文件
- **工具配置**：各工具独立配置文件（ruff.toml、pytest.ini等）
- **环境配置**：使用`.env.template`提供环境变量模板
- **编辑器配置**：`.editorconfig`确保代码风格一致性

#### 构建和部署
- **构建脚本**：提供跨平台构建脚本（Makefile、PowerShell脚本）
- **CI/CD配置**：GitHub Actions工作流在`.github/workflows/`
- **发布配置**：语义化发布配置`.releaserc.json`
- **依赖锁定**：`uv.lock`确保环境一致性

## 开发流程规范

### 依赖管理

- **包管理器**：使用`uv`作为现代Python包管理器，提供快速依赖解析和安装
- **配置文件**：使用`pyproject.toml`管理项目配置和依赖
- **核心依赖**：`typer`（CLI工具）
- **开发依赖组**：通过`[dependency-groups]`管理开发工具链
  - 测试工具：`pytest`, `pytest-cov`, `pytest-xdist`, `pytest-benchmark`, `hypothesis`
  - 代码质量：`ruff`, `mypy`, `bandit`, `pre-commit`
  - 文档工具：`sphinx`, `sphinx-rtd-theme`
  - 发布工具：`twine`, `build`

### 测试要求

- **测试框架**：使用pytest，支持并行测试(pytest-xdist)
- **测试类型**：
  - 单元测试：核心功能测试
  - 属性测试：使用hypothesis进行基于属性的测试
  - 性能测试：使用pytest-benchmark进行基准测试
  - 异步测试：使用pytest-asyncio支持异步代码测试
- **测试覆盖率**：核心功能必须≥90%覆盖率，生成HTML和XML报告
- **测试命名**：测试函数以`test_`开头，清晰描述测试场景
- **测试独立性**：每个测试用例必须独立运行，支持并行执行
- **边界测试**：必须测试边界条件、异常情况和错误处理

### 版本兼容性

- **Python版本**：支持Python 3.10+（与pyproject.toml一致）
- **多版本测试**：CI中测试Python 3.9-3.14版本
- **向后兼容**：新功能不能破坏现有API
- **弃用策略**：废弃功能需要提前一个版本警告，使用`warnings`模块

## 文档规范

### 文档要求

- 使用**Sphinx**生成文档
- **README.rst**：项目介绍、安装和基本使用
- **API文档**：所有公共接口必须有详细文档
- **使用示例**：提供清晰的代码示例

### 文档格式

- 使用reStructuredText格式
- 代码示例必须可执行
- 包含安装、使用、贡献指南

## 发布和部署

### 版本管理

- 遵循**语义化版本**规范(SemVer)
- 版本号格式：MAJOR.MINOR.PATCH
- 在`__init__.py`和`pyproject.toml`中保持版本一致

### CI/CD流程

- **平台**：使用GitHub Actions，支持多操作系统(Ubuntu/Windows/macOS)
- **触发条件**：
  - 推送到main分支
  - Pull Request到main分支
  - 手动触发(workflow_dispatch)
  - 发布时自动触发
- **智能检测**：使用path filters检测变更，只在相关文件变更时运行
- **并行执行**：
  - 测试作业：多Python版本(3.9-3.14)和多操作系统并行
  - 代码质量检查：独立并行执行
- **缓存优化**：使用uv缓存加速依赖安装
- **报告生成**：
  - 测试结果和覆盖率报告
  - 安全扫描报告
  - 上传到Codecov进行覆盖率跟踪

## 贡献规范

### 代码提交

- **提交信息**：使用清晰的提交信息，遵循约定式提交
- **分支策略**：功能开发使用feature分支
- **代码审查**：所有代码变更必须经过审查

### 新功能开发

- 新需求开发在dev分支（从main拉取），或者从main拉取feature分支开发
- 先编写测试用例（TDD）
- 确保所有测试通过
- 更新相关文档
- 添加使用示例

## 性能和安全

### 性能要求

- 优先使用Python内置函数和标准库
- 避免不必要的依赖
- 考虑内存使用效率
- 提供性能基准测试

### 安全考虑

- 输入验证和边界检查
- 避免使用不安全的函数
- 定期更新依赖版本
- 不在代码中硬编码敏感信息

## 工具配置

### 编辑器配置

- 遵循`.editorconfig`设置
- 使用UTF-8编码
- Unix风格换行符(LF)
- 文件末尾插入换行符

### 开发环境设置

- **包管理器**：使用`uv`进行依赖管理和虚拟环境管理
- **环境初始化**：
  ```bash
  # 安装uv（如果未安装）
  curl -LsSf https://astral.sh/uv/install.sh | sh
  
  # 同步开发环境
  uv sync --dev
  ```
- **常用开发命令**：
  ```bash
  # 运行测试
  uv run pytest
  
  # 运行测试并生成覆盖率报告
  uv run pytest --cov=src/pyutils --cov-report=html
  
  # 代码格式化
  uv run ruff format .
  
  # 代码检查
  uv run ruff check .
  
  # 类型检查
  uv run mypy src/
  
  # 安全检查
  uv run bandit -r src/
  
  # 性能基准测试
  uv run pytest --benchmark-only
  
  # 安装pre-commit钩子
  uv run pre-commit install
  ```
- **IDE配置**：推荐配置编辑器支持ruff和mypy集成

## 代码审查和质量保证

### 代码审查标准

- **功能性审查**：
  - 代码逻辑正确性
  - 边界条件处理
  - 错误处理机制
  - 性能影响评估
- **代码质量审查**：
  - 遵循项目编码规范
  - 类型注解完整性
  - 文档字符串质量
  - 测试覆盖率
- **安全性审查**：
  - 输入验证
  - 潜在安全漏洞
  - 依赖安全性
- **可维护性审查**：
  - 代码可读性
  - 模块化设计
  - 重复代码检查

### 质量门禁

- **自动化检查**：
  - 所有测试必须通过
  - 代码覆盖率≥90%
  - 静态分析无严重问题
  - 安全扫描通过
- **手动审查**：
  - 至少一人代码审查
  - 架构设计审查（重大变更）
  - 文档更新确认

## 性能优化指南

### 性能基准

- **基准测试**：使用pytest-benchmark进行性能测试
- **性能回归**：CI中监控性能变化
- **内存使用**：监控内存占用和泄漏
- **并发性能**：测试多线程/异步场景

### 优化策略

- **算法优化**：选择合适的数据结构和算法
- **缓存策略**：合理使用缓存减少重复计算
- **懒加载**：延迟初始化和计算
- **批处理**：批量处理减少开销

## AI助手行为规范

### 代码生成要求

- 生成的代码必须符合项目的所有规范
- 包含完整的类型注解和Google风格文档字符串
- 提供对应的测试用例，包括边界测试
- 考虑错误处理和异常情况
- 遵循性能最佳实践

### 建议和优化

- 优先推荐Python标准库解决方案
- 关注代码的可读性、可维护性和性能
- 提供具体的性能优化建议
- 确保向后兼容性和API稳定性
- 考虑安全性和最佳实践

### 问题解决

- 提供具体可执行的解决方案
- 解释技术选择的原因和权衡
- 考虑多种实现方案的优缺点
- 关注长期维护性和扩展性
- 提供性能和安全性分析

## 项目维护和最佳实践

### 依赖管理最佳实践

- **版本锁定**：使用`uv.lock`锁定依赖版本，确保环境一致性
- **安全更新**：定期更新依赖，使用GitHub Dependabot自动检测安全漏洞
- **最小依赖**：避免不必要的依赖，优先使用标准库
- **兼容性测试**：在CI中测试依赖更新的兼容性

### 文档维护

- **API文档**：使用Sphinx自动生成，保持与代码同步
- **变更日志**：遵循Keep a Changelog格式，记录所有重要变更
- **示例代码**：提供可执行的示例，定期验证有效性
- **贡献指南**：明确的贡献流程和代码规范

### 发布流程

- **语义化版本**：严格遵循SemVer规范
- **自动化发布**：使用GitHub Actions自动化发布流程
- **发布检查**：发布前进行完整的测试和质量检查
- **回滚策略**：准备快速回滚机制应对问题

### 监控和维护

- **性能监控**：跟踪关键性能指标
- **错误追踪**：监控生产环境中的错误和异常
- **使用统计**：了解API使用情况，指导优化方向
- **社区反馈**：积极响应issue和PR，维护社区关系

### 技术债务管理

- **定期重构**：识别和重构技术债务
- **代码审计**：定期进行代码质量审计
- **性能优化**：基于基准测试进行性能优化
- **架构演进**：根据需求变化适时调整架构设计
