
import json
from pathlib import Path

from scripts.cost_tag_check import check_plan


def test_cost_tag_check_with_fixture(capsys):
    plan_path = Path("fixtures/plan.json")

    result = check_plan(str(plan_path))

    output = capsys.readouterr().out

    # Missing landlord_account_id resources must be reported.
    assert result == 1
    assert "aws_s3_bucket.listing_media" in output
    assert "aws_lambda_function.mls_feed_sync" in output

    # Resources with the required tag must not be reported.
    assert "aws_s3_bucket.landlord_media[0]" not in output
    assert "aws_lambda_function.screening_report_export" not in output

    # No-op and delete resources must be ignored.
    assert "aws_s3_bucket.archive_media" not in output
    assert "aws_s3_bucket.decommissioned_media" not in output


def test_cost_tag_check_idempotency(capsys):
    plan_path = Path("fixtures/plan.json")

    first_result = check_plan(str(plan_path))
    first_output = capsys.readouterr().out

    second_result = check_plan(str(plan_path))
    second_output = capsys.readouterr().out

    # Both executions must return the same result.
    assert first_result == second_result == 1

    # Both executions must produce identical output.
    assert first_output == second_output

    # Each missing resource must appear exactly once per run.
    assert first_output.count("aws_s3_bucket.listing_media") == 1
    assert first_output.count("aws_lambda_function.mls_feed_sync") == 1


def test_valid_plan_returns_zero(tmp_path, capsys):
    plan = {
        "resource_changes": [
            {
                "address": "aws_s3_bucket.valid",
                "change": {
                    "actions": ["create"],
                    "after": {
                        "tags": {
                            "landlord_account_id": "la-001"
                        }
                    }
                }
            }
        ]
    }

    plan_file = tmp_path / "valid_plan.json"
    plan_file.write_text(json.dumps(plan), encoding="utf-8")

    result = check_plan(str(plan_file))

    assert result == 0
    assert capsys.readouterr().out == ""
