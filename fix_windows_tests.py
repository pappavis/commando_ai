"""
User story:
As a Windows developer, I want the retro-reverse-engineer tests to handle
UTF-8 Markdown files and unavailable symbolic-link privileges correctly,
so that the test suite produces platform-independent results.

Version: 1.0.0
ChatID: A3F7C1D9
"""

from __future__ import annotations

from pathlib import Path


VERSION = "1.0.0"
CHAT_ID = "A3F7C1D9"

TEST_FILE = Path(
    "skills",
    "retro-reverse-engineer",
    "tests",
    "test_generator.py",
)


class WindowsTestFixer:
    """Apply the minimal Windows compatibility fixes to test_generator.py."""

    def __init__(self, test_file: Path) -> None:
        self.test_file = test_file

    def run(self) -> None:
        print(f"Windows Test Fixer Version: {VERSION}")
        print(f"ChatID: {CHAT_ID}")
        print(f"Target: {self.test_file}")

        if not self.test_file.is_file():
            raise FileNotFoundError(
                f"Test file not found: {self.test_file}\n"
                "Run this program from the commando_ai repository root."
            )

        original = self.test_file.read_text(encoding="utf-8")
        updated = original

        updated, encoding_replacements = self._fix_utf8_reads(updated)
        updated, symlink_replacements = self._fix_symlink_test(updated)

        if updated == original:
            print("No changes were required.")
            print("The Windows compatibility fixes may already be installed.")
            return

        backup_file = self.test_file.with_suffix(".py.before_windows_fix")
        backup_file.write_text(original, encoding="utf-8", newline="\n")
        self.test_file.write_text(updated, encoding="utf-8", newline="\n")

        print(f"UTF-8 read replacements: {encoding_replacements}")
        print(f"Symlink test replacements: {symlink_replacements}")
        print(f"Backup created: {backup_file}")
        print("Fix applied successfully.")

    @staticmethod
    def _fix_utf8_reads(content: str) -> tuple[str, int]:
        old_text = ".read_text()"
        new_text = '.read_text(encoding="utf-8")'

        replacement_count = content.count(old_text)
        updated = content.replace(old_text, new_text)

        return updated, replacement_count

    @staticmethod
    def _fix_symlink_test(content: str) -> tuple[str, int]:
        old_text = (
            "out=self.root/'konsep';"
            "out.symlink_to(self.root/'ontbreek')"
        )

        new_text = """out = self.root / 'konsep'
        try:
            out.symlink_to(self.root / 'ontbreek')
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                self.skipTest(
                    "Windows symbolic-link privilege is unavailable. "
                    "Enable Developer Mode or run with suitable privileges."
                )
            raise"""

        replacement_count = content.count(old_text)

        if replacement_count > 1:
            raise RuntimeError(
                "The expected symlink statement occurs more than once. "
                "No ambiguous replacement will be performed."
            )

        if replacement_count == 0:
            already_fixed = (
                'getattr(exc, "winerror", None) == 1314' in content
                or "getattr(exc, 'winerror', None) == 1314" in content
            )

            if already_fixed:
                return content, 0

            raise RuntimeError(
                "The expected symlink statement was not found. "
                "The test file may have changed since this fix was prepared."
            )

        updated = content.replace(old_text, new_text)
        return updated, replacement_count


def main() -> None:
    fixer = WindowsTestFixer(TEST_FILE)
    fixer.run()


if __name__ == "__main__":
    main()
