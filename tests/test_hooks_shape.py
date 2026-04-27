"""
Hook-script shape tests: every bash hook opens with the subagent-loop guard
and exits 0 fail-open. Naga ships exactly ONE hook by design (skill-invoked
plugin like Wixie).

Run: python -m unittest tests.test_hooks_shape -v
"""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PLUGINS_DIR = REPO_ROOT / "plugins"

GUARD_LINE = 'if [[ -n "${CLAUDE_SUBAGENT:-}" ]]; then'
EXIT_ZERO = "exit 0"


class TestHookShape(unittest.TestCase):
    def test_every_hook_has_subagent_guard(self):
        hooks = list(PLUGINS_DIR.rglob("hooks/*/*.sh"))
        self.assertGreater(len(hooks), 0, "No hook .sh files found under plugins/")
        for path in hooks:
            with self.subTest(hook=str(path.relative_to(REPO_ROOT))):
                text = path.read_text(encoding="utf-8")
                self.assertIn(
                    GUARD_LINE,
                    text,
                    f"{path.name}: missing subagent-loop guard",
                )
                self.assertIn(
                    EXIT_ZERO,
                    text,
                    f"{path.name}: missing fail-open 'exit 0'",
                )

    def test_exactly_one_hook_binding_present(self):
        # Naga is skill-invoked by design like Wixie. PreCompact is the only hook.
        bindings = {
            ("naga-learning", "pre-compact"),
        }
        for plugin, event in bindings:
            with self.subTest(plugin=plugin, event=event):
                d = PLUGINS_DIR / plugin / "hooks" / event
                self.assertTrue(
                    d.is_dir(),
                    f"missing hooks/{event} dir under plugin {plugin}",
                )
                scripts = list(d.glob("*.sh"))
                self.assertGreater(
                    len(scripts), 0, f"no .sh script under {d}"
                )

    def test_no_other_plugin_ships_a_hook(self):
        # Skill-invoked sub-plugins MUST NOT ship a hooks/ directory.
        skill_invoked = {
            "naga-observe", "naga-shift", "naga-validate",
            "naga-cross-repo", "naga-fingerprint", "full",
        }
        for plugin in skill_invoked:
            with self.subTest(plugin=plugin):
                d = PLUGINS_DIR / plugin / "hooks"
                self.assertFalse(
                    d.is_dir(),
                    f"{plugin} must not ship hooks/ — Naga is skill-invoked by design",
                )


if __name__ == "__main__":
    unittest.main()
