# Design Notes

## B2 — Idempotency key

The exact idempotency key used by `cost_tag_check.py` is the Terraform resource address, obtained using:

```python
resource.get("address", "<unknown>")
```

For example:

- `aws_s3_bucket.listing_media`
- `aws_lambda_function.mls_feed_sync`

The resource address uniquely identifies a resource instance within the Terraform plan.

The checker uses a Python set with `set(missing_tags)` to eliminate duplicate resource addresses and `sorted()` to produce deterministic output.

The checker only evaluates resources whose planned actions include `create` or `update`. It checks the `after.tags` attribute and reports resources that are missing a non-empty `landlord_account_id` tag.

### Why is the check idempotent?

The cost-tag check is deterministic and does not maintain any external or persistent state.

Every execution:

1. Reads the same Terraform plan JSON file.
2. Evaluates the same resource changes.
3. Uses the Terraform resource address as the idempotency key.
4. Removes duplicate addresses using a set.
5. Sorts the results before printing.
6. Returns exit code `1` if missing tags exist, otherwise returns `0`.

Therefore, running the checker multiple times against an unchanged plan produces identical output and the same exit code.

The `test_cost_tag_check_idempotency` test verifies this by executing the checker twice and comparing both outputs and exit codes.

## Other design decisions with non-obvious alternatives

### 1. Using `for_each` instead of `count`

An alternative was to continue using `count` with a list of landlord accounts.

However, removing an account from the middle of the list can shift resource indexes and cause unnecessary infrastructure changes.

I chose `for_each` with `landlord_account_id` because it provides stable resource identities and avoids index-shifting problems.

### 2. Using landlord_account_id instead of tenant_id

An alternative was to use the existing `tenant_id` tag for cost allocation.

However, the README identifies the landlord account as the actual billing unit.

I therefore chose `landlord_account_id` as the required cost-allocation tag so that infrastructure costs can be attributed to the correct landlord account.

### 3. Checking only create and update actions

An alternative was to validate every resource change, including deletion and no-op actions.

I chose to check only resources being created or updated because those are the resources that need to satisfy the required cost-tagging policy in this check.

### 4. Using an in-memory set instead of persistent storage

An alternative was to store previously reported resources in a database or local file.

I chose an in-memory set because the Terraform plan already provides the resource information needed for each execution.

This keeps the checker simple, repeatable, and independent of external state.