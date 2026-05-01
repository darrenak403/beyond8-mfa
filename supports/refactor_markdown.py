# py supports/refactor_markdown.py "source/pmg201/PMG201c - SU25 - FE.md"
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

ANSWER_RE = re.compile(r"^(?:ANSWER|Đáp án)\s*:\s*(.*)$", re.IGNORECASE)
OPTION_RE = re.compile(r"^([A-F])\.\s*(.*)$")
NUMBERED_STEM_RE = re.compile(r"^\d{1,3}\.\s+(.*)$")


@dataclass
class QuestionBlock:
	stem_lines: list[str] = field(default_factory=list)
	options: list[tuple[str, str]] = field(default_factory=list)
	answer: str = ""


def _normalize_ws(text: str) -> str:
	return re.sub(r"\s+", " ", text).strip()


try:
	from .diacritics import restore_vietnamese_diacritics  # type: ignore
except Exception:
	def restore_vietnamese_diacritics(text: str, source_root: Optional[Path] = None) -> str:  # type: ignore
		return text


def _parse_question_block(lines: list[str]) -> QuestionBlock | None:
	if not lines:
		return None

	block = QuestionBlock()
	answer_idx = -1
	for idx, line in enumerate(lines):
		if ANSWER_RE.match(line):
			answer_idx = idx
			break

	if answer_idx == -1:
		return None

	body = lines[:answer_idx]
	answer_match = ANSWER_RE.match(lines[answer_idx])
	if not answer_match:
		return None
	block.answer = _normalize_ws(answer_match.group(1))

	current_option_idx = -1
	for raw_line in body:
		line = raw_line.strip()
		if not line:
			continue

		option_match = OPTION_RE.match(line)
		if option_match:
			label = option_match.group(1)
			text = _normalize_ws(option_match.group(2))
			block.options.append((label, text))
			current_option_idx = len(block.options) - 1
			continue

		if current_option_idx >= 0:
			label, prev = block.options[current_option_idx]
			merged = _normalize_ws(f"{prev} {line}")
			block.options[current_option_idx] = (label, merged)
		else:
			numbered = NUMBERED_STEM_RE.match(line)
			clean = numbered.group(1) if numbered else line
			block.stem_lines.append(clean)

	if not block.stem_lines:
		return None

	block.stem_lines = [_normalize_ws(" ".join(block.stem_lines))]
	return block


def refactor_markdown_text(raw_text: str) -> str:
	"""Refactor raw PMG markdown text into normalized numbered question blocks."""
	# Best-effort: restore Vietnamese diacritics before parsing if possible.
	raw_text = restore_vietnamese_diacritics(raw_text)
	lines = [line.rstrip() for line in raw_text.replace("\r\n", "\n").split("\n")]

	chunks: list[list[str]] = []
	current: list[str] = []
	for line in lines:
		current.append(line)
		if ANSWER_RE.match(line.strip()):
			chunks.append(current)
			current = []

	# Guard against accidental truncation: trailing non-empty content must be parseable.
	if any(item.strip() for item in current):
		raise ValueError("Unparsed trailing content detected; aborting overwrite.")

	parsed_blocks: list[QuestionBlock] = []
	for chunk in chunks:
		block = _parse_question_block(chunk)
		if block is not None:
			parsed_blocks.append(block)

	if not parsed_blocks:
		raise ValueError("No valid question blocks found; aborting overwrite.")

	out_lines: list[str] = []
	for idx, block in enumerate(parsed_blocks, start=1):
		out_lines.append(f"{idx}. {block.stem_lines[0]}")
		out_lines.append("")
		for label, text in block.options:
			out_lines.append(f"{label}. {text}")
			out_lines.append("")
		out_lines.append(f"Đáp án: {block.answer}")
		out_lines.append("")

	return "\n".join(out_lines).rstrip() + "\n"


def refactor_markdown_file(input_path: str | Path, output_path: str | Path | None = None) -> Path:
	"""Read markdown quiz file and write a refactored version.

	If output_path is None, it will overwrite input_path.
	"""
	source = Path(input_path)
	target = Path(output_path) if output_path else source

	raw = source.read_text(encoding="utf-8")
	refactored = refactor_markdown_text(raw)
	target.write_text(refactored, encoding="utf-8")
	return target


def _build_cli() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		description="Refactor PMG markdown quiz file into normalized format."
	)
	parser.add_argument(
		"input_path",
		type=Path,
		help="Path to raw markdown file to refactor.",
	)
	return parser


if __name__ == "__main__":
	args = _build_cli().parse_args()
	result = refactor_markdown_file(args.input_path)
	print(f"Refactored: {result}")
