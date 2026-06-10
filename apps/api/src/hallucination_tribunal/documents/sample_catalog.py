"""Curated AI governance sample documents for quick corpus onboarding."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SampleDocument:
    sample_id: str
    title: str
    category: str
    source: str
    url: str
    description: str
    good_for: str = ""

    @property
    def filename(self) -> str:
        return f"sample-{self.sample_id}.md"

    def render_markdown(self) -> str:
        lines = [
            f"# {self.title}",
            "",
            f"**Category:** {self.category}",
            f"**Source:** {self.source}",
            f"**Official URL:** {self.url}",
            "",
            "## Overview",
            "",
            self.description,
            "",
        ]
        if self.good_for:
            lines.extend(
                [
                    "## Governance Use Cases",
                    "",
                    self.good_for,
                    "",
                ]
            )
        lines.extend(
            [
                "## How to Use in Policy Review",
                "",
                "Use this reference when evaluating AI governance, acceptable use, risk management,",
                "privacy, security, procurement, and organizational accountability requirements.",
                "Cite the official URL above when grounding tribunal answers in external standards.",
                "",
            ]
        )
        return "\n".join(lines)


SAMPLE_DOCUMENTS: tuple[SampleDocument, ...] = (
    SampleDocument(
        sample_id="nist-ai-rmf",
        title="NIST AI Risk Management Framework",
        category="NIST & Federal Standards",
        source="NIST AI RMF 1.0, GenAI Profile, Playbook",
        url="https://www.nist.gov/itl/ai-risk-management-framework",
        description=(
            "The NIST AI Risk Management Framework (AI RMF 1.0) provides voluntary guidance "
            "for managing risks across the AI lifecycle. It organizes practices into Govern, "
            "Map, Measure, and Manage functions to help organizations design, deploy, and "
            "monitor trustworthy AI systems."
        ),
        good_for=(
            "Enterprise AI governance structure, risk taxonomy, lifecycle controls, "
            "accountability roles, and mapping organizational policies to federal guidance."
        ),
    ),
    SampleDocument(
        sample_id="nist-genai-profile",
        title="NIST Generative AI Profile",
        category="NIST & Federal Standards",
        source="NIST.AI.600-1 Generative AI Profile",
        url="https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf",
        description=(
            "Companion profile to the AI RMF focused on generative AI risks, including "
            "hallucination, data privacy, model security, misuse, and third-party dependency risks."
        ),
        good_for=(
            "Hallucination controls, GenAI acceptable-use language, privacy safeguards, "
            "security requirements, and governance reviews of LLM deployments."
        ),
    ),
    SampleDocument(
        sample_id="nist-ai-rmf-playbook",
        title="NIST AI RMF Playbook",
        category="NIST & Federal Standards",
        source="NIST AI RMF Playbook",
        url="https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook",
        description=(
            "Practical actions and suggested activities mapped to Govern, Map, Measure, and "
            "Manage for teams implementing AI risk management."
        ),
        good_for=(
            "Operationalizing governance programs, control checklists, and translating "
            "high-level AI policy into actionable procedures."
        ),
    ),
    SampleDocument(
        sample_id="nist-airc",
        title="NIST AI Resource Center",
        category="NIST & Federal Standards",
        source="NIST AI Resource Center (AIRC)",
        url="https://airc.nist.gov/",
        description=(
            "Central hub for NIST AI RMF materials, profiles, playbooks, and related "
            "trustworthy AI resources."
        ),
        good_for="Discovering authoritative NIST AI governance artifacts and cross-references.",
    ),
    SampleDocument(
        sample_id="govai-coalition-templates",
        title="GovAI Coalition Templates (San José)",
        category="GovAI Coalition & Government Templates",
        source="City of San José GovAI Coalition",
        url=(
            "https://www.sanjoseca.gov/your-government/departments-offices/"
            "information-technology/artificial-intelligence-inventory/"
            "govai-coalition/templates-resources"
        ),
        description=(
            "Public-sector AI policy templates, governance documents, fact sheets, and "
            "procurement resources from the GovAI Coalition."
        ),
        good_for=(
            "Municipal and public-sector AI inventories, policy templates, and "
            "government procurement language."
        ),
    ),
    SampleDocument(
        sample_id="digital-government-hub-govai",
        title="Digital Government Hub: GovAI Templates",
        category="GovAI Coalition & Government Templates",
        source="Digital Government Hub",
        url="https://digitalgovernmenthub.org/library/govai-coalition-templates-and-resources/",
        description=(
            "Curated browsing experience for GovAI Coalition templates and example "
            "government AI policies."
        ),
        good_for="Finding government AI policy examples and implementation resources.",
    ),
    SampleDocument(
        sample_id="san-jose-ai-policy-template",
        title="San José AI Policy Template",
        category="GovAI Coalition & Government Templates",
        source="City of San José / Digital Government Hub",
        url="https://digitalgovernmenthub.org/examples/san-jose-ai-policy-template/",
        description=(
            "Customizable municipal AI policy template suitable for public agencies "
            "establishing acceptable use and oversight."
        ),
        good_for="Drafting agency-level AI acceptable-use and oversight policies.",
    ),
    SampleDocument(
        sample_id="nten-gai-policy-template",
        title="NTEN Generative AI Use Policy Template",
        category="Organizational Policy Templates",
        source="NTEN",
        url="https://word.nten.org/wp-content/uploads/2024/07/GAI-Policy-Template.pdf",
        description=(
            "Template policy for organizational generative AI use, covering workforce "
            "expectations and guardrails."
        ),
        good_for="Nonprofit and organizational GenAI acceptable-use policy drafting.",
    ),
    SampleDocument(
        sample_id="data-org-gai-policy-template",
        title="Data.org Generative AI Policy Template",
        category="Organizational Policy Templates",
        source="Data.org",
        url="https://data.org/wp-content/uploads/2024/11/Generative-AI-Policy-Template.pdf",
        description=(
            "Generic generative AI policy template for employees, contractors, and affiliates."
        ),
        good_for="Baseline workforce GenAI rules, contractor obligations, and affiliate use.",
    ),
    SampleDocument(
        sample_id="fisher-phillips-gai-policy",
        title="Fisher Phillips Acceptable Use of Generative AI Tools",
        category="Organizational Policy Templates",
        source="Fisher Phillips",
        url="https://www.fisherphillips.com/a/web/gjKyaHVbk96CZxaQe1Gv6E/ai-policy.pdf",
        description=(
            "Sample employee acceptable-use policy for generative AI tools in workplace settings."
        ),
        good_for="HR-facing acceptable-use rules, employee training, and legal review baselines.",
    ),
    SampleDocument(
        sample_id="harvard-genai-guidelines",
        title="Harvard Generative AI Guidelines",
        category="Higher Education Policies",
        source="Harvard University IT",
        url="https://www.huit.harvard.edu/ai/guidelines",
        description=(
            "Institutional guidance on responsible generative AI use in teaching, research, "
            "and administration."
        ),
        good_for="Academic integrity, research use, and institutional AI guidance comparisons.",
    ),
    SampleDocument(
        sample_id="una-ai-use-policy",
        title="University of North Alabama AI Use Policy",
        category="Higher Education Policies",
        source="University of North Alabama",
        url="https://www.una.edu/academics/docs/ai-use-policy.pdf",
        description="Formal university AI use policy for students, faculty, and staff.",
        good_for="Campus-wide acceptable-use and academic integrity policy patterns.",
    ),
    SampleDocument(
        sample_id="usc-genai-policy",
        title="USC Generative AI General Policy",
        category="Higher Education Policies",
        source="University of Southern California",
        url="https://policy.usc.edu/generative-ai-general-policy/",
        description="University-wide generative AI policy covering permitted and restricted uses.",
        good_for="Higher-ed governance comparisons and institutional accountability language.",
    ),
    SampleDocument(
        sample_id="quinnipiac-ai-policy",
        title="Quinnipiac Artificial Intelligence Policy",
        category="Higher Education Policies",
        source="Quinnipiac University",
        url=(
            "https://catalog.qu.edu/university-policies/artificial-intelligence-policy/"
            "artificial-intelligence-policy.pdf"
        ),
        description="Institutional artificial intelligence policy published in the university catalog.",
        good_for="Formal policy structure, definitions, and enforcement language in higher ed.",
    ),
    SampleDocument(
        sample_id="andrews-ai-policy",
        title="Andrews University Institutional AI Policy",
        category="Higher Education Policies",
        source="Andrews University",
        url="https://www.andrews.edu/services/its/ai/au-institutional-ai-policy.pdf",
        description="Institutional AI policy covering workforce and academic use expectations.",
        good_for="Institutional AI governance and IT policy alignment.",
    ),
    SampleDocument(
        sample_id="australia-public-genai-guidance",
        title="Australian Government Staff Guidance for Public GenAI",
        category="Public Sector Guidance",
        source="Australian Government Digital Policy",
        url="https://www.digital.gov.au/policy/ai/staff-guidance-public-generative-ai",
        description=(
            "Practical public-sector guidance for staff using generative AI tools responsibly."
        ),
        good_for="Public-sector workforce guidance, risk-aware usage, and government guardrails.",
    ),
    SampleDocument(
        sample_id="mrsc-ai-policies",
        title="MRSC AI Policies and Resources for Local Government",
        category="Public Sector Guidance",
        source="Municipal Research and Services Center (MRSC)",
        url="https://mrsc.org/explore-topics/technology/it/artificial-intelligence",
        description=(
            "Collection of AI policies and resources tailored to local government agencies."
        ),
        good_for="Local government policy examples, inventories, and implementation references.",
    ),
)

SAMPLE_BY_ID: dict[str, SampleDocument] = {doc.sample_id: doc for doc in SAMPLE_DOCUMENTS}


def list_sample_documents() -> list[SampleDocument]:
    return list(SAMPLE_DOCUMENTS)


def get_sample_document(sample_id: str) -> SampleDocument | None:
    return SAMPLE_BY_ID.get(sample_id)
