from api.compliance import ComplianceProgram


def test_compliance_readiness_requires_external_audit_before_go_live() -> None:
    program = ComplianceProgram()
    overview = program.readiness_overview()

    assert overview["go_live_ready"] is False
    assert overview["required_tracks"] == 6
    assert overview["external_audit_required_tracks"] >= 1
    assert "ISO/IEC 27001 ISMS kapsam" in overview["recommended_sequence"][2]


def test_certification_matrix_tracks_mandatory_evidence_and_gaps() -> None:
    program = ComplianceProgram()
    matrix = program.certification_matrix()

    assert any(item["code"] == "KVKK-GDPR" and item["mandatory_for_go_live"] for item in matrix)
    assert any("docs/security-kvkk-tr.md" in item["evidence_files"] for item in matrix)
    assert any(action["track"] == "PCI-DSS-4.0.1" for action in program.missing_go_live_actions())


def test_curriculum_map_links_learning_outcomes_to_repo_artifacts() -> None:
    program = ComplianceProgram()
    curriculum = program.curriculum_map()

    assert any(item["code"] == "SEC-201" and "api/compliance.py" in item["repo_artifacts"] for item in curriculum)
    assert any(item["level"] == "expert" for item in curriculum)
    assert "ISO-27001" in program.evidence_pack()
