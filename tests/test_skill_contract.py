from pathlib import Path
import re
from typing import Optional
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def markdown_section(content: str, heading: str, next_heading: Optional[str]) -> str:
    heading_pattern = re.compile(
        rf"^{re.escape(heading)}(?=[（\n])",
        re.MULTILINE,
    )
    start_match = heading_pattern.search(content)
    if start_match is None:
        raise ValueError(f"heading not found: {heading}")
    start = start_match.start()

    if next_heading:
        next_pattern = re.compile(
            rf"^{re.escape(next_heading)}(?=[（\n])",
            re.MULTILINE,
        )
        next_match = next_pattern.search(content, start_match.end())
        if next_match is None:
            raise ValueError(f"heading not found: {next_heading}")
        end = next_match.start()
    else:
        end = len(content)
    return content[start:end]


class GenericReleaseContractTests(unittest.TestCase):
    def test_public_runtime_documents_have_no_legacy_single_domain_language(
        self,
    ) -> None:
        public_runtime_documents = (
            "README.md",
            "SKILL.md",
            "portable/easy-prompt-portable.md",
            "references/anti-patterns.md",
            "references/catalysts.md",
            "references/domain-structures.md",
            "references/examples.md",
            "references/five-elements.md",
            "references/recipes.md",
        )
        legacy_single_domain_language = re.compile(
            r"Robo"
            r"Master|(?<![A-Za-z0-9_])R"
            r"M(?![A-Za-z0-9_])|装"
            r"甲板|自"
            r"瞄|哨"
            r"兵|视觉"
            r"组",
            re.IGNORECASE,
        )

        for relative_path in public_runtime_documents:
            with self.subTest(path=relative_path):
                self.assertNotRegex(
                    read(relative_path),
                    legacy_single_domain_language,
                )

    def test_gold_examples_cover_distinct_domains(self) -> None:
        examples = read("references/examples.md")
        domains = {
            "## 例 1": ("工程执行类", "订单查询接口", "调用链"),
            "## 例 2": ("学习理解类", "A/B 测试报告", "统计基础"),
            "## 例 3": ("决策比较类", "远程公益团队", "知识库"),
            "## 例 4": ("猜想探索类", "社区读书会", "每月预算"),
            "## 例 5": ("内容生成类", "线上工作坊", "主持人操作手册"),
            "## 例 6": ("会话收割·面向 coding agent", "TSAN"),
            "## 例 7": ("弹性格式最小示例", "机会成本", "周末时间"),
            "## 例 8": ("引导采样 → 上下文回滚", "旧版页面", "起名字"),
        }
        headings = tuple(domains)

        for index, (heading, required_phrases) in enumerate(domains.items()):
            next_heading = headings[index + 1] if index + 1 < len(headings) else None
            section = markdown_section(examples, heading, next_heading)
            for expected in required_phrases:
                with self.subTest(example=heading, expected=expected):
                    self.assertIn(expected, section)


class BackgroundContractTests(unittest.TestCase):
    def test_background_is_diagnosed_but_conditionally_output(self) -> None:
        skill = read("SKILL.md")

        self.assertIn("`背景` 是条件字段", skill)
        self.assertIn("删除测试", skill)
        self.assertIn("逐项检查不等于逐项输出", skill)
        self.assertIn("不得复述已在 `目标` 或 `材料` 中表达的信息", skill)
        self.assertIn("预算、人手、时间等资源上限属于 `限制`", skill)
        self.assertNotIn("背景、限制或验收缺失", skill)
        self.assertNotIn("按以下固定字段组织", skill)

        portable = read("portable/easy-prompt-portable.md")
        self.assertIn("不得复述已在 `目标` 或 `材料` 中表达的信息", portable)

    def test_runtime_rules_do_not_infer_identity_from_domain(self) -> None:
        runtime_copies = (
            "SKILL.md",
            "portable/easy-prompt-portable.md",
        )

        for relative_path in runtime_copies:
            with self.subTest(path=relative_path):
                content = read(relative_path)
                self.assertIn(
                    "默认推断用户是新手、专家或具备特定身份和能力",
                    content,
                )

    def test_examples_cover_omitted_and_retained_background(self) -> None:
        examples = read("references/examples.md")

        self.assertIn("背景判定：省略", examples)
        self.assertIn("背景判定：保留", examples)

        example_1 = markdown_section(examples, "## 例 1", "## 例 2")
        example_2 = markdown_section(examples, "## 例 2", "## 例 3")
        example_3 = markdown_section(examples, "## 例 3", "## 例 4")
        example_4 = markdown_section(examples, "## 例 4", "## 例 5")
        example_5 = markdown_section(examples, "## 例 5", "## 例 6")

        self.assertNotIn("\n背景：", example_1)
        self.assertIn(
            "背景：读者负责活动运营，刚接触数据分析，统计基础一般",
            example_2,
        )
        self.assertIn(
            "背景：团队共 6 人、采用远程协作、成员每半年轮换，"
            "维护工作由志愿者承担",
            example_3,
        )
        self.assertNotIn("\n背景：", example_4)
        self.assertIn(
            "限制：可投入 3 名志愿者，每月预算不超过 500 元",
            example_4,
        )
        self.assertIn(
            "背景：读者是第一次主持线上工作坊的志愿者",
            example_5,
        )
        self.assertIn(
            "限制：【推断】格式仿照下面的目标风格样例",
            example_5,
        )


class IndependentCriticContractTests(unittest.TestCase):
    def test_skill_requires_capability_gated_independent_review(self) -> None:
        skill = read("SKILL.md")

        for expected in (
            "独立反方审查",
            "未参与初步分析的子 agent",
            "不支持子 agent",
            "最终推荐是否改变",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, skill)

    def test_review_modes_and_comparison_only_bypass_are_explicit(self) -> None:
        skill = read("SKILL.md")
        recipes = read("references/recipes.md")
        portable = read("portable/easy-prompt-portable.md")

        for expected in ("推荐审查", "筛选审查", "指定方案反驳"):
            with self.subTest(expected=expected):
                self.assertIn(expected, skill)

        for content in (recipes, portable):
            with self.subTest(document="comparison-only branch"):
                self.assertIn("只比较时不触发", content)
                self.assertIn("不加入独立反方审查", content)

        self.assertIn("不要凭空增加推荐", skill)
        self.assertIn("用户要求推荐时，先比较再推荐；只比较时停在比较结果", skill)

    def test_symmetric_counterarguments_do_not_become_named_plan_rebuttal(self) -> None:
        for relative_path in (
            "SKILL.md",
            "references/catalysts.md",
            "references/recipes.md",
            "portable/easy-prompt-portable.md",
        ):
            content = read(relative_path)
            with self.subTest(path=relative_path):
                self.assertIn("对全部候选项逐项、对称地列出反方观点", content)
                self.assertIn("仍属于只比较", content)

    def test_named_plan_rebuttal_does_not_expand_into_alternative_comparison(self) -> None:
        skill = read("SKILL.md")
        recipes = read("references/recipes.md")

        self.assertIn("不得比较或展开替代方案", skill)
        self.assertIn("指定方案反驳不要求统一比较维度", recipes)
        self.assertNotIn("要求推荐、筛选或反驳：统一比较维度", recipes)

    def test_named_plan_rebuttal_triggers_without_a_verdict_request(self) -> None:
        for relative_path in (
            "SKILL.md",
            "references/catalysts.md",
            "references/recipes.md",
            "portable/easy-prompt-portable.md",
        ):
            content = read(relative_path)
            with self.subTest(path=relative_path):
                self.assertIn("作为非对称攻击对象", content)
                self.assertIn("即使用户不要求判断原结论是否改变", content)

        skill = read("SKILL.md")
        self.assertIn("若用户明确禁止改判结论，只报告反驳成立范围", skill)

    def test_review_mode_contract_is_consistent_across_runtime_copies(self) -> None:
        runtime_contracts = {
            "SKILL.md": (
                "推荐审查",
                "筛选审查",
                "指定方案反驳",
                "最终推荐是否改变",
                "候选集是否改变",
                "原判断是否改变",
                "只比较时不触发",
                "不支持子 agent",
            ),
            "references/catalysts.md": (
                "推荐审查",
                "筛选审查",
                "指定方案反驳",
                "最终推荐是否改变",
                "候选集是否改变",
                "原判断是否改变",
                "只比较时不触发",
                "不支持子 agent",
            ),
            "references/recipes.md": (
                "推荐审查",
                "筛选审查",
                "指定方案反驳",
                "最终推荐是否改变",
                "候选集是否改变",
                "原判断是否改变",
                "只比较时不触发",
                "不加入独立反方审查",
                "不支持子 agent",
            ),
            "portable/easy-prompt-portable.md": (
                "推荐审查",
                "筛选审查",
                "指定方案反驳",
                "最终推荐是否改变",
                "候选集是否改变",
                "原判断是否改变",
                "只比较时不触发",
                "不支持子 agent",
            ),
            "README.md": (
                "推荐审查",
                "筛选审查",
                "指定方案反驳",
                "最终推荐是否改变",
                "候选集是否改变",
                "原判断是否改变",
                "只比较时不触发",
            ),
        }

        for relative_path, required_phrases in runtime_contracts.items():
            content = read(relative_path)
            for expected in required_phrases:
                with self.subTest(path=relative_path, expected=expected):
                    self.assertIn(expected, content)

    def test_python_cache_files_are_ignored(self) -> None:
        gitignore = read(".gitignore")

        self.assertIn("__pycache__/", gitignore)
        self.assertIn("*.py[cod]", gitignore)

    def test_recipe_catalyst_and_portable_copy_share_review_contract(self) -> None:
        runtime_files = (
            "references/catalysts.md",
            "references/recipes.md",
            "portable/easy-prompt-portable.md",
        )

        for relative_path in runtime_files:
            content = read(relative_path)
            with self.subTest(path=relative_path):
                self.assertIn("独立反方审查", content)
                self.assertIn("子 agent", content)
                self.assertIn("不支持子 agent", content)
                self.assertIn("最终推荐是否改变", content)


class TopFiveGapContractTests(unittest.TestCase):
    runtime_copies = (
        "SKILL.md",
        "portable/easy-prompt-portable.md",
    )

    def test_material_replaces_input_as_the_prompt_field_label(self) -> None:
        field_documents = (
            "SKILL.md",
            "portable/easy-prompt-portable.md",
            "references/five-elements.md",
            "references/recipes.md",
            "references/examples.md",
        )

        for relative_path in field_documents:
            content = read(relative_path)
            with self.subTest(path=relative_path):
                self.assertIn("材料", content)
                self.assertNotIn("\n输入：", content)

        for relative_path in self.runtime_copies:
            with self.subTest(path=relative_path, expected="五要素字段名"):
                self.assertIn(
                    "目标、背景、材料、限制、验收",
                    read(relative_path),
                )

        self.assertIn(
            "目标、背景、材料、限制、验收",
            read("README.md"),
        )
        self.assertIn("输入事件", read("references/domain-structures.md"))

    def test_harvest_evidence_volume_and_deletion_contract_is_in_both_copies(
        self,
    ) -> None:
        required_phrases = (
            "用户亲述的需求、操作或观察结果",
            "代码、配置、日志或命令输出",
            "不得自动升级为已验证根因",
            "AI 自身未经验证的断言",
            "候选方向",
            "只摘录能支持当前任务的关键片段",
            "注明来源位置",
            "对每项候选收割内容执行“删除测试”",
            "适用于全部收割内容",
        )

        for relative_path in self.runtime_copies:
            content = read(relative_path)
            for expected in required_phrases:
                with self.subTest(path=relative_path, expected=expected):
                    self.assertIn(expected, content)

    def test_review_diff_and_zero_class_exit_are_in_both_copies(self) -> None:
        runtime_phrases = (
            "代码评审",
            "review diff",
            "目标清楚但五类均不匹配",
            "未套用五类配方",
            "不加入改码或回滚要求",
        )

        for relative_path in self.runtime_copies:
            content = read(relative_path)
            for expected in runtime_phrases:
                with self.subTest(path=relative_path, expected=expected):
                    self.assertIn(expected, content)

        recipes = read("references/recipes.md")
        portable = read("portable/easy-prompt-portable.md")
        for content_name, content in (
            ("references/recipes.md", recipes),
            ("portable/easy-prompt-portable.md", portable),
        ):
            for expected in (
                "严重性评级保守",
                "只报告能从代码确认的问题",
                "`文件:行`",
            ):
                with self.subTest(path=content_name, expected=expected):
                    self.assertIn(expected, content)

        for expected in (
            "代码评审默认限制",
            "代码评审默认验收",
            "代码评审转写模板",
        ):
            with self.subTest(path="references/recipes.md", expected=expected):
                self.assertIn(expected, recipes)

    def test_flexible_format_and_scenario_examples_are_locked(self) -> None:
        required_phrases = (
            "弹性格式",
            "单一明确目标、无需收割或粘贴任何材料、无特殊限制",
            "2–3 行自然语句",
            "会话收割且面向 coding agent",
            "对照例 6",
            "弹性格式对照例 7",
            "只对照例 1 的完整字段结构和口吻",
            "不照搬其中的软件服务对象、材料或排查维度",
        )

        for relative_path in self.runtime_copies:
            content = read(relative_path)
            for expected in required_phrases:
                with self.subTest(path=relative_path, expected=expected):
                    self.assertIn(expected, content)

        for relative_path in (
            "references/examples.md",
            "portable/easy-prompt-portable.md",
        ):
            content = read(relative_path)
            example_6 = markdown_section(content, "## 例 6", "## 例 7")
            example_7 = markdown_section(content, "## 例 7", None)
            with self.subTest(path=relative_path, example=6):
                self.assertIn("会话收割·面向 coding agent", example_6)
                self.assertIn("`src/cache.cpp`", example_6)
                self.assertIn(
                    "ctest --test-dir build -R cache --output-on-failure",
                    example_6,
                )
                self.assertIn("`/tmp/cache-tsan.log`", example_6)
                self.assertNotRegex(example_6, r"<[^>]+>")
            with self.subTest(path=relative_path, example=7):
                self.assertIn("弹性格式最小示例", example_7)
                self.assertIn("用大白话解释“机会成本”", example_7)
                self.assertIn("不套五要素标签", example_7)

    def test_reset_mainline_and_merged_final_line_are_in_both_copies(
        self,
    ) -> None:
        required_phrases = (
            "现在切换任务，忽略前文风格，以下只以本条为准",
            "用户描述、或会话内可直接观察到",
            "当前唯一目标：<X>",
            "候选问题列表",
            "多条末行提醒同时触发时",
            "必须合并为同一句且只占",
            "不再同时要求回溯发送",
        )

        for relative_path in self.runtime_copies:
            content = read(relative_path)
            for expected in required_phrases:
                with self.subTest(path=relative_path, expected=expected):
                    self.assertIn(expected, content)

    def test_two_stage_waiting_sentences_are_in_both_copies(self) -> None:
        required_phrases = (
            "等 AI 展开完再发第二条",
            "拿候选术语对照代码",
            "新开一个干净会话再发第二条",
        )

        for relative_path in self.runtime_copies:
            content = read(relative_path)
            for expected in required_phrases:
                with self.subTest(path=relative_path, expected=expected):
                    self.assertIn(expected, content)

    def test_guided_sampling_example_is_locked(self) -> None:
        for relative_path in (
            "references/examples.md",
            "portable/easy-prompt-portable.md",
        ):
            example_8 = markdown_section(read(relative_path), "## 例 8", None)
            for expected in (
                "引导采样 → 上下文回滚·两段式",
                "先不要给修复方案",
                "5–8 个可能相关的技术概念",
                "拿候选术语对照代码、配置和日志核实后，新开一个干净会话再发第二条。",
                "候选方向不是已确认结论",
            ):
                with self.subTest(path=relative_path, expected=expected):
                    self.assertIn(expected, example_8)

        for relative_path in self.runtime_copies:
            with self.subTest(path=relative_path, expected="两段式对照例 8"):
                self.assertIn("两段式对照例 8", read(relative_path))

    def test_copied_examples_are_identical_in_reference_and_portable_copy(
        self,
    ) -> None:
        reference_example_1 = markdown_section(
            read("references/examples.md"),
            "## 例 1",
            "## 例 2",
        )
        portable_example_1 = markdown_section(
            read("portable/easy-prompt-portable.md"),
            "## 例 1",
            "## 例 6",
        )
        examples = markdown_section(read("references/examples.md"), "## 例 6", None)
        portable = markdown_section(
            read("portable/easy-prompt-portable.md"),
            "## 例 6",
            None,
        )

        self.assertEqual(reference_example_1, portable_example_1)
        self.assertEqual(examples, portable)


    def test_rewind_asymmetry_and_field_assignment_are_in_both_copies(
        self,
    ) -> None:
        required_phrases = (
            "回溯只回退对话、不回退文件",
            "无来由的 diff 当异常追查",
            "材料、bug 现象与失败观察入 `材料`",
        )

        for relative_path in self.runtime_copies:
            content = read(relative_path)
            for expected in required_phrases:
                with self.subTest(path=relative_path, expected=expected):
                    self.assertIn(expected, content)

        skill = read("SKILL.md")
        with self.subTest(path="SKILL.md", expected="关键背景已改为关键信息"):
            self.assertNotIn("关键背景", skill)
            self.assertIn("等关键信息要内联写全", skill)


if __name__ == "__main__":
    unittest.main()
