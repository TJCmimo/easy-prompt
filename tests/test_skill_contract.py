from pathlib import Path
from typing import Optional
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def markdown_section(content: str, heading: str, next_heading: Optional[str]) -> str:
    start = content.index(heading)
    end = content.index(next_heading, start) if next_heading else len(content)
    return content[start:end]


class BackgroundContractTests(unittest.TestCase):
    def test_background_is_diagnosed_but_conditionally_output(self) -> None:
        skill = read("SKILL.md")

        self.assertIn("`背景` 是条件字段", skill)
        self.assertIn("删除测试", skill)
        self.assertIn("逐项检查不等于逐项输出", skill)
        self.assertIn("不得复述已在 `目标` 或 `输入` 中表达的信息", skill)
        self.assertIn("预算、人手、时间等资源上限属于 `限制`", skill)
        self.assertNotIn("背景、限制或验收缺失", skill)
        self.assertNotIn("按以下固定字段组织", skill)

        portable = read("portable/easy-prompt-portable.md")
        self.assertIn("不得复述已在 `目标` 或 `输入` 中表达的信息", portable)

    def test_runtime_rules_do_not_default_to_rm_newcomer(self) -> None:
        runtime_files = (
            "SKILL.md",
            "references/five-elements.md",
            "references/recipes.md",
            "portable/easy-prompt-portable.md",
        )

        for relative_path in runtime_files:
            with self.subTest(path=relative_path):
                content = read(relative_path)
                self.assertNotIn('默认"RM 新生、相应方向基础一般"', content)
                self.assertNotIn("背景：【推断】RM", content)

    def test_examples_cover_omitted_and_retained_background(self) -> None:
        examples = read("references/examples.md")

        self.assertIn("背景判定：省略", examples)
        self.assertIn("背景判定：保留", examples)

        example_1 = markdown_section(examples, "## 例 1", "## 例 2")
        example_2 = markdown_section(examples, "## 例 2", "## 例 3")
        example_3 = markdown_section(examples, "## 例 3", "## 例 4")
        example_4 = markdown_section(examples, "## 例 4", "## 例 5")
        example_5 = markdown_section(examples, "## 例 5", None)

        self.assertNotIn("\n背景：", example_1)
        self.assertIn("\n背景：", example_2)
        self.assertNotIn("目标：用适合初学者", example_2)
        self.assertNotIn("背景：RM 自瞄项目", example_3)
        self.assertNotIn("背景：RM 哨兵导航项目", example_4)
        self.assertNotIn("\n背景：", example_4)
        self.assertIn("限制：项目人手和经费有限", example_4)
        self.assertNotIn("目标：为 RM 视觉组", example_5)


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


if __name__ == "__main__":
    unittest.main()
