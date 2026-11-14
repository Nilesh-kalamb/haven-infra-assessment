resource "aws_s3_bucket" "listing_media" {
  bucket = "haven-listing-media"
}

resource "aws_s3_bucket_lifecycle_configuration" "listing_media_archive" {
  bucket = aws_s3_bucket.listing_media.id

  rule {
    id     = "archive-sold-listing-photos"
    status = "Enabled"

    filter {}

    transition {
      days          = 60
      storage_class = "GLACIER"
    }
  }
}