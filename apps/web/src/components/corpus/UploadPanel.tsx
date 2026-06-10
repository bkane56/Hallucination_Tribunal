"use client";

import { useRef, useState } from "react";
import { api } from "@/lib/api/client";

interface UploadPanelProps {
  onUploaded?: () => void;
}

export function UploadPanel({ onUploaded }: UploadPanelProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleUpload(file: File) {
    setLoading(true);
    setError(null);
    setStatus(null);
    try {
      const result = await api.uploadDocument(file);
      setStatus(`Indexed ${result.filename} (${result.chunk_count} chunks)`);
      onUploaded?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-lg border border-paper-line bg-ivory p-6 shadow-sm">
      <h2 className="mb-2 text-lg font-semibold text-charcoal">Upload Documents</h2>
      <p className="mb-4 text-sm text-slate-gray">
        Supported formats: PDF, Markdown, TXT, DOCX, HTML
      </p>
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.md,.txt,.docx,.html,.htm"
        className="hidden"
        aria-label="Choose document file"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) handleUpload(file);
        }}
      />
      <button
        type="button"
        disabled={loading}
        onClick={() => inputRef.current?.click()}
        className="rounded-md bg-gavel-gold px-4 py-2 text-sm font-medium text-deep-ink hover:opacity-90 disabled:opacity-50"
      >
        {loading ? "Uploading..." : "Choose File"}
      </button>
      {status && (
        <p className="mt-3 text-sm text-verdict-teal" role="status">
          {status}
        </p>
      )}
      {error && (
        <p className="mt-3 text-sm text-overruled-red" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
