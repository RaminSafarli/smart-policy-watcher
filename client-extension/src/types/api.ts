export interface ChangeSummaryMeta {
  policyUrl?: string;
  checkedAt?: string;
  model?: string;
  version?: string;
}

export interface ChangeSummary {
  short: string;
  long: string;
  meta?: ChangeSummaryMeta;
}

export interface AnalyzeChangeResponse {
  is_meaningful: boolean;
  summary: ChangeSummary;
}
