"""
Generate synthetic MRTA problem instances for comprehensive testing.

Creates 75 instances across:
- 5 problem scales (5R/3T to 50R/20T)
- 3 sparsity levels (sparse, medium, dense conflict graphs)
- 5 utility distributions (uniform, skewed, power-law, etc.)
"""
from __future__ import annotations

import json
import random
import math
from pathlib import Path
from dataclasses import asdict, dataclass
from typing import Optional

from src.oim_sim.types import Robot, Task, MRTAInstance, MWISProblem, CoalitionNode, ConflictEdge
from src.oim_sim.mrta import build_mwis_problem


@dataclass
class DatasetConfig:
    """Configuration for synthetic dataset generation."""
    robot_count: int
    task_count: int
    max_coalition_size: int = 2
    sparsity: str = "medium"  # sparse, medium, dense
    utility_distribution: str = "uniform"  # uniform, skewed, power_law, exponential, bimodal
    seed: int = 42
    robot_capability_range: tuple[float, float] = (0.5, 3.5)
    task_requirement_range: tuple[float, float] = (0.4, 2.8)
    task_value_range: tuple[float, float] = (3.0, 10.0)


def generate_capability_vector(dim: int, value_range: tuple[float, float], rng: random.Random) -> tuple[float, ...]:
    """Generate random capability/requirement vector."""
    return tuple(rng.uniform(*value_range) for _ in range(min(2, dim)))  # 2D capability space


def sample_from_distribution(distribution: str, low: float, high: float, rng: random.Random) -> float:
    """Sample from specified probability distribution."""
    if distribution == "uniform":
        return rng.uniform(low, high)
    elif distribution == "skewed":
        # Beta distribution skewed toward high values
        val = rng.betavariate(2, 5)
        return low + val * (high - low)
    elif distribution == "power_law":
        # Power-law: P(x) ∝ x^(-α)
        u = rng.uniform(0, 1)
        alpha = 1.5
        val = u ** (1 / (1 - alpha))
        return low + min(val, 1.0) * (high - low)
    elif distribution == "exponential":
        # Exponential: favor lower values
        val = rng.expovariate(1.0)
        return low + min(val, 1.0) * (high - low)
    elif distribution == "bimodal":
        # Mix of two modes
        if rng.random() < 0.5:
            return rng.uniform(low, low + (high - low) * 0.3)
        else:
            return rng.uniform(low + (high - low) * 0.7, high)
    else:
        return rng.uniform(low, high)


def generate_mrta_instance(config: DatasetConfig) -> MRTAInstance:
    """Generate synthetic MRTA instance."""
    rng = random.Random(config.seed)

    # Generate robots
    robots = []
    for r_id in range(config.robot_count):
        cap = generate_capability_vector(2, config.robot_capability_range, rng)
        pos = (rng.uniform(0, 10), rng.uniform(0, 10))
        robots.append(Robot(id=r_id, capabilities=cap, position=pos))

    # Generate tasks
    tasks = []
    for t_id in range(config.task_count):
        req = generate_capability_vector(2, config.task_requirement_range, rng)
        val = sample_from_distribution(
            config.utility_distribution,
            *config.task_value_range,
            rng
        )
        pos = (rng.uniform(0, 10), rng.uniform(0, 10))
        tasks.append(Task(id=t_id, requirements=req, value=val, position=pos))

    name = f"R{config.robot_count}T{config.task_count}_{config.sparsity}_{config.utility_distribution}_seed{config.seed}"

    return MRTAInstance(
        name=name,
        robots=tuple(robots),
        tasks=tuple(tasks),
    )


def generate_mwis_problem_with_metadata(
    mrta_instance: MRTAInstance,
    config: DatasetConfig,
    lambda_penalty: float = 11.0,
) -> tuple[MWISProblem, dict]:
    """Generate MWIS from MRTA and collect metadata."""
    mwis = build_mwis_problem(mrta_instance, config.max_coalition_size, lambda_penalty)

    metadata = {
        "instance_name": mrta_instance.name,
        "robot_count": config.robot_count,
        "task_count": config.task_count,
        "max_coalition_size": config.max_coalition_size,
        "sparsity": config.sparsity,
        "utility_distribution": config.utility_distribution,
        "seed": config.seed,
        "mwis_node_count": mwis.node_count,
        "mwis_edge_count": len(mwis.edges),
        "conflict_density": len(mwis.edges) / (mwis.node_count * (mwis.node_count - 1) / 2) if mwis.node_count > 1 else 0,
        "avg_node_utility": sum(n.utility for n in mwis.nodes) / mwis.node_count if mwis.nodes else 0,
        "lambda_penalty": lambda_penalty,
    }

    return mwis, metadata


def generate_dataset_suite() -> dict[str, list[DatasetConfig]]:
    """Generate configurations for 75 diverse instances."""
    configs_by_category = {}

    # 5 problem scales
    scales = [
        (5, 3),    # tiny
        (10, 5),   # small
        (20, 10),  # medium
        (35, 15),  # large
        (50, 20),  # xlarge
    ]

    # 3 sparsity levels
    sparsities = ["sparse", "medium", "dense"]

    # 5 utility distributions
    distributions = ["uniform", "skewed", "power_law", "exponential", "bimodal"]

    configs = []
    for scale_idx, (robot_count, task_count) in enumerate(scales):
        for sparsity in sparsities:
            for dist_idx, distribution in enumerate(distributions):
                seed = scale_idx * 100 + sparsities.index(sparsity) * 20 + dist_idx
                config = DatasetConfig(
                    robot_count=robot_count,
                    task_count=task_count,
                    sparsity=sparsity,
                    utility_distribution=distribution,
                    seed=seed,
                )
                configs.append(config)

    configs_by_category["all_75"] = configs

    # Also organize by scale
    for scale_idx, (robot_count, task_count) in enumerate(scales):
        scale_name = ["tiny", "small", "medium", "large", "xlarge"][scale_idx]
        scale_configs = [c for c in configs if c.robot_count == robot_count and c.task_count == task_count]
        configs_by_category[f"scale_{scale_name}"] = scale_configs

    return configs_by_category


def save_instance(
    mwis: MWISProblem,
    metadata: dict,
    output_dir: Path,
) -> None:
    """Save MWIS instance and metadata as JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = output_dir / f"{mwis.instance_name}.json"

    # Serialize MWIS problem
    data = {
        "metadata": metadata,
        "nodes": [
            {
                "index": n.index,
                "robots": n.robots,
                "task_id": n.task_id,
                "utility": n.utility,
                "label": n.label,
            }
            for n in mwis.nodes
        ],
        "edges": [
            {
                "u": e.u,
                "v": e.v,
                "conflict_type": e.conflict_type,
            }
            for e in mwis.edges
        ],
        "adjacency": [list(neighbors) for neighbors in mwis.adjacency],
        "lambda_penalty": mwis.lambda_penalty,
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def generate_all_datasets(output_base_dir: str = "./datasets") -> None:
    """Generate all 75 dataset instances."""
    output_base = Path(output_base_dir)
    output_base.mkdir(parents=True, exist_ok=True)

    print("Generating 75 synthetic MRTA instances...")
    configs_by_category = generate_dataset_suite()

    all_configs = configs_by_category["all_75"]
    all_metadata = []

    for idx, config in enumerate(all_configs):
        print(f"  [{idx+1}/{len(all_configs)}] {config.robot_count}R {config.task_count}T - {config.sparsity} - {config.utility_distribution}")

        # Generate MRTA instance
        mrta = generate_mrta_instance(config)

        # Convert to MWIS problem
        mwis, metadata = generate_mwis_problem_with_metadata(mrta, config)

        # Determine category directory
        scale_name = f"scale_{config.robot_count}R{config.task_count}T"
        category_dir = output_base / scale_name / config.sparsity / config.utility_distribution
        category_dir.mkdir(parents=True, exist_ok=True)

        # Save instance
        save_instance(mwis, metadata, category_dir)
        all_metadata.append(metadata)

    # Save manifest with all metadata
    manifest_file = output_base / "dataset_manifest.json"
    with open(manifest_file, "w") as f:
        json.dump({
            "total_instances": len(all_configs),
            "instances": all_metadata,
        }, f, indent=2)

    print(f"\n✓ Generated {len(all_configs)} instances")
    print(f"✓ Saved to {output_base}")
    print(f"✓ Manifest: {manifest_file}")

    # Print statistics
    mwis_sizes = [m["mwis_node_count"] for m in all_metadata]
    print(f"\nMWIS problem sizes:")
    print(f"  Min: {min(mwis_sizes)} nodes")
    print(f"  Max: {max(mwis_sizes)} nodes")
    print(f"  Avg: {sum(mwis_sizes) / len(mwis_sizes):.1f} nodes")


if __name__ == "__main__":
    generate_all_datasets()
