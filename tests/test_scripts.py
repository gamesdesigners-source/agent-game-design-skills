import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIX = Path(__file__).resolve().parent / "fixtures"
SK = ROOT / "skills"


def run(script, *args):
    return subprocess.run(
        [sys.executable, str(script), *map(str, args)],
        capture_output=True, text=True,
    )


class RegistryTests(unittest.TestCase):
    script = SK / "gdd-owner" / "scripts" / "validate_registry.py"

    def test_template_registry_is_valid(self):
        r = run(self.script, ROOT / "templates" / "design")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_bad_registry_reports_each_problem(self):
        r = run(self.script, FIX / "registry_bad.yaml")
        self.assertEqual(r.returncode, 1)
        out = r.stdout
        self.assertIn("duplicate id", out)
        self.assertIn("ZON-missing does not exist", out)
        self.assertIn("canon entry refs WPN-club which is proposed", out)
        self.assertIn("canon entry has no file", out)
        self.assertIn("unknown prefix 'BAD'", out)
        self.assertIn("invalid status", out)

    def test_missing_file_is_usage_error(self):
        r = run(self.script, FIX / "nope.yaml")
        self.assertEqual(r.returncode, 2)


class GraphTests(unittest.TestCase):
    script = SK / "level-designer" / "scripts" / "validate_graph.py"

    def test_valid_graph_with_key_gate(self):
        r = run(self.script, FIX / "graph_ok.json")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_gate_before_key_is_respected(self):
        # Key sits in a branch that is only reachable AFTER the gate -> must fail.
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "g.json"
            p.write_text(json.dumps({
                "nodes": [{"id": "s", "type": "start"}, {"id": "a"}, {"id": "e", "type": "end"}],
                "edges": [
                    {"from": "s", "to": "a", "gated_by": "K"},
                    {"from": "a", "to": "e"},
                ],
                "grants": {"a": ["K"]},
            }))
            r = run(self.script, p)
            self.assertEqual(r.returncode, 1)
            self.assertIn("G03", r.stdout)

    def test_softlock_and_problems_detected(self):
        r = run(self.script, FIX / "graph_softlock.json")
        self.assertEqual(r.returncode, 1)
        self.assertIn("G04 soft-lock: pit", r.stdout)
        self.assertIn("G03 node unreachable from start: orphan", r.stdout)
        self.assertIn("G02 edge references unknown node", r.stdout)
        self.assertIn("G06 gate start -> end needs ITM-never", r.stdout)


class CombatTests(unittest.TestCase):
    script = SK / "combat-balancer" / "scripts" / "ttk_matrix.py"

    def test_matrix_and_flags(self):
        r = run(self.script, FIX / "combat.json")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("TTK matrix", r.stdout)
        self.assertIn("DEAD", r.stdout)  # the twig
        self.assertIn("WPN-twig", r.stdout)

    def test_json_math(self):
        r = run(self.script, FIX / "combat.json", "--json")
        data = json.loads(r.stdout)
        # short sword vs goblin: 12 dmg * (1 + .1*.5) * 2.0 * .9 = 22.68 dps -> 30/22.68
        cell = data["matrix"]["WPN-short-sword|ENM-goblin"]
        self.assertAlmostEqual(cell["dps"], 22.68, places=2)
        self.assertAlmostEqual(cell["ttk"], 30 / 22.68, places=3)

    def test_armor_floor(self):
        # twig deals 1; armor 6 would reduce below zero -> floored at 0.1
        r = run(self.script, FIX / "combat.json", "--json")
        data = json.loads(r.stdout)
        self.assertAlmostEqual(data["matrix"]["WPN-twig|ENM-ogre"]["dps"], 0.1, places=3)


class EconomyTests(unittest.TestCase):
    script = SK / "economy-designer" / "scripts" / "economy_sim.py"

    def test_runs_and_flags_dead_currency(self):
        r = run(self.script, FIX / "economy.json", "--runs", "20", "--seed", "3")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("NO_SOURCE", r.stdout)   # CUR-dust has no source
        self.assertIn("ITM-iron-sword", r.stdout)

    def test_deterministic_with_seed(self):
        a = run(self.script, FIX / "economy.json", "--runs", "10", "--seed", "7", "--json")
        b = run(self.script, FIX / "economy.json", "--runs", "10", "--seed", "7", "--json")
        self.assertEqual(a.stdout, b.stdout)

    def test_bad_input(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.json"
            p.write_text("{not json")
            self.assertEqual(run(self.script, p).returncode, 2)


class XpCurveTests(unittest.TestCase):
    script = SK / "progression-difficulty" / "scripts" / "xp_curve.py"

    def test_exponential_costs(self):
        r = run(self.script, "--levels", "1-5", "--kind", "exp", "--base", "100",
                "--growth", "2", "--xp-per-hour", "1000", "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = json.loads(r.stdout)["rows"]
        self.assertEqual([round(x["xp_to_next"]) for x in rows], [100, 200, 400, 800])

    def test_wall_flag_when_income_flat(self):
        r = run(self.script, "--levels", "1-10", "--kind", "exp", "--base", "100",
                "--growth", "2.5", "--xp-per-hour", "1000")
        self.assertIn("WALL", r.stdout)

    def test_target_miss(self):
        r = run(self.script, "--levels", "1-10", "--target-hours", "1")
        self.assertIn("TARGET", r.stdout)

    def test_bad_option(self):
        self.assertEqual(run(self.script, "--bogus", "1").returncode, 2)


class LintTests(unittest.TestCase):
    def test_repo_skills_pass_lint(self):
        r = run(ROOT / "scripts" / "lint_skills.py")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_lint_catches_problems(self):
        with tempfile.TemporaryDirectory() as d:
            skill = Path(d) / "broken-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: other-name\ndescription: short\n---\n# Broken\n"
            )
            r = run(ROOT / "scripts" / "lint_skills.py", d)
            self.assertEqual(r.returncode, 1)
            self.assertIn("L02", r.stdout)
            self.assertIn("L03", r.stdout)
            self.assertIn("L04", r.stdout)


if __name__ == "__main__":
    unittest.main()
