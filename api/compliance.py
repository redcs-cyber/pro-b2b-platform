from dataclasses import asdict, dataclass, field
from typing import Any, Literal

ComplianceStatus = Literal["planned", "in_progress", "evidence_ready", "external_audit_required", "not_applicable"]
CurriculumLevel = Literal["foundation", "intermediate", "advanced", "expert"]


@dataclass(frozen=True)
class CertificationTrack:
    code: str
    name: str
    owner: str
    status: ComplianceStatus
    mandatory_for_go_live: bool
    evidence_files: list[str]
    missing_actions: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CurriculumModule:
    code: str
    title: str
    level: CurriculumLevel
    outcomes: list[str]
    repo_artifacts: list[str]
    assessment: str


@dataclass
class ComplianceProgram:
    """Maps ProB2B repository artifacts to enterprise certification and training readiness.

    This class does not grant a certificate. It makes the gap visible so an accredited auditor,
    legal advisor, or internal governance team can verify the final production scope.
    """

    certifications: list[CertificationTrack] = field(default_factory=list)
    curriculum: list[CurriculumModule] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.certifications:
            self.certifications = _default_certifications()
        if not self.curriculum:
            self.curriculum = _default_curriculum()

    def readiness_overview(self) -> dict[str, Any]:
        required = [item for item in self.certifications if item.mandatory_for_go_live]
        evidence_ready = [item for item in required if item.status == "evidence_ready"]
        external_audit = [item for item in required if item.status == "external_audit_required"]
        in_progress = [item for item in required if item.status in {"planned", "in_progress"}]
        return {
            "answer": "Kod deposu müfredat/sertifika yol haritasını içerir; üretim sertifikası için dış denetim ve gerçek ortam kanıtları hâlâ gereklidir.",
            "go_live_ready": not external_audit and not in_progress,
            "required_tracks": len(required),
            "evidence_ready_tracks": len(evidence_ready),
            "external_audit_required_tracks": len(external_audit),
            "in_progress_tracks": len(in_progress),
            "recommended_sequence": [
                "KVKK/GDPR veri envanteri ve aydınlatma/onay metinleri",
                "OWASP ASVS L2 güvenlik gereksinim doğrulaması",
                "ISO/IEC 27001 ISMS kapsam, risk ve SoA dosyaları",
                "PCI DSS kapsam dışı bırakma veya SAQ/AOC çalışması",
                "ERP/e-Fatura/e-Arşiv/e-İrsaliye entegrasyon kabul testleri",
                "ISO 22301 iş sürekliliği ve yedek dönüş testi",
            ],
        }

    def certification_matrix(self) -> list[dict[str, Any]]:
        return [asdict(item) for item in self.certifications]

    def curriculum_map(self) -> list[dict[str, Any]]:
        return [asdict(item) for item in self.curriculum]

    def missing_go_live_actions(self) -> list[dict[str, Any]]:
        actions = []
        for track in self.certifications:
            if not track.mandatory_for_go_live:
                continue
            for action in track.missing_actions:
                actions.append({"track": track.code, "action": action})
        return actions

    def evidence_pack(self) -> dict[str, list[str]]:
        return {track.code: track.evidence_files for track in self.certifications}


def _default_certifications() -> list[CertificationTrack]:
    return [
        CertificationTrack(
            code="KVKK-GDPR",
            name="Kişisel veri koruma, açık rıza, saklama/imha ve ilgili kişi talepleri",
            owner="DPO / hukuk / security",
            status="in_progress",
            mandatory_for_go_live=True,
            evidence_files=["docs/security-kvkk-tr.md", ".env.example", "migrations/001_b2b_core.sql"],
            missing_actions=[
                "Gerçek veri işleme envanteri çıkarılmalı",
                "Aydınlatma metni, açık rıza ve veri işleyen sözleşmeleri onaylanmalı",
                "Silme/yok etme/anonimleştirme prosedürü gerçek job ile bağlanmalı",
            ],
        ),
        CertificationTrack(
            code="ISO-27001",
            name="Bilgi Güvenliği Yönetim Sistemi / ISMS",
            owner="CISO / ISMS manager",
            status="external_audit_required",
            mandatory_for_go_live=True,
            evidence_files=["docs/security-kvkk-tr.md", "docs/runbook-tr.md", "observability/prometheus/prometheus.yml"],
            missing_actions=[
                "ISMS kapsam dokümanı, risk işleme planı ve Statement of Applicability hazırlanmalı",
                "İç denetim ve yönetim gözden geçirme kayıtları oluşturulmalı",
                "Akredite belgelendirme kuruluşu ile aşama 1/aşama 2 denetim tamamlanmalı",
            ],
        ),
        CertificationTrack(
            code="OWASP-ASVS-L2",
            name="Web/API uygulama güvenliği doğrulama seviyesi",
            owner="AppSec / engineering",
            status="in_progress",
            mandatory_for_go_live=True,
            evidence_files=["openapi/prob2b.openapi.yaml", "tests/test_enterprise_suite.py", "tests/test_b2b_ecosystem.py"],
            missing_actions=[
                "Kimlik doğrulama, session, access control ve API rate-limit testleri eklenmeli",
                "SAST/DAST ve dependency scanning CI kapıları eklenmeli",
                "Penetrasyon testi bulguları kapatılmalı",
            ],
        ),
        CertificationTrack(
            code="PCI-DSS-4.0.1",
            name="Kartlı ödeme güvenliği veya kart verisini kapsam dışında bırakma",
            owner="Finance / payment / security",
            status="planned",
            mandatory_for_go_live=True,
            evidence_files=[".env.example", "docs/enterprise-b2b-ecosystem-tr.md"],
            missing_actions=[
                "Kart verisi saklanmayacaksa tokenized hosted payment entegrasyonu netleştirilmeli",
                "SAQ tipi, network segmentasyonu ve ödeme sağlayıcı AOC dosyaları belirlenmeli",
            ],
        ),
        CertificationTrack(
            code="E-INVOICE-TR",
            name="Türkiye e-Fatura, e-Arşiv ve e-İrsaliye entegrasyon kabulü",
            owner="ERP / finance integration",
            status="in_progress",
            mandatory_for_go_live=True,
            evidence_files=[
                "integrations/erp/order_export.csv",
                "integrations/erp/erp_field_mapping.json",
                "integrations/erp/product_sync.xml",
            ],
            missing_actions=[
                "Gerçek ERP/GİB özel entegratör test ortamında uçtan uca senaryo koşulmalı",
                "Fatura iptal/iade, irsaliye ve cari mutabakat testleri eklenmeli",
            ],
        ),
        CertificationTrack(
            code="ISO-22301",
            name="İş sürekliliği, yedekleme ve felaket kurtarma",
            owner="SRE / operations",
            status="in_progress",
            mandatory_for_go_live=True,
            evidence_files=["deploy/onprem/scripts/backup_postgres.sh", "docs/runbook-tr.md", "deploy/saas/k8s/prob2b-api-hpa.yaml"],
            missing_actions=[
                "RPO/RTO hedefleri yönetim tarafından onaylanmalı",
                "Yedekten geri dönüş testi ve kesinti tatbikatı kanıtı üretilmeli",
            ],
        ),
        CertificationTrack(
            code="ISO-9001",
            name="Kalite yönetimi, değişiklik yönetimi ve müşteri memnuniyeti",
            owner="Product / quality",
            status="planned",
            mandatory_for_go_live=False,
            evidence_files=["docs/adr/0001-modular-monolith-first.md", "tests/test_enterprise_suite.py"],
            missing_actions=["Sürüm yönetimi, müşteri şikâyeti ve CAPA süreçleri tanımlanmalı"],
        ),
    ]


def _default_curriculum() -> list[CurriculumModule]:
    return [
        CurriculumModule(
            code="B2B-101",
            title="B2B iş modeli, bayi/cari hiyerarşisi ve sipariş yaşam döngüsü",
            level="foundation",
            outcomes=["Cari hiyerarşi okuma", "Tekliften siparişe akışı açıklama", "Stok rezervasyon mantığını anlama"],
            repo_artifacts=["api/b2b_ecosystem.py", "docs/enterprise-b2b-ecosystem-tr.md"],
            assessment="Örnek CARI-99 siparişini oluşturup ERP job çıktısını yorumlama",
        ),
        CurriculumModule(
            code="SEC-201",
            title="KVKK, OWASP ASVS ve güvenli API geliştirme",
            level="intermediate",
            outcomes=["Audit trail gereksinimi yazma", "API endpoint risklerini sınıflandırma", "KVKK saklama/imha sorumluluklarını açıklama"],
            repo_artifacts=["docs/security-kvkk-tr.md", "openapi/prob2b.openapi.yaml", "api/compliance.py"],
            assessment="Bir endpoint için ASVS kontrol listesi ve test senaryosu hazırlama",
        ),
        CurriculumModule(
            code="ERP-EDI-301",
            title="ERP, EDI ve e-belge entegrasyonları",
            level="advanced",
            outcomes=["ERP mapper tasarlama", "X12/EDIFACT akışını açıklama", "e-Fatura kabul testi planlama"],
            repo_artifacts=["integrations/erp/erp_field_mapping.json", "integrations/edi/x12_850_purchase_order.txt"],
            assessment="Sipariş export dosyasını ERP alanlarına eşleme",
        ),
        CurriculumModule(
            code="DEVOPS-301",
            title="SaaS/on-prem dağıtım, observability ve iş sürekliliği",
            level="advanced",
            outcomes=["Docker/Kubernetes dağıtımı okuma", "RPO/RTO tanımlama", "Prometheus/Grafana izlemesini planlama"],
            repo_artifacts=["deploy/", "observability/", "docs/runbook-tr.md"],
            assessment="Kesinti senaryosu için runbook ve rollback adımı yazma",
        ),
        CurriculumModule(
            code="ARCH-401",
            title="Modüler monolitten mikroservis/worker mimarisine evrim",
            level="expert",
            outcomes=["Bounded context çizme", "Worker ayrışma kararını verme", "SLA ve entegrasyon kuyruklarını tasarlama"],
            repo_artifacts=["docs/mega-repository-plan-tr.md", "docs/adr/0001-modular-monolith-first.md"],
            assessment="ERP worker, notification worker ve search indexer ayrışma planı hazırlama",
        ),
    ]
