"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { api } from "@/lib/api/client";
import type { SampleDocument } from "@/lib/types";

interface SampleGovernancePanelProps {
  onImported?: () => void;
}

export function SampleGovernancePanel({ onImported }: SampleGovernancePanelProps) {
  const [samples, setSamples] = useState<SampleDocument[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [selectedSampleId, setSelectedSampleId] = useState<string>("");
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);
  const [importing, setImporting] = useState(false);
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadSamples = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.listSampleDocuments();
      setSamples(data.samples);
      setCategories(data.categories);
      const firstAvailable = data.samples.find((sample) => !sample.already_imported);
      setSelectedSampleId(firstAvailable?.sample_id ?? data.samples[0]?.sample_id ?? "");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load sample documents");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadSamples();
  }, [loadSamples]);

  const filteredSamples = useMemo(() => {
    if (selectedCategory === "all") return samples;
    return samples.filter((sample) => sample.category === selectedCategory);
  }, [samples, selectedCategory]);

  const selectedSample = samples.find((sample) => sample.sample_id === selectedSampleId);

  useEffect(() => {
    if (!filteredSamples.some((sample) => sample.sample_id === selectedSampleId)) {
      setSelectedSampleId(filteredSamples[0]?.sample_id ?? "");
    }
  }, [filteredSamples, selectedSampleId]);

  function toggleSelection(sampleId: string) {
    setSelectedIds((current) => {
      const next = new Set(current);
      if (next.has(sampleId)) {
        next.delete(sampleId);
      } else {
        next.add(sampleId);
      }
      return next;
    });
  }

  function selectVisible() {
    setSelectedIds(new Set(filteredSamples.map((sample) => sample.sample_id)));
  }

  function clearSelection() {
    setSelectedIds(new Set());
  }

  async function importSamples(sampleIds: string[]) {
    if (sampleIds.length === 0) return;
    setImporting(true);
    setError(null);
    setStatus(null);
    try {
      const result = await api.importSampleDocuments(sampleIds);
      const importedCount = result.imported.length;
      const skippedCount = result.skipped.length;
      const errorCount = result.errors.length;
      const parts = [];
      if (importedCount > 0) parts.push(`${importedCount} added`);
      if (skippedCount > 0) parts.push(`${skippedCount} already in corpus`);
      if (errorCount > 0) parts.push(`${errorCount} failed`);
      setStatus(parts.join(", ") || "No changes made");
      setSelectedIds(new Set());
      await loadSamples();
      onImported?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Import failed");
    } finally {
      setImporting(false);
    }
  }

  return (
    <div className="rounded-lg border border-paper-line bg-ivory p-6 shadow-sm">
      <h2 className="mb-2 text-lg font-semibold text-charcoal">Add Governance References</h2>
      <p className="mb-4 text-sm text-slate-gray">
        Start with curated AI governance sources from NIST, GovAI Coalition, universities, and
        public-sector guidance. You can still upload your own files below.
      </p>

      {loading && <p className="text-sm text-slate-gray">Loading sample library...</p>}
      {error && (
        <p className="text-sm text-overruled-red" role="alert">
          {error}
        </p>
      )}

      {!loading && samples.length > 0 && (
        <div className="space-y-4">
          <div className="grid gap-3 md:grid-cols-2">
            <label className="block text-sm">
              <span className="mb-1 block font-medium text-charcoal">Category</span>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full rounded-md border border-paper-line bg-white px-3 py-2 text-sm"
                aria-label="Governance document category"
              >
                <option value="all">All categories</option>
                {categories.map((category) => (
                  <option key={category} value={category}>
                    {category}
                  </option>
                ))}
              </select>
            </label>

            <label className="block text-sm">
              <span className="mb-1 block font-medium text-charcoal">Document</span>
              <select
                value={selectedSampleId}
                onChange={(e) => setSelectedSampleId(e.target.value)}
                className="w-full rounded-md border border-paper-line bg-white px-3 py-2 text-sm"
                aria-label="Governance document"
              >
                {filteredSamples.map((sample) => (
                  <option key={sample.sample_id} value={sample.sample_id}>
                    {sample.title}
                    {sample.already_imported ? " (in corpus)" : ""}
                  </option>
                ))}
              </select>
            </label>
          </div>

          {selectedSample && (
            <div className="rounded-md border border-paper-line bg-parchment/40 p-4 text-sm">
              <p className="font-medium text-charcoal">{selectedSample.title}</p>
              <p className="mt-1 text-slate-gray">{selectedSample.description}</p>
              {selectedSample.good_for && (
                <p className="mt-2 text-slate-gray">
                  <span className="font-medium text-charcoal">Good for:</span>{" "}
                  {selectedSample.good_for}
                </p>
              )}
              <a
                href={selectedSample.url}
                target="_blank"
                rel="noreferrer"
                className="mt-2 inline-block text-verdict-teal hover:underline"
              >
                View official source
              </a>
            </div>
          )}

          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              disabled={importing || !selectedSampleId}
              onClick={() => importSamples([selectedSampleId])}
              className="rounded-md bg-gavel-gold px-4 py-2 text-sm font-medium text-deep-ink hover:opacity-90 disabled:opacity-50"
            >
              {importing ? "Adding..." : "Add Selected Document"}
            </button>
            <button
              type="button"
              disabled={importing}
              onClick={() => importSamples(filteredSamples.map((sample) => sample.sample_id))}
              className="rounded-md border border-paper-line px-4 py-2 text-sm hover:bg-parchment disabled:opacity-50"
            >
              Add All in Category
            </button>
          </div>

          <details className="rounded-md border border-paper-line bg-white p-4">
            <summary className="cursor-pointer text-sm font-medium text-charcoal">
              Select multiple documents
            </summary>
            <div className="mt-3 space-y-2">
              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  onClick={selectVisible}
                  className="rounded-md border border-paper-line px-3 py-1 text-xs hover:bg-parchment"
                >
                  Select visible
                </button>
                <button
                  type="button"
                  onClick={clearSelection}
                  className="rounded-md border border-paper-line px-3 py-1 text-xs hover:bg-parchment"
                >
                  Clear selection
                </button>
                <button
                  type="button"
                  disabled={importing || selectedIds.size === 0}
                  onClick={() => importSamples(Array.from(selectedIds))}
                  className="rounded-md bg-gavel-gold px-3 py-1 text-xs font-medium text-deep-ink disabled:opacity-50"
                >
                  Add {selectedIds.size} selected
                </button>
              </div>
              <div className="max-h-56 space-y-2 overflow-y-auto pr-1">
                {filteredSamples.map((sample) => (
                  <label
                    key={sample.sample_id}
                    className="flex items-start gap-2 rounded border border-paper-line/70 p-2 text-sm"
                  >
                    <input
                      type="checkbox"
                      checked={selectedIds.has(sample.sample_id)}
                      onChange={() => toggleSelection(sample.sample_id)}
                      className="mt-1"
                    />
                    <span>
                      <span className="font-medium">{sample.title}</span>
                      {sample.already_imported && (
                        <span className="ml-2 text-xs text-verdict-teal">In corpus</span>
                      )}
                      <span className="mt-1 block text-xs text-slate-gray">{sample.source}</span>
                    </span>
                  </label>
                ))}
              </div>
            </div>
          </details>
        </div>
      )}

      {status && (
        <p className="mt-3 text-sm text-verdict-teal" role="status">
          {status}
        </p>
      )}
    </div>
  );
}
