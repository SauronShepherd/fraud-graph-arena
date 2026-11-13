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
  it("renders a 100-node graph fixture with stable scoped counts", () => {
    const nodes = Array.from({ length: 100 }, (_, index) => ({ record_id: `N${index.toString().padStart(3, "0")}`, record_type: "PERSON_RECORD" as const, record_subtype: "", label: `Node ${index}`, source_system_id: "benchmark", provenance_ref: `r${index}`, safe_summary: "Published benchmark record." }));
    const edges = nodes.slice(1).map((node, index) => ({ relationship_id: `E${index.toString().padStart(3, "0")}`, source_record_id: nodes[index].record_id, target_record_id: node.record_id, relationship_family: "DIRECT_SOURCE", relationship_type: "LINKED", directed: true, provenance: `e${index}`, event_time: "", player_safe_summary: "Published benchmark relationship." }));
    render(<GraphViewport graph={{ projection_version: "1", nodes, edges, node_count: nodes.length, edge_count: edges.length }} />);
    expect(screen.getByText("100 visible nodes · 99 visible relationships")).toBeVisible();
    expect(screen.getByRole("img", { name: "100 nodes in current graph view" })).toBeVisible();
  });

  it("announces omitted graph content when the projection is partial", () => {
    render(<GraphViewport graph={{ ...graph, partial: true, omitted_node_count: 4, omitted_edge_count: 7 }} />);
    expect(screen.getByRole("status")).toHaveTextContent("Partial view · 4 nodes and 7 relationships omitted");
  });

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
    fireEvent.click(screen.getByRole("button", { name: "Focus selection" }));
    expect(screen.getByRole("button", { name: "Show all nodes" })).toBeVisible();
    expect(screen.getByRole("img", { name: /nodes in current graph view/i })).toBeVisible();
  });

  it("reports controlled relationship filters so the workspace can preserve them", () => {
    const onRelationshipFamiliesChange = vi.fn();
    render(<GraphViewport graph={graph} relationshipFamilies={null} onRelationshipFamiliesChange={onRelationshipFamiliesChange} />);
    fireEvent.click(screen.getByRole("checkbox", { name: "DIRECT_SOURCE" }));
    expect(onRelationshipFamiliesChange).toHaveBeenCalledWith(["DIRECT_SOURCE"]);
    fireEvent.click(screen.getByRole("button", { name: "Reset view" }));
    expect(onRelationshipFamiliesChange).toHaveBeenLastCalledWith(null);
  });

  it("collapses and restores a node without changing the source graph", () => {
    const { container } = render(<GraphViewport graph={graph} />);
    fireEvent.click(screen.getByRole("button", { name: "Collapse Puppy One" }));
    expect(screen.getByText("1 visible nodes · 0 visible relationships")).toBeVisible();
    expect(screen.queryByRole("button", { name: "Puppy One, P1" })).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Restore Puppy One" })).toBeVisible();
    expect(container.querySelectorAll(".graph-minimap circle")).toHaveLength(1);
    expect(container.querySelector(".graph-minimap rect")).not.toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "Restore Puppy One" }));
    expect(screen.getByRole("button", { name: "Puppy One, P1" })).toBeVisible();
  });

  it("clears selection when the selected node is collapsed", () => {
    const onNodeSelect = vi.fn();
    render(<GraphViewport graph={graph} onNodeSelect={onNodeSelect} />);
    fireEvent.click(screen.getByRole("button", { name: "Puppy One, P1" }));
    expect(screen.getByRole("button", { name: "Fit selection" })).toBeEnabled();
    fireEvent.click(screen.getByRole("button", { name: "Collapse Puppy One" }));
    expect(screen.getByRole("button", { name: "Fit selection" })).toBeDisabled();
    expect(onNodeSelect).toHaveBeenLastCalledWith(null);
  });

  it("renders directed relationships with an arrow marker", () => {
    const { container } = render(<GraphViewport graph={graph} />);
    expect(container.querySelector('line[marker-end="url(#graph-arrow)"]')).toBeTruthy();
  });

  it("supports keyboard-operable pan and fit controls", () => {
    render(<GraphViewport graph={graph} />);
    const transform = screen.getByTestId("graph-transform");
    const before = transform.getAttribute("transform");
    fireEvent.click(screen.getByRole("button", { name: "Pan right" }));
    expect(transform.getAttribute("transform")).not.toBe(before);
    fireEvent.click(screen.getByRole("button", { name: "Puppy One, P1" }));
    expect(screen.getByRole("button", { name: "Fit selection" })).toBeEnabled();
    fireEvent.click(screen.getByRole("button", { name: "Fit selection" }));
    fireEvent.click(screen.getByRole("button", { name: "Fit graph" }));
  });

  it("fits the selected node with its visible one-hop context", () => {
    const contextGraph = {
      ...graph,
      nodes: [
        ...graph.nodes,
        { record_id: "A1", record_type: "ACCOUNT_RECORD" as const, record_subtype: "", label: "Account One", source_system_id: "s3", provenance_ref: "r4", safe_summary: "An account." },
      ],
      edges: [
        ...graph.edges,
        { relationship_id: "E2", source_record_id: "P1", target_record_id: "A1", relationship_family: "DIRECT_SOURCE", relationship_type: "USES", directed: true, provenance: "r5", event_time: "", player_safe_summary: "A second published relationship." },
      ],
      node_count: 3,
      edge_count: 2,
    } satisfies Graph;
    render(<GraphViewport graph={contextGraph} />);
    fireEvent.click(screen.getByRole("button", { name: "Puppy One, P1" }));
    const transform = screen.getByTestId("graph-transform");
    fireEvent.click(screen.getByRole("button", { name: "Fit selection" }));
    expect(transform.getAttribute("transform")).toContain("scale(1.46875)");
  });

  it("shows hover previews without replacing the selected record", () => {
    const { container } = render(<GraphViewport graph={graph} />);
    fireEvent.click(screen.getByRole("button", { name: "Puppy One, P1" }));
    const inspector = container.querySelector(".graph-inspector strong");
    expect(inspector?.textContent).toBe("Puppy One");
    const edge = container.querySelector('[data-edge-id="E1"]');
    expect(edge).not.toBeNull();
    fireEvent.mouseEnter(edge!);
    expect(inspector?.textContent).toBe("WORKS_FOR");
    fireEvent.mouseLeave(edge!);
    expect(inspector?.textContent).toBe("Puppy One");
  });
});
