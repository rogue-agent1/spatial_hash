#!/usr/bin/env python3
"""Spatial hash grid — O(1) neighbor queries for uniform distributions."""
import sys, random, math
from collections import defaultdict

class SpatialHash:
    def __init__(self, cell_size=10):
        self.cell = cell_size; self.grid = defaultdict(list); self.objects = {}
    def _key(self, x, y):
        return (int(x // self.cell), int(y // self.cell))
    def insert(self, id, x, y):
        k = self._key(x, y)
        self.grid[k].append(id)
        self.objects[id] = (x, y)
    def query(self, x, y, radius):
        results = []
        cr = int(radius // self.cell) + 1
        cx, cy = int(x // self.cell), int(y // self.cell)
        for dx in range(-cr, cr+1):
            for dy in range(-cr, cr+1):
                for id in self.grid.get((cx+dx, cy+dy), []):
                    ox, oy = self.objects[id]
                    d = math.sqrt((ox-x)**2 + (oy-y)**2)
                    if d <= radius:
                        results.append((d, id, ox, oy))
        return sorted(results)
    def stats(self):
        counts = [len(v) for v in self.grid.values()]
        return {"cells": len(self.grid), "objects": len(self.objects),
                "avg_per_cell": sum(counts)/len(counts) if counts else 0,
                "max_per_cell": max(counts) if counts else 0}

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    random.seed(42)
    sh = SpatialHash(cell_size=10)
    for i in range(n):
        sh.insert(i, random.uniform(0, 200), random.uniform(0, 200))
    query = (100.0, 100.0)
    near = sh.query(*query, radius=15)
    stats = sh.stats()
    print(f"Spatial Hash: {n} objects, cell=10")
    print(f"Cells: {stats['cells']}, avg {stats['avg_per_cell']:.1f}/cell, max {stats['max_per_cell']}")
    print(f"\nQuery ({query[0]}, {query[1]}) r=15: {len(near)} found")
    for d, id, x, y in near[:5]:
        print(f"  #{id}: ({x:.1f}, {y:.1f}) d={d:.2f}")
