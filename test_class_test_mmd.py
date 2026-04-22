"""
Tests for class_test.mmd — a Mermaid classDiagram file.

Validates diagram syntax, class definitions, inheritance relationships,
member declarations, and visibility modifiers.
"""

import os
import re
import pytest

MMD_PATH = os.path.join(os.path.dirname(__file__), "class_test.mmd")


@pytest.fixture(scope="module")
def diagram_content():
    with open(MMD_PATH, "r") as f:
        return f.read()


@pytest.fixture(scope="module")
def diagram_lines(diagram_content):
    return [line.rstrip() for line in diagram_content.splitlines()]


# ---------------------------------------------------------------------------
# File-level structure
# ---------------------------------------------------------------------------


class TestFileLevelStructure:
    def test_file_exists(self):
        assert os.path.isfile(MMD_PATH), "class_test.mmd must exist"

    def test_file_is_not_empty(self, diagram_content):
        assert diagram_content.strip(), "class_test.mmd must not be empty"

    def test_starts_with_classDiagram(self, diagram_lines):
        assert diagram_lines[0].strip() == "classDiagram", (
            "First non-empty line must be 'classDiagram'"
        )

    def test_line_count(self, diagram_lines):
        # The diagram has exactly 16 lines (no trailing newline in source)
        assert len(diagram_lines) == 16, (
            f"Expected 16 lines, got {len(diagram_lines)}"
        )


# ---------------------------------------------------------------------------
# Inheritance relationships
# ---------------------------------------------------------------------------


class TestInheritanceRelationships:
    def test_duck_inherits_from_animal(self, diagram_content):
        assert "Animal <|-- Duck" in diagram_content, (
            "Duck must inherit from Animal via 'Animal <|-- Duck'"
        )

    def test_fish_inherits_from_animal(self, diagram_content):
        assert "Animal <|-- Fish" in diagram_content, (
            "Fish must inherit from Animal via 'Animal <|-- Fish'"
        )

    def test_no_reverse_inheritance_duck(self, diagram_content):
        assert "Duck <|-- Animal" not in diagram_content, (
            "Animal must not inherit from Duck"
        )

    def test_no_reverse_inheritance_fish(self, diagram_content):
        assert "Fish <|-- Animal" not in diagram_content, (
            "Animal must not inherit from Fish"
        )

    def test_no_circular_inheritance(self, diagram_content):
        assert "Animal <|-- Animal" not in diagram_content
        assert "Duck <|-- Duck" not in diagram_content
        assert "Fish <|-- Fish" not in diagram_content

    def test_exactly_two_inheritance_arrows(self, diagram_content):
        arrows = re.findall(r"<\|--", diagram_content)
        assert len(arrows) == 2, (
            f"Expected exactly 2 inheritance arrows, found {len(arrows)}"
        )


# ---------------------------------------------------------------------------
# Class definitions
# ---------------------------------------------------------------------------


class TestClassDefinitions:
    def test_duck_class_defined(self, diagram_content):
        assert re.search(r"\bclass\s+Duck\s*\{", diagram_content), (
            "Duck class block must be defined"
        )

    def test_fish_class_defined(self, diagram_content):
        assert re.search(r"\bclass\s+Fish\s*\{", diagram_content), (
            "Fish class block must be defined"
        )

    def test_no_duplicate_class_duck(self, diagram_content):
        matches = re.findall(r"\bclass\s+Duck\b", diagram_content)
        assert len(matches) == 1, f"Duck class defined {len(matches)} times, expected 1"

    def test_no_duplicate_class_fish(self, diagram_content):
        matches = re.findall(r"\bclass\s+Fish\b", diagram_content)
        assert len(matches) == 1, f"Fish class defined {len(matches)} times, expected 1"

    def test_class_blocks_are_closed(self, diagram_content):
        # Count opening and closing braces; they must balance for class blocks
        open_braces = diagram_content.count("{")
        close_braces = diagram_content.count("}")
        assert open_braces == close_braces, (
            f"Unbalanced braces: {open_braces} '{{' vs {close_braces} '}}'"
        )


# ---------------------------------------------------------------------------
# Animal members (declared with colon notation, not inside a block)
# ---------------------------------------------------------------------------


class TestAnimalMembers:
    def test_animal_has_int_age(self, diagram_content):
        assert re.search(r"Animal\s*:\s*\+int\s+age", diagram_content), (
            "Animal must declare '+int age'"
        )

    def test_animal_has_string_gender(self, diagram_content):
        assert re.search(r"Animal\s*:\s*\+String\s+gender", diagram_content), (
            "Animal must declare '+String gender'"
        )

    def test_animal_has_isMammal_method(self, diagram_content):
        assert re.search(r"Animal\s*:\s*\+isMammal\(\)", diagram_content), (
            "Animal must declare '+isMammal()'"
        )

    def test_animal_has_mate_method(self, diagram_content):
        assert re.search(r"Animal\s*:\s*\+mate\(\)", diagram_content), (
            "Animal must declare '+mate()'"
        )

    def test_animal_attributes_are_public(self, diagram_content):
        # age and gender must use '+' (public)
        assert re.search(r"Animal\s*:\s*\+int\s+age", diagram_content)
        assert re.search(r"Animal\s*:\s*\+String\s+gender", diagram_content)

    def test_animal_methods_are_public(self, diagram_content):
        assert re.search(r"Animal\s*:\s*\+isMammal\(\)", diagram_content)
        assert re.search(r"Animal\s*:\s*\+mate\(\)", diagram_content)


# ---------------------------------------------------------------------------
# Duck members
# ---------------------------------------------------------------------------


class TestDuckMembers:
    def test_duck_has_beakColor(self, diagram_content):
        assert re.search(r"\+String\s+beakColor", diagram_content), (
            "Duck must declare '+String beakColor'"
        )

    def test_duck_has_swim_method(self, diagram_content):
        assert re.search(r"\+swim\(\)", diagram_content), (
            "Duck must declare '+swim()'"
        )

    def test_duck_has_quack_method(self, diagram_content):
        assert re.search(r"\+quack\(\)", diagram_content), (
            "Duck must declare '+quack()'"
        )

    def test_duck_beakColor_is_public(self, diagram_content):
        assert re.search(r"\+String\s+beakColor", diagram_content), (
            "beakColor must be public ('+' prefix)"
        )

    def test_duck_swim_is_public(self, diagram_content):
        assert re.search(r"\+swim\(\)", diagram_content)

    def test_duck_quack_is_public(self, diagram_content):
        assert re.search(r"\+quack\(\)", diagram_content)

    def test_duck_members_inside_class_block(self, diagram_content):
        # Extract Duck class block and verify members are inside it
        duck_block = re.search(r"class Duck\s*\{([^}]*)\}", diagram_content, re.DOTALL)
        assert duck_block, "Duck class block not found"
        block_body = duck_block.group(1)
        assert "beakColor" in block_body
        assert "swim" in block_body
        assert "quack" in block_body


# ---------------------------------------------------------------------------
# Fish members
# ---------------------------------------------------------------------------


class TestFishMembers:
    def test_fish_has_sizeInFeet(self, diagram_content):
        assert re.search(r"-int\s+sizeInFeet", diagram_content), (
            "Fish must declare '-int sizeInFeet'"
        )

    def test_fish_has_canEat_method(self, diagram_content):
        assert re.search(r"-canEat\(\)", diagram_content), (
            "Fish must declare '-canEat()'"
        )

    def test_fish_sizeInFeet_is_private(self, diagram_content):
        assert re.search(r"-int\s+sizeInFeet", diagram_content), (
            "sizeInFeet must be private ('-' prefix)"
        )

    def test_fish_canEat_is_private(self, diagram_content):
        assert re.search(r"-canEat\(\)", diagram_content), (
            "canEat must be private ('-' prefix)"
        )

    def test_fish_members_inside_class_block(self, diagram_content):
        fish_block = re.search(r"class Fish\s*\{([^}]*)\}", diagram_content, re.DOTALL)
        assert fish_block, "Fish class block not found"
        block_body = fish_block.group(1)
        assert "sizeInFeet" in block_body
        assert "canEat" in block_body

    def test_fish_sizeInFeet_not_public(self, diagram_content):
        # Ensure sizeInFeet is not accidentally marked public
        assert not re.search(r"\+int\s+sizeInFeet", diagram_content), (
            "sizeInFeet should be private, not public"
        )

    def test_fish_canEat_not_public(self, diagram_content):
        assert not re.search(r"\+canEat\(\)", diagram_content), (
            "canEat should be private, not public"
        )


# ---------------------------------------------------------------------------
# Visibility modifiers
# ---------------------------------------------------------------------------


class TestVisibilityModifiers:
    def test_only_valid_visibility_prefixes_used(self, diagram_content):
        # Mermaid supports +, -, #, ~ for visibility
        # All member lines in class blocks should start with a known modifier
        member_lines = re.findall(r"^\s+([+\-#~]\w)", diagram_content, re.MULTILINE)
        valid_prefixes = {"+", "-", "#", "~"}
        for line in member_lines:
            assert line[0] in valid_prefixes, (
                f"Unknown visibility modifier '{line[0]}' found"
            )

    def test_public_members_use_plus(self, diagram_content):
        # beakColor, swim, quack, age, gender, isMammal, mate are public
        public_names = ["beakColor", "swim", "quack", "age", "gender", "isMammal", "mate"]
        for name in public_names:
            assert re.search(rf"\+.*{re.escape(name)}", diagram_content), (
                f"'{name}' should be marked public with '+'"
            )

    def test_private_members_use_minus(self, diagram_content):
        # sizeInFeet and canEat are private
        private_names = ["sizeInFeet", "canEat"]
        for name in private_names:
            assert re.search(rf"-.*{re.escape(name)}", diagram_content), (
                f"'{name}' should be marked private with '-'"
            )


# ---------------------------------------------------------------------------
# Regression / boundary tests
# ---------------------------------------------------------------------------


class TestRegressionAndBoundary:
    def test_diagram_type_is_classDiagram_not_flowchart(self, diagram_content):
        assert not diagram_content.lstrip().startswith("flowchart"), (
            "File must be a classDiagram, not a flowchart"
        )

    def test_no_syntax_config_block(self, diagram_content):
        # class_test.mmd should not have a YAML front-matter config block
        assert not diagram_content.startswith("---"), (
            "class_test.mmd should not contain a YAML config block"
        )

    def test_three_classes_referenced(self, diagram_content):
        # Animal, Duck, Fish must all appear
        for cls in ("Animal", "Duck", "Fish"):
            assert cls in diagram_content, f"Class '{cls}' not found in diagram"

    def test_animal_is_not_defined_with_block_syntax(self, diagram_content):
        # Animal uses colon notation, not a braces block
        assert not re.search(r"class\s+Animal\s*\{", diagram_content), (
            "Animal should use colon notation, not a class block"
        )

    def test_no_extra_unknown_classes(self, diagram_content):
        # Only Animal, Duck, Fish should appear as class identifiers
        class_names = set(re.findall(r"\bclass\s+(\w+)\s*\{", diagram_content))
        assert class_names == {"Duck", "Fish"}, (
            f"Unexpected class blocks found: {class_names}"
        )

    def test_duck_and_fish_do_not_inherit_from_each_other(self, diagram_content):
        assert "Duck <|-- Fish" not in diagram_content
        assert "Fish <|-- Duck" not in diagram_content

    def test_beakColor_type_is_String(self, diagram_content):
        assert re.search(r"\+String\s+beakColor", diagram_content), (
            "beakColor must have type 'String'"
        )

    def test_sizeInFeet_type_is_int(self, diagram_content):
        assert re.search(r"-int\s+sizeInFeet", diagram_content), (
            "sizeInFeet must have type 'int'"
        )

    def test_age_type_is_int(self, diagram_content):
        assert re.search(r"\+int\s+age", diagram_content), (
            "age must have type 'int'"
        )

    def test_gender_type_is_String(self, diagram_content):
        assert re.search(r"\+String\s+gender", diagram_content), (
            "gender must have type 'String'"
        )