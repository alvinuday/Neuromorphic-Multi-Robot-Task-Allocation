from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Robot:
    id: int
    capabilities: tuple[float, ...]
    position: tuple[float, float]


@dataclass(frozen=True)
class Task:
    id: int
    requirements: tuple[float, ...]
    value: float
    position: tuple[float, float]


@dataclass(frozen=True)
class MRTAInstance:
    name: str
    robots: tuple[Robot, ...]
    tasks: tuple[Task, ...]


@dataclass(frozen=True)
class CoalitionNode:
    index: int
    robots: tuple[int, ...]
    task_id: int
    utility: float
    label: str


@dataclass(frozen=True)
class ConflictEdge:
    u: int
    v: int
    conflict_type: str


@dataclass
class MWISProblem:
    instance_name: str
    nodes: list[CoalitionNode]
    adjacency: list[set[int]]
    edges: list[ConflictEdge]
    lambda_penalty: float

    @property
    def node_count(self) -> int:
        return len(self.nodes)


@dataclass
class SolverResult:
    name: str
    selected: list[int]
    utility: float
    feasible: bool
    runtime_ms: float
    metadata: dict[str, Any] = field(default_factory=dict)
