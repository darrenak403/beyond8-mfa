from __future__ import annotations

import argparse
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ANSWER_RE = re.compile(
    r"(?:^|\n)\s*(?:ANSWER|Dap\s*an|Đáp\s*án)\s*:\s*([^\n]+)",
    re.IGNORECASE,
)
QUESTION_SPLIT_RE = re.compile(r"^(\d{1,4})\.\s+", re.MULTILINE)
OPTION_START_RE = re.compile(r"^([A-Fa-f])[\.)]\s*(.*)$")
NUMBERED_STEM_RE = re.compile(r"^\d{1,4}\.\s+")
IGNORE_QUESTION_PREFIX_RE = re.compile(r"^question\s*:\s*", re.IGNORECASE)


@dataclass(frozen=True)
class Occurrence:
    file_path: str
    question_number: str
    answer_signature: str
    answer_display: str


@dataclass(frozen=True)
class IgnoreRules:
    ignored_questions: set[str]


def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def strip_diacritics(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    no_marks = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return no_marks.replace("đ", "d").replace("Đ", "D")


def normalize_for_compare(text: str) -> str:
    # Comparison key is punctuation-insensitive to reduce false conflicts caused by formatting.
    cleaned = strip_diacritics(normalize_ws(text)).lower()
    cleaned = re.sub(r"_", " ", cleaned)
    cleaned = re.sub(r"[^\w\s]", " ", cleaned)
    return normalize_ws(cleaned)


def load_ignore_rules(ignore_path: Path) -> tuple[IgnoreRules, int]:
    if not ignore_path.exists():
        return IgnoreRules(ignored_questions=set()), 0

    ignored_questions: set[str] = set()
    ignored_entries = 0

    for raw_line in ignore_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        question_text = IGNORE_QUESTION_PREFIX_RE.sub("", line)
        normalized_question = normalize_for_compare(question_text)
        if not normalized_question:
            continue

        ignored_questions.add(normalized_question)
        ignored_entries += 1

    return IgnoreRules(ignored_questions=ignored_questions), ignored_entries


def should_ignore_question(normalized_stem: str, ignore_rules: IgnoreRules) -> bool:
    return normalized_stem in ignore_rules.ignored_questions


def parse_answer_keys(raw_answer: str) -> list[str]:
    return sorted(set(letter.upper() for letter in re.findall(r"[A-Fa-f]", raw_answer)))


def extract_stem(question_body: str, answer_start_index: int) -> str:
    body_before_answer = question_body[:answer_start_index]
    stem_lines: list[str] = []

    for raw_line in body_before_answer.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if OPTION_START_RE.match(line):
            break
        stem_lines.append(NUMBERED_STEM_RE.sub("", line))

    if not stem_lines:
        return ""

    return normalize_ws(" ".join(stem_lines))


def extract_option_map(question_body: str, answer_start_index: int) -> dict[str, str]:
    body_before_answer = question_body[:answer_start_index]
    option_map: dict[str, str] = {}

    current_label = ""
    current_lines: list[str] = []

    def flush_current_option() -> None:
        nonlocal current_label, current_lines
        if current_label:
            option_map[current_label] = normalize_ws(" ".join(current_lines))
        current_label = ""
        current_lines = []

    for raw_line in body_before_answer.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        option_match = OPTION_START_RE.match(line)
        if option_match:
            flush_current_option()
            current_label = option_match.group(1).upper()
            option_text = normalize_ws(option_match.group(2))
            if option_text:
                current_lines = [option_text]
            continue

        if current_label:
            current_lines.append(line)

    flush_current_option()
    return option_map


def resolve_answer_signature(raw_answer: str, option_map: dict[str, str]) -> tuple[str, str]:
    answer_keys = parse_answer_keys(raw_answer)
    if answer_keys and all(key in option_map for key in answer_keys):
        answer_texts = [normalize_ws(option_map[key]) for key in answer_keys]
        normalized_texts = sorted(
            set(normalize_for_compare(text) for text in answer_texts if text)
        )
        if normalized_texts:
            answer_display = " | ".join(
                f"{key}: {option_map[key]}" for key in answer_keys
            )
            return " || ".join(normalized_texts), answer_display

    fallback_answer = normalize_ws(raw_answer)
    if not fallback_answer:
        return "", ""

    return normalize_for_compare(fallback_answer), fallback_answer


def scan_file(path: Path, repo_root: Path) -> list[tuple[str, str, Occurrence]]:
    content = path.read_text(encoding="utf-8", errors="ignore").replace("\r\n", "\n")
    blocks = QUESTION_SPLIT_RE.split(content)
    results: list[tuple[str, str, Occurrence]] = []

    for idx in range(1, len(blocks), 2):
        question_number = blocks[idx]
        question_body = blocks[idx + 1].strip()
        if not question_body:
            continue

        answer_match = ANSWER_RE.search(question_body)
        if not answer_match:
            continue

        stem = extract_stem(question_body, answer_match.start())
        if not stem:
            continue

        option_map = extract_option_map(question_body, answer_match.start())
        answer_signature, answer_display = resolve_answer_signature(
            answer_match.group(1), option_map
        )
        if not answer_signature:
            continue

        normalized_stem = normalize_for_compare(stem)
        relative_file = path.relative_to(repo_root).as_posix()
        occurrence = Occurrence(
            file_path=relative_file,
            question_number=question_number,
            answer_signature=answer_signature,
            answer_display=answer_display,
        )
        results.append((normalized_stem, stem, occurrence))

    return results


def build_report(
    source_dir: Path,
    output_path: Path,
    total_files: int,
    total_questions: int,
    ignored_questions_count: int,
    ignored_occurrences: int,
    ignore_rules_count: int,
    ignore_file: Path,
    conflicts: list[tuple[str, str, dict[str, list[Occurrence]]]],
) -> None:
    now_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: list[str] = [
        "=== CONFLICTING ANSWERS REPORT ===",
        f"Generated at: {now_text}",
        f"Source folder: {source_dir.as_posix()}",
        f"Scanned files: {total_files}",
        f"Parsed questions: {total_questions}",
        f"Ignore list file: {ignore_file.as_posix()}",
        f"Ignored questions in list: {ignore_rules_count}",
        f"Skipped conflict questions by ignore list: {ignored_questions_count}",
        f"Skipped occurrences by ignore list: {ignored_occurrences}",
        f"Conflicting questions: {len(conflicts)}",
        "",
    ]

    if not conflicts:
        lines.append("No conflicts found.")
    else:
        for index, (_, display_stem, answer_map) in enumerate(conflicts, start=1):
            lines.append(f"CONFLICT #{index}")
            lines.append(f"Question: {display_stem}")
            lines.append("")

            for answer_key in sorted(answer_map.keys()):
                answer_display = answer_map[answer_key][0].answer_display
                lines.append(f"  Answer text: {answer_display}")
                for occ in answer_map[answer_key]:
                    lines.append(
                        f"    - {occ.file_path} (Question #{occ.question_number})"
                    )
                lines.append("")

            lines.append("-" * 80)
            lines.append("")

    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def find_conflicts(
    source_dir: Path,
    repo_root: Path,
    ignore_rules: IgnoreRules,
) -> tuple[int, int, int, int, list[tuple[str, str, dict[str, list[Occurrence]]]]]:
    question_answers: dict[str, dict[str, list[Occurrence]]] = defaultdict(lambda: defaultdict(list))
    display_stems: dict[str, str] = {}

    files = sorted(source_dir.rglob("*.md"))
    total_questions = 0
    ignored_occurrences = 0
    ignored_questions: set[str] = set()

    for file_path in files:
        parsed_rows = scan_file(file_path, repo_root)
        total_questions += len(parsed_rows)
        for normalized_stem, display_stem, occurrence in parsed_rows:
            if should_ignore_question(normalized_stem, ignore_rules):
                ignored_occurrences += 1
                ignored_questions.add(normalized_stem)
                continue
            display_stems.setdefault(normalized_stem, display_stem)
            question_answers[normalized_stem][occurrence.answer_signature].append(
                occurrence
            )

    conflicts: list[tuple[str, str, dict[str, list[Occurrence]]]] = []
    for normalized_stem, answer_map in question_answers.items():
        if len(answer_map) > 1:
            conflicts.append((normalized_stem, display_stems[normalized_stem], answer_map))

    conflicts.sort(key=lambda item: item[1].lower())
    return (
        len(files),
        total_questions,
        len(ignored_questions),
        ignored_occurrences,
        conflicts,
    )


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(
        description="Scan source markdown files and report questions with conflicting answers."
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=repo_root / "source",
        help="Folder to recursively scan for markdown files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / "conflict_questions.txt",
        help="Output report file path.",
    )
    parser.add_argument(
        "--ignore-list",
        type=Path,
        default=repo_root / "conflict_questions.ignore.txt",
        help=(
            "Path to ignore list file. Each non-comment line is full question text "
            "(or prefixed with 'Question:') to ignore globally across all files."
        ),
    )
    args = parser.parse_args()

    source_dir = args.source_dir.resolve()
    output_path = args.output.resolve()
    ignore_list_path = args.ignore_list.resolve()

    if not source_dir.exists() or not source_dir.is_dir():
        print(f"ERROR: source folder not found: {source_dir}")
        return 1

    ignore_rules, ignore_rules_count = load_ignore_rules(ignore_list_path)
    (
        total_files,
        total_questions,
        ignored_questions_count,
        ignored_occurrences,
        conflicts,
    ) = find_conflicts(
        source_dir,
        repo_root,
        ignore_rules,
    )
    build_report(
        source_dir,
        output_path,
        total_files,
        total_questions,
        ignored_questions_count,
        ignored_occurrences,
        ignore_rules_count,
        ignore_list_path,
        conflicts,
    )

    print("Done.")
    print(f"Scanned files: {total_files}")
    print(f"Parsed questions: {total_questions}")
    print(f"Ignored questions in list: {ignore_rules_count}")
    print(f"Skipped conflict questions: {ignored_questions_count}")
    print(f"Skipped occurrences: {ignored_occurrences}")
    print(f"Conflicting questions: {len(conflicts)}")
    print(f"Report: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
