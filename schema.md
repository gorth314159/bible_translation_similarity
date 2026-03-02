# bible.eng.db Schema

## Tables

### _prisma_migrations

| Column | Type |
|--------|------|
| id | TEXT |
| checksum | TEXT |
| finished_at | NUM |
| migration_name | TEXT |
| logs | TEXT |
| rolled_back_at | NUM |
| started_at | NUM |
| applied_steps_count | INT |

### Translation

| Column | Type |
|--------|------|
| id | TEXT |
| name | TEXT |
| website | TEXT |
| licenseUrl | TEXT |
| shortName | TEXT |
| englishName | TEXT |
| language | TEXT |
| textDirection | TEXT |
| sha256 | TEXT |
| licenseNotes | TEXT |

### Book

| Column | Type |
|--------|------|
| id | TEXT |
| translationId | TEXT |
| name | TEXT |
| commonName | TEXT |
| title | TEXT |
| order | INT |
| numberOfChapters | INT |
| sha256 | TEXT |
| isApocryphal | NUM |
| id:1 | TEXT |
| name:1 | TEXT |
| website | TEXT |
| licenseUrl | TEXT |
| shortName | TEXT |
| englishName | TEXT |
| language | TEXT |
| textDirection | TEXT |
| sha256:1 | TEXT |
| licenseNotes | TEXT |

### Chapter

| Column | Type |
|--------|------|
| number | INT |
| bookId | TEXT |
| translationId | TEXT |
| json | TEXT |
| sha256 | TEXT |
| id | TEXT |
| name | TEXT |
| website | TEXT |
| licenseUrl | TEXT |
| shortName | TEXT |
| englishName | TEXT |
| language | TEXT |
| textDirection | TEXT |
| sha256:1 | TEXT |
| licenseNotes | TEXT |

### ChapterVerse

| Column | Type |
|--------|------|
| number | INT |
| chapterNumber | INT |
| bookId | TEXT |
| translationId | TEXT |
| text | TEXT |
| contentJson | TEXT |
| sha256 | TEXT |
| id | TEXT |
| name | TEXT |
| website | TEXT |
| licenseUrl | TEXT |
| shortName | TEXT |
| englishName | TEXT |
| language | TEXT |
| textDirection | TEXT |
| sha256:1 | TEXT |
| licenseNotes | TEXT |

### ChapterFootnote

| Column | Type |
|--------|------|
| id | INT |
| chapterNumber | INT |
| bookId | TEXT |
| translationId | TEXT |
| text | TEXT |
| verseNumber | INT |
| sha256 | TEXT |
| id:1 | TEXT |
| name | TEXT |
| website | TEXT |
| licenseUrl | TEXT |
| shortName | TEXT |
| englishName | TEXT |
| language | TEXT |
| textDirection | TEXT |
| sha256:1 | TEXT |
| licenseNotes | TEXT |

### ChapterAudioUrl

| Column | Type |
|--------|------|
| number | INT |
| bookId | TEXT |
| translationId | TEXT |
| reader | TEXT |
| url | TEXT |
| id | TEXT |
| name | TEXT |
| website | TEXT |
| licenseUrl | TEXT |
| shortName | TEXT |
| englishName | TEXT |
| language | TEXT |
| textDirection | TEXT |
| sha256 | TEXT |
| licenseNotes | TEXT |

### Commentary

| Column | Type |
|--------|------|
| id | TEXT |
| name | TEXT |
| website | TEXT |
| licenseUrl | TEXT |
| englishName | TEXT |
| language | TEXT |
| textDirection | TEXT |
| sha256 | TEXT |
| licenseNotes | TEXT |

### CommentaryBook

| Column | Type |
|--------|------|
| id | TEXT |
| commentaryId | TEXT |
| name | TEXT |
| commonName | TEXT |
| introduction | TEXT |
| order | INT |
| numberOfChapters | INT |
| sha256 | TEXT |
| introductionSummary | TEXT |
| id:1 | TEXT |
| name:1 | TEXT |
| website | TEXT |
| licenseUrl | TEXT |
| englishName | TEXT |
| language | TEXT |
| textDirection | TEXT |
| sha256:1 | TEXT |
| licenseNotes | TEXT |

### CommentaryChapter

| Column | Type |
|--------|------|
| number | INT |
| bookId | TEXT |
| commentaryId | TEXT |
| introduction | TEXT |
| json | TEXT |
| sha256 | TEXT |
| id | TEXT |
| name | TEXT |
| website | TEXT |
| licenseUrl | TEXT |
| englishName | TEXT |
| language | TEXT |
| textDirection | TEXT |
| sha256:1 | TEXT |
| licenseNotes | TEXT |

### CommentaryChapterVerse

| Column | Type |
|--------|------|
| number | INT |
| chapterNumber | INT |
| bookId | TEXT |
| commentaryId | TEXT |
| text | TEXT |
| contentJson | TEXT |
| sha256 | TEXT |
| id | TEXT |
| name | TEXT |
| website | TEXT |
| licenseUrl | TEXT |
| englishName | TEXT |
| language | TEXT |
| textDirection | TEXT |
| sha256:1 | TEXT |
| licenseNotes | TEXT |

### Dataset

| Column | Type |
|--------|------|
| id | TEXT |
| name | TEXT |
| website | TEXT |
| licenseUrl | TEXT |
| licenseNotes | TEXT |
| englishName | TEXT |
| language | TEXT |
| textDirection | TEXT |
| sha256 | TEXT |

### DatasetBook

| Column | Type |
|--------|------|
| id | TEXT |
| datasetId | TEXT |
| order | INT |
| numberOfChapters | INT |
| sha256 | TEXT |
| id:1 | TEXT |
| name | TEXT |
| website | TEXT |
| licenseUrl | TEXT |
| licenseNotes | TEXT |
| englishName | TEXT |
| language | TEXT |
| textDirection | TEXT |
| sha256:1 | TEXT |

### DatasetChapter

| Column | Type |
|--------|------|
| number | INT |
| bookId | TEXT |
| datasetId | TEXT |
| json | TEXT |
| sha256 | TEXT |
| id | TEXT |
| name | TEXT |
| website | TEXT |
| licenseUrl | TEXT |
| licenseNotes | TEXT |
| englishName | TEXT |
| language | TEXT |
| textDirection | TEXT |
| sha256:1 | TEXT |

### DatasetChapterVerse

| Column | Type |
|--------|------|
| number | INT |
| chapterNumber | INT |
| bookId | TEXT |
| datasetId | TEXT |
| contentJson | TEXT |
| sha256 | TEXT |
| id | TEXT |
| name | TEXT |
| website | TEXT |
| licenseUrl | TEXT |
| licenseNotes | TEXT |
| englishName | TEXT |
| language | TEXT |
| textDirection | TEXT |
| sha256:1 | TEXT |

### DatasetReference

| Column | Type |
|--------|------|
| id | INT |
| datasetId | TEXT |
| bookId | TEXT |
| chapterNumber | INT |
| verseNumber | INT |
| referenceBookId | TEXT |
| referenceChapter | INT |
| referenceVerse | INT |
| endVerseNumber | INT |
| score | INT |
| id:1 | TEXT |
| name | TEXT |
| website | TEXT |
| licenseUrl | TEXT |
| licenseNotes | TEXT |
| englishName | TEXT |
| language | TEXT |
| textDirection | TEXT |
| sha256 | TEXT |

---

**Note:** Many tables contain denormalized columns (suffixed with `:1`) that appear to be duplicated from parent tables (Translation, Commentary, or Dataset). These likely result from JOIN operations used when the database was originally exported.
