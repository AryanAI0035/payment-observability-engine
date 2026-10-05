import asyncio
import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock


def load_backend(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    spec = importlib.util.spec_from_file_location("payment_backend", Path(__file__).parents[1] / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def transaction(module):
    return module.Transaction(id="test-failure", amount=10, currency="USD", merchant="Test", status="FAILED", timestamp="2026-10-06")


def test_analysis_is_async_and_has_no_invented_confidence(monkeypatch):
    module = load_backend(monkeypatch)
    generate = AsyncMock(return_value=SimpleNamespace(text="Reason: Timeout\nRecommended Action: Check gateway"))
    module.client = SimpleNamespace(aio=SimpleNamespace(models=SimpleNamespace(generate_content=generate)))
    asyncio.run(module.analyze_failed_transaction(transaction(module)))
    generate.assert_awaited_once()
    result = module.ai_analyses["test-failure"]
    assert result.reason == "Timeout"
    assert result.recommended_action == "Check gateway"
    assert result.confidence is None
    prompt = generate.call_args.kwargs["contents"]
    assert "Synthetic failure log:" in prompt
    assert "RAG retrieved" not in prompt


def test_missing_api_key_disables_analysis_without_breaking_transactions(monkeypatch):
    module = load_backend(monkeypatch)
    assert module.client is None
    tx = transaction(module)
    module.transactions_db.append(tx)
    asyncio.run(module.analyze_failed_transaction(tx))
    assert asyncio.run(module.get_transactions()) == [tx]
    assert tx.id not in module.ai_analyses
