import { describe, expect, it } from "vitest";
import { screenSet } from "./definitions";
import { auditRegistries } from "./registryAudit";
describe("screen registry audit", () => { it("accepts the production catalogue", () => expect(auditRegistries(screenSet)).toEqual([])); });
