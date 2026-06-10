export type Verdict =
  | "Supported"
  | "Partially Supported"
  | "Unsupported"
  | "Contradicted"
  | "Not Enough Evidence";

export interface Document {
  document_id: string;
  filename: string;
  file_type: string;
  chunk_count: number;
  status: string;
  error_message?: string | null;
  created_at: string;
  updated_at: string;
}

export interface SampleDocument {
  sample_id: string;
  title: string;
  category: string;
  source: string;
  url: string;
  description: string;
  good_for: string;
  filename: string;
  already_imported: boolean;
}

export interface SampleDocumentImportResult {
  sample_id: string;
  document_id?: string | null;
  filename?: string | null;
  status: string;
  chunk_count: number;
  message?: string | null;
}

export interface RetrievedSource {
  chunk_id: string;
  document_id: string;
  filename: string;
  page_number?: number | null;
  section_title?: string | null;
  text: string;
  similarity_score: number;
}

export interface Citation {
  document_name: string;
  page_number?: number | null;
  section_title?: string | null;
  chunk_id?: string | null;
}

export interface WitnessAnswer {
  answer_text: string;
  citations: Citation[];
  uncertainty_notes?: string | null;
}

export interface Claim {
  claim_id: string;
  claim_text: string;
  claim_type: string;
  cited_sources: string[];
  extracted_from_sentence: string;
}

export interface ProsecutorObjection {
  objection_id: string;
  claim_id: string;
  objection_type: string;
  explanation: string;
  missing_evidence?: string | null;
  contradicted_by_sources: string[];
}

export interface JudgeVerdict {
  claim_id: string;
  verdict: Verdict;
  confidence: number;
  explanation: string;
  supporting_sources: string[];
  recommended_revision?: string | null;
}

export interface TribunalResult {
  tribunal_result_id: string;
  question: string;
  final_answer: string;
  overall_verdict: Verdict | string;
  reliability_score: number | string;
  retrieved_sources: RetrievedSource[];
  witness_answer: WitnessAnswer;
  claims: Claim[];
  prosecutor_objections: ProsecutorObjection[];
  judge_verdict: JudgeVerdict[];
  created_at: string;
}

export interface EvaluationCaseResult {
  case_id: string;
  question: string;
  retrieval_hit: boolean;
  citation_accuracy: number;
  unsupported_claim_count: number;
  contradicted_claim_count: number;
  reliability_score: number | string;
  expected_verdict_behavior: string;
  passed: boolean;
}

export interface EvaluationRun {
  run_id: string;
  started_at: string;
  completed_at: string;
  aggregate_metrics: Record<string, unknown>;
  case_results: EvaluationCaseResult[];
}
