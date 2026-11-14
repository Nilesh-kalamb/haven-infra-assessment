# B0 — The `count` trap
#
# Each landlord account gets a dedicated S3 bucket for their media.
# Buckets are addressed by POSITION in var.landlord_accounts.
#
# Removing an account from the middle of the list can cause Terraform
# to destroy and recreate buckets because count uses positional indexes.

resource "aws_s3_bucket" "landlord_media" {
  count  = length(var.landlord_accounts)
  bucket = "haven-landlord-media-${var.landlord_accounts[count.index]}"
}