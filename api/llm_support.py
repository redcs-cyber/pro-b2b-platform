from dataclasses import asdict, dataclass, field
from typing import Any, Literal
from uuid import uuid4

LLMTaskType = Literal["support_reply", "quote_summary", "compliance_gap", "product_copy", "sql_report", "integration_debug"]
ProviderMode = Literal["local_rule", "openai_compatible", "ollama", "azure_openai", "offline_queue"]


@dataclass(frozen=True)
class LLMProviderCapability:
    name: str
    mode: ProviderMode
    endpoint_env: str | None
    supports_streaming: bool
    supports_tools: bool
    pii_policy: str


@dataclass
class LLMTaskRequest:
    task_type: LLMTaskType
    prompt: str
    language: Literal["tr", "en"] = "tr"
    context: dict[str, Any] = field(default_factory=dict)
    require_human_approval: bool = True


@dataclass
class LLMTaskPlan:
    task_id: str
    provider_route: str
    system_prompt: str
    user_prompt: str
    guardrails: list[str]
    tools: list[str]
    output_schema: dict[str, Any]
    status: Literal["planned", "queued"] = "planned"


class LLMOrchestrator:
    """Offline-safe LLM orchestration layer.

    It prepares provider routes, prompts, tool hints, and output schemas without calling external
    services. Production workers can consume the returned plan and execute it with the chosen LLM.
    """

    def __init__(self) -> None:
        self.providers = [
            LLMProviderCapability("local-rules", "local_rule", None, False, False, "PII leaves no process"),
            LLMProviderCapability("ollama-local", "ollama", "OLLAMA_URL", True, False, "PII stays on local network"),
            LLMProviderCapability("openai-compatible", "openai_compatible", "OPENAI_BASE_URL", True, True, "Mask PII before request"),
            LLMProviderCapability("azure-openai", "azure_openai", "AZURE_OPENAI_ENDPOINT", True, True, "Enterprise tenant controls"),
            LLMProviderCapability("offline-review-queue", "offline_queue", None, False, False, "Human approval required"),
        ]

    def capabilities(self) -> dict[str, Any]:
        return {
            "providers": [asdict(provider) for provider in self.providers],
            "supported_tasks": ["support_reply", "quote_summary", "compliance_gap", "product_copy", "sql_report", "integration_debug"],
            "default_guardrails": self._guardrails(True),
        }

    def plan_task(self, request: LLMTaskRequest) -> dict[str, Any]:
        route = self._route_for(request)
        plan = LLMTaskPlan(
            task_id=f"LLM-{uuid4().hex[:8].upper()}",
            provider_route=route,
            system_prompt=self._system_prompt(request),
            user_prompt=self._user_prompt(request),
            guardrails=self._guardrails(request.require_human_approval),
            tools=self._tools_for(request.task_type),
            output_schema=self._output_schema(request.task_type),
            status="queued" if request.require_human_approval else "planned",
        )
        return asdict(plan)

    def _route_for(self, request: LLMTaskRequest) -> str:
        if request.task_type in {"compliance_gap", "sql_report"}:
            return "offline-review-queue"
        if request.context.get("local_only"):
            return "ollama-local"
        if request.context.get("requires_tools"):
            return "openai-compatible"
        return "local-rules"

    def _system_prompt(self, request: LLMTaskRequest) -> str:
        role = {
            "support_reply": "B2B bayi destek temsilcisi gibi net, güvenli ve çözüm odaklı yanıt ver.",
            "quote_summary": "Teklif kalemlerini bayi dilinde açıkla; iskonto, KDV ve onay durumunu sadeleştir.",
            "compliance_gap": "Uyumluluk denetçisi gibi eksik kanıtları ve riskleri açıkça listele.",
            "product_copy": "PIM ürün editörü gibi teknik ama satışa uygun ürün açıklaması üret.",
            "sql_report": "BI analisti gibi rapor amacını, metrikleri ve güvenli sorgu sınırlarını açıkla.",
            "integration_debug": "ERP/EDI entegrasyon uzmanı gibi mapper, payload ve kuyruk durumunu analiz et.",
        }[request.task_type]
        return f"Dil: {request.language}. Rol: {role}"

    def _user_prompt(self, request: LLMTaskRequest) -> str:
        return f"İstek: {request.prompt}\nBağlam: {request.context}"

    def _guardrails(self, require_human_approval: bool) -> list[str]:
        rules = [
            "KVKK/PII alanlarını maskele veya en az veri ilkesiyle kullan.",
            "Fiyat, stok, ödeme ve hukuki taahhütlerde kesin karar verme; kaynak sistem doğrulaması iste.",
            "ERP, finans, iade ve compliance aksiyonlarında audit kaydı öner.",
            "Kullanıcıdan gizli anahtar, kart verisi veya parola isteme.",
        ]
        if require_human_approval:
            rules.append("Müşteriye gönderimden önce insan onayı gerektir.")
        return rules

    def _tools_for(self, task_type: LLMTaskType) -> list[str]:
        return {
            "support_reply": ["customer_tree", "orders", "shipments", "returns"],
            "quote_summary": ["quote", "price_rules", "inventory"],
            "compliance_gap": ["compliance_matrix", "evidence_pack", "missing_actions"],
            "product_copy": ["pim", "search_index", "visual_assets"],
            "sql_report": ["analytics_snapshot", "audit_trail"],
            "integration_debug": ["erp_mapping", "edi_packets", "integration_jobs"],
        }[task_type]

    def _output_schema(self, task_type: LLMTaskType) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["summary", "actions", "risk_level"],
            "properties": {
                "summary": {"type": "string"},
                "actions": {"type": "array", "items": {"type": "string"}},
                "risk_level": {"enum": ["low", "medium", "high"]},
                "task_type": {"const": task_type},
            },
        }
