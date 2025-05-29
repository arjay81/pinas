# Pinas XML Feed Merger

This repository merges multiple RSS feeds into `pinas_merged_feed.xml`, updated every 12 hours via GitHub Actions.

## Setup Instructions

1. **Update Feed URLs**
   - Edit `pinas_merge.py` to change the `FEED_URLS` list.

2. **GitHub Actions**
   - The `.github/workflows/pinas_merge.yml` runs every 12 hours (00:00, 12:00 UTC).
   - Trigger manually via the Actions tab.

3. **Access the Feed**
   - Find `pinas_merged_feed.xml` in the repository.
   - URL: `https://raw.githubusercontent.com/arjay81/pinas/main/pinas_merged_feed.xml`

## Notes
- Feeds must be RSS 2.0.
- Workflow uses `GITHUB_TOKEN` with read/write permissions.
- Check Actions tab for logs.

## License
MIT
