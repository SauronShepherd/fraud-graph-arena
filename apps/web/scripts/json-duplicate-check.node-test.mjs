import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { parseJsonRejectDuplicateKeys } from "./json-duplicate-check.mjs";

test("parses valid nested JSON and escaped keys", () => {
  assert.deepEqual(parseJsonRejectDuplicateKeys('{"a":{"x\\u0061":1},"b":[true,null]}'), { a: { xa: 1 }, b: [true, null] });
});

test("rejects duplicate keys in the root and nested objects", () => {
  assert.throws(() => parseJsonRejectDuplicateKeys('{"screen_set_id":"FGA03","screen_set_id":"other"}'), /Duplicate JSON key/);
  assert.throws(() => parseJsonRejectDuplicateKeys('{"screen":{"id":"LAUNCH","id":"CASE"}}'), /Duplicate JSON key/);
});

test("Node build validator rejects the shared semantic-invalid screen fixtures", (context) => {
  const fixtures = JSON.parse(readFileSync("src/screen-system/test-fixtures/validation-cases.json", "utf8"));
  const baseline = JSON.parse(readFileSync("src/screen-system/definitions/fga-screen-set.v1.json", "utf8"));
  const directory = mkdtempSync(join(tmpdir(), "fga-screen-validation-"));
  context.after(() => rmSync(directory, { recursive: true, force: true }));

  for (const fixture of fixtures) {
    const candidate = structuredClone(baseline);
    let target = candidate;
    for (const segment of fixture.path.slice(0, -1)) target = target[segment];
    target[fixture.path.at(-1)] = fixture.value;
    const path = join(directory, `${fixture.name.replaceAll(" ", "-")}.json`);
    writeFileSync(path, JSON.stringify(candidate));
    const result = spawnSync(process.execPath, ["scripts/validate-screen-set.mjs", path], { encoding: "utf8" });
    assert.notEqual(result.status, 0, `${fixture.name} unexpectedly passed`);
    assert.match(result.stderr, /Invalid screen set/, `${fixture.name} had no stable diagnostic`);
  }
});
