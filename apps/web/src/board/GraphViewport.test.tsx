import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { GraphViewport } from "./GraphViewport";
import type { Graph } from "../api/contracts";

const graph = {
  projection_version: "1",
  nodes: [
    { record_id: "P1", record_type: "PERSON_RECORD", record_subtype: "", label: "Puppy One", source_system_id: "s1", provenance_ref: "r1", safe_summary: "A person." },
    { record_id: "O1", record_type: "ORGANIZATION_RECORD", record_subtype: "", label: "Office One", source_system_id: "s2", provenance_ref: "r2", safe_summary: "An organization." },
  ],
  edges: [{ relationship_id: "E1", source_record_id: "P1", target_record_id: "O1", relationship_family: "DIRECT_SOURCE", relationship_type: "WORKS_FOR", directed: true, provenance: "r3", event_time: "", player_safe_summary: "A published relationship." }],
  node_count: 2,
  edge_count: 1,
} satisfies Graph;

describe("GraphViewport", () => {
  it("supports zoom, layout, family filtering, and semantic selection", () => {
    const onNodeSelect = vi.fn();
    render(<GraphViewport graph={graph} onNodeSelect={onNodeSelect} />);
    expect(screen.getByText("2 visible nodes · 1 visible relationships")).toBeVisible();
    fireEvent.click(screen.getByRole("button", { name: "Zoom in" }));
    fireEvent.click(screen.getByRole("button", { name: "Circle layout" }));
    fireEvent.click(screen.getByRole("checkbox", { name: "DIRECT_SOURCE" }));
    expect(screen.getByText("2 visible nodes · 1 visible relationships")).toBeVisible();
    fireEvent.click(screen.getByRole("checkbox", { name: "DIRECT_SOURCE" }));
    expect(screen.getByText("2 visible nodes · 0 visible relationships")).toBeVisible();
    fireEvent.click(screen.getByText("Semantic evidence list"));
    fireEvent.click(screen.getByRole("button", { name: /Puppy One \(P1\)/ }));
    expect(onNodeSelect).toHaveBeenCalledWith("P1");
  });

  it("collapses and restores a node without changing the source graph", () => {
    render(<GraphViewport graph={graph} />);
    fireEvent.click(screen.getByRole("button", { name: "Collapse Puppy One" }));
    expect(screen.queryByRole("button", { name: "Puppy One, P1" })).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Restore Puppy One" })).toBeVisible();
    fireEvent.click(screen.getByRole("button", { name: "Restore Puppy One" }));
    expect(screen.getByRole("button", { name: "Puppy One, P1" })).toBeVisible();
  });
});
