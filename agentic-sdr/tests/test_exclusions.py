import pytest
from src.exclusions.checker import check_exclusion


# --- Hard blocks ---

def test_amazon_blocked_as_customer():
    result = check_exclusion("Amazon")
    assert result["excluded"] is True
    assert result["reason"] == "customer"

def test_pepsi_blocked_as_strategic():
    result = check_exclusion("PepsiCo")
    assert result["excluded"] is True

def test_target_blocked_as_strategic_or_target():
    result = check_exclusion("Target")
    assert result["excluded"] is True

def test_geodis_blocked():
    result = check_exclusion("Geodis")
    assert result["excluded"] is True

def test_whirlpool_blocked():
    result = check_exclusion("Whirlpool")
    assert result["excluded"] is True


# --- Fuzzy matching ---

def test_fuzzy_geodis_na():
    result = check_exclusion("Geodis NA")
    assert result["excluded"] is True

def test_fuzzy_pg():
    result = check_exclusion("P&G")
    assert result["excluded"] is True

def test_fuzzy_amazon_logistics():
    result = check_exclusion("Amazon Logistics")
    assert result["excluded"] is True

def test_fuzzy_nestle_accent():
    result = check_exclusion("Nestle")
    assert result["excluded"] is True


# --- Net-new accounts (should pass) ---

def test_net_new_acme_logistics():
    result = check_exclusion("Acme Logistics Co")
    assert result["excluded"] is False
    assert result["reason"] is None

def test_net_new_summit_distribution():
    result = check_exclusion("Summit Distribution Partners")
    assert result["excluded"] is False

def test_net_new_apex_cold_storage():
    result = check_exclusion("Apex Cold Storage")
    assert result["excluded"] is False
