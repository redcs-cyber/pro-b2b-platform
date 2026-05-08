from api.llm_support import LLMOrchestrator, LLMTaskRequest


def test_llm_capabilities_include_local_and_enterprise_routes() -> None:
    capabilities = LLMOrchestrator().capabilities()
    provider_names = {provider["name"] for provider in capabilities["providers"]}

    assert "local-rules" in provider_names
    assert "ollama-local" in provider_names
    assert "openai-compatible" in provider_names
    assert "integration_debug" in capabilities["supported_tasks"]


def test_llm_task_plan_routes_sensitive_tasks_to_review_queue() -> None:
    plan = LLMOrchestrator().plan_task(
        LLMTaskRequest(
            task_type="compliance_gap",
            prompt="ISO 27001 eksiklerini çıkar",
            context={"customer_id": "CARI-99"},
        )
    )

    assert plan["provider_route"] == "offline-review-queue"
    assert plan["status"] == "queued"
    assert "compliance_matrix" in plan["tools"]
    assert any("KVKK" in guardrail for guardrail in plan["guardrails"])


def test_llm_task_plan_can_route_tool_enabled_quote_summary() -> None:
    plan = LLMOrchestrator().plan_task(
        LLMTaskRequest(
            task_type="quote_summary",
            prompt="Teklifi bayi dilinde açıkla",
            context={"requires_tools": True},
            require_human_approval=False,
        )
    )

    assert plan["provider_route"] == "openai-compatible"
    assert plan["status"] == "planned"
    assert plan["output_schema"]["properties"]["task_type"]["const"] == "quote_summary"
