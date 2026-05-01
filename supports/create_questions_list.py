# py supports/create_questions_list.py
from __future__ import annotations

import re
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

# Ensure `supports/` is on sys.path so `import refactor_markdown` works when
# the script is imported as a module or executed from different working dirs.
_supports_dir = Path(__file__).resolve().parent
if str(_supports_dir) not in sys.path:
	sys.path.insert(0, str(_supports_dir))

from refactor_markdown import refactor_markdown_text
try:
	from .diacritics import restore_vietnamese_diacritics  # type: ignore
except Exception:
	try:
		from supports.diacritics import restore_vietnamese_diacritics  # type: ignore
	except Exception:
		def restore_vietnamese_diacritics(text: str, source_root=None) -> str:  # type: ignore
			return text

OPTION_LINE_RE = re.compile(r"^([A-Fa-f])[\.)]\s*(.*)$")
NUMBERED_STEM_RE = re.compile(r"^\d{1,3}\.\s+(.*)$")
ANSWER_MARKER_RE = re.compile(r"^(?:ANSWER|Đáp án)\s*:\s*.+$", re.IGNORECASE | re.MULTILINE)


def _normalize_ws(text: str) -> str:
	return re.sub(r"\s+", " ", text).strip()


def _parse_answer_keys(raw_answer: str) -> list[str]:
	keys = [part.upper() for part in re.findall(r"[A-Fa-f]", raw_answer)]
	seen: set[str] = set()
	unique: list[str] = []
	for key in keys:
		if key not in seen:
			seen.add(key)
			unique.append(key)
	return unique


def _file_has_questions(path: Path) -> bool:
	try:
		content = path.read_text(encoding="utf-8")
	except OSError:
		return True
	return bool(ANSWER_MARKER_RE.search(content))


class QuestionInputApp:
	def __init__(self, root: tk.Tk) -> None:
		self.root = root
		self.root.title("Create Questions List")
		self.root.geometry("1000x620")

		self.file_path_var = tk.StringVar(value="source/pmg201/questions.md")
		self.subject_var = tk.StringVar()
		self.source_file_var = tk.StringVar()
		self.status_var = tk.StringVar(value="Ready")
		self.timer_var = tk.StringVar(value="00:00")
		self.source_root = Path.cwd() / "source"
		self.source_files: list[str] = []
		self.files_by_subject: dict[str, list[str]] = {}
		self.file_display_to_rel: dict[str, str] = {}
		self.answer_choice_states: dict[str, bool] = {}
		self.answer_choice_buttons: dict[str, tk.Button] = {}
		self.elapsed_seconds = 0

		self.raw_block_text: tk.Text
		self.subject_combo: ttk.Combobox
		self.source_combo: ttk.Combobox
		self.answer_choices_frame: ttk.Frame
		self.save_button: tk.Button

		self._build_ui()
		self._refresh_source_files()
		self._tick_timer()

	def _build_ui(self) -> None:
		container = ttk.Frame(self.root, padding=12)
		container.pack(fill=tk.BOTH, expand=True)
		container.columnconfigure(0, weight=3)
		container.columnconfigure(1, weight=2)
		container.rowconfigure(1, weight=1)
		container.rowconfigure(2, weight=1)

		file_bar = ttk.Frame(container)
		file_bar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
		file_bar.columnconfigure(1, weight=1)
		file_bar.columnconfigure(5, weight=1)

		ttk.Label(file_bar, text="Markdown file:").grid(row=0, column=0, sticky="w", padx=(0, 8))
		ttk.Entry(file_bar, textvariable=self.file_path_var).grid(row=0, column=1, sticky="ew", padx=(0, 8))
		ttk.Button(file_bar, text="Browse", command=self._browse_file).grid(row=0, column=2)
		# Copy filename (without .md) to clipboard
		ttk.Button(
			file_bar,
			text="Copy tên file",
			command=self._copy_filename_to_clipboard,
		).grid(row=0, column=3, padx=(6, 6))
		ttk.Label(file_bar, text="Timer:").grid(row=0, column=4, sticky="e", padx=(10, 6))
		ttk.Label(file_bar, textvariable=self.timer_var).grid(row=0, column=5, sticky="w")

		ttk.Label(file_bar, text="Subject:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(8, 0))
		self.subject_combo = ttk.Combobox(
			file_bar,
			textvariable=self.subject_var,
			state="readonly",
		)
		self.subject_combo.grid(row=1, column=1, sticky="ew", pady=(8, 0), padx=(0, 8))
		self.subject_combo.bind("<<ComboboxSelected>>", self._on_subject_selected)

		ttk.Label(file_bar, text="File:").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=(8, 0))
		self.source_combo = ttk.Combobox(
			file_bar,
			textvariable=self.source_file_var,
			state="readonly",
		)
		self.source_combo.grid(row=2, column=1, columnspan=2, sticky="ew", pady=(8, 0), padx=(0, 8))
		self.source_combo.bind("<<ComboboxSelected>>", self._on_source_file_selected)
		ttk.Button(file_bar, text="Refresh", command=self._refresh_source_files).grid(row=2, column=3, pady=(8, 0))

		left = ttk.LabelFrame(container, text="Input câu hỏi", padding=10)
		left.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
		left.columnconfigure(0, weight=1)
		left.rowconfigure(1, weight=1)

		ttk.Label(left, text="Dán full block câu hỏi + các options (A/B/C...):").grid(
			row=0,
			column=0,
			sticky="nw",
			pady=(0, 4),
		)
		self.raw_block_text = tk.Text(left, height=16, wrap="word")
		self.raw_block_text.grid(row=1, column=0, sticky="nsew", pady=(0, 8))
		self.raw_block_text.bind("<KeyRelease>", self._on_raw_block_changed)

		right = ttk.LabelFrame(container, text="Nhập đáp án đúng", padding=10)
		right.grid(row=1, column=1, sticky="nsew")
		right.columnconfigure(0, weight=1)
		right.rowconfigure(1, weight=1)

		ttk.Label(right, text="Chọn đáp án đúng theo options vừa detect được").grid(
			row=0,
			column=0,
			sticky="w",
			pady=(0, 6),
		)

		self.answer_choices_frame = ttk.Frame(right)
		self.answer_choices_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
		self._set_answer_choices([])

		self.save_button = tk.Button(
			right,
			text="Lưu vào file md (Ctrl+Enter)",
			command=self._save_question,
			font=("Segoe UI", 12, "bold"),
			height=2,
		)
		self.save_button.grid(row=2, column=0, sticky="ew", pady=(0, 10))

		ttk.Label(
			right,
			text="Sau khi lưu: app tự format + append vào file đã chọn ở trên.",
			wraplength=280,
			justify="left",
		).grid(row=3, column=0, sticky="w")

		preview_frame = ttk.LabelFrame(container, text="Preview", padding=10)
		preview_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(8, 0))
		preview_frame.columnconfigure(0, weight=1)
		preview_frame.rowconfigure(0, weight=1)

		self.preview = tk.Text(preview_frame, wrap="word", state="disabled")
		self.preview.grid(row=0, column=0, sticky="nsew")

		status = ttk.Label(container, textvariable=self.status_var, anchor="w")
		status.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(8, 0))

		self.raw_block_text.focus_set()

	def _tick_timer(self) -> None:
		minutes = self.elapsed_seconds // 60
		seconds = self.elapsed_seconds % 60
		self.timer_var.set(f"{minutes:02d}:{seconds:02d}")
		self.elapsed_seconds += 1
		self.root.after(1000, self._tick_timer)

	def _set_answer_choices(self, labels: list[str]) -> None:
		previously_selected = {k for k, v in self.answer_choice_states.items() if v}
		for child in self.answer_choices_frame.winfo_children():
			child.destroy()

		self.answer_choice_states = {}
		self.answer_choice_buttons = {}
		if not labels:
			ttk.Label(
				self.answer_choices_frame,
				text="Chua detect duoc options. Hay dan cau hoi ben trai.",
			).grid(row=0, column=0, sticky="w")
			return

		for i in range(4):
			self.answer_choices_frame.columnconfigure(i, weight=1)

		for idx, label in enumerate(labels):
			selected = label in previously_selected
			self.answer_choice_states[label] = selected
			btn = tk.Button(
				self.answer_choices_frame,
				text=label,
				width=4,
				height=2,
				font=("Segoe UI", 14, "bold"),
				command=lambda value=label: self._toggle_answer_choice(value),
			)
			btn.grid(row=idx // 4, column=idx % 4, sticky="nsew", padx=6, pady=6)
			self.answer_choice_buttons[label] = btn
			self._paint_answer_choice(label)

	def _paint_answer_choice(self, label: str) -> None:
		btn = self.answer_choice_buttons.get(label)
		if not btn:
			return

		if self.answer_choice_states.get(label, False):
			btn.configure(
				text=f"✓ {label}",
				relief=tk.SUNKEN,
				bg="#1f6feb",
				fg="white",
				activebackground="#1f6feb",
			)
		else:
			btn.configure(
				text=label,
				relief=tk.RAISED,
				bg="#f2f2f2",
				fg="black",
				activebackground="#e6e6e6",
			)

	def _toggle_answer_choice(self, label: str) -> None:
		current = self.answer_choice_states.get(label, False)
		self.answer_choice_states[label] = not current
		self._paint_answer_choice(label)

	def _on_raw_block_changed(self, _event: tk.Event[tk.Misc]) -> None:
		# If user pressed Enter, attempt a best-effort diacritics restoration
		# to improve live preview and option detection.
		try:
			keysym = getattr(_event, "keysym", None)
			if keysym in ("Return", "KP_Enter"):
				raw = self.raw_block_text.get("1.0", "end-1c")
				restored = restore_vietnamese_diacritics(raw)
				if restored != raw:
					# Replace content and move cursor to end of insertion
					self.raw_block_text.delete("1.0", "end")
					self.raw_block_text.insert("1.0", restored)
					self.raw_block_text.mark_set("insert", "end-1c")
					self.raw_block_text.see("insert")
		except Exception:
			# Best-effort only; swallow errors to avoid interrupting typing
			pass
		self._refresh_answer_choices()

	def _refresh_answer_choices(self) -> None:
		raw_block = self.raw_block_text.get("1.0", "end").strip()
		if not raw_block:
			self._set_answer_choices([])
			return

		try:
			_, options = self._parse_raw_block(raw_block)
		except ValueError:
			self._set_answer_choices([])
			return

		labels = [label for label, _ in options]
		self._set_answer_choices(labels)

	def _browse_file(self) -> None:
		selected = filedialog.askopenfilename(
			title="Select markdown file",
			filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
		)
		if selected:
			self.file_path_var.set(selected)
			self._sync_source_selection_from_path()

	def _copy_filename_to_clipboard(self) -> None:
		"""Copy the selected file's base name (without .md) to the clipboard."""
		current_raw = self.file_path_var.get().strip()
		if not current_raw:
			messagebox.showerror("No file selected", "Please select a markdown file first.")
			return
		try:
			p = Path(current_raw)
			filename = p.name or str(p)
			stem = Path(filename).stem
			self.root.clipboard_clear()
			self.root.clipboard_append(stem)
			self.status_var.set(f"Copied filename: {stem}")
		except Exception as err:
			messagebox.showerror("Copy failed", str(err))
			self.status_var.set(f"Failed to copy: {err}")

	def _to_workspace_relative_posix(self, value: str) -> str:
		path = Path(value)
		if path.is_absolute():
			try:
				path = path.relative_to(Path.cwd())
			except ValueError:
				return path.as_posix()
		return path.as_posix()

	def _sync_source_selection_from_path(self) -> None:
		current_raw = self.file_path_var.get().strip()
		if not current_raw:
			self.subject_var.set("")
			self.source_file_var.set("")
			return

		current = self._to_workspace_relative_posix(current_raw)
		if current in self.source_files:
			parts = Path(current).parts
			subject = parts[1] if len(parts) >= 2 else ""
			if subject in self.files_by_subject:
				self.subject_var.set(subject)
				self._update_file_combo_for_subject(subject)
			else:
				self.subject_var.set("")
				self._update_file_combo_for_subject("")

			display = self._display_name_for_rel(current, subject)
			self.source_file_var.set(display)
			self.file_path_var.set(current)
		else:
			self.subject_var.set("")
			self._update_file_combo_for_subject("")
			self.source_file_var.set("")

	def _display_name_for_rel(self, rel: str, subject: str) -> str:
		parts = Path(rel).parts
		if len(parts) >= 3 and parts[0] == "source" and parts[1] == subject:
			return Path(*parts[2:]).as_posix()
		return Path(rel).name

	def _update_file_combo_for_subject(self, subject: str) -> None:
		files = self.files_by_subject.get(subject, [])
		display = [self._display_name_for_rel(item, subject) for item in files]
		self.file_display_to_rel = dict(zip(display, files))
		self.source_combo["values"] = display

	def _refresh_source_files(self) -> None:
		if not self.source_root.exists():
			self.source_files = []
			self.files_by_subject = {}
			self.subject_combo["values"] = []
			self.source_combo["values"] = []
			self.subject_var.set("")
			self.source_file_var.set("")
			return

		md_files = sorted(
			path.relative_to(Path.cwd()).as_posix()
			for path in self.source_root.rglob("*.md")
			if not _file_has_questions(path)
		)
		self.source_files = md_files

		grouped: dict[str, list[str]] = {}
		for rel in md_files:
			parts = Path(rel).parts
			subject = parts[1] if len(parts) >= 2 else ""
			grouped.setdefault(subject, []).append(rel)
		self.files_by_subject = grouped

		subjects = sorted(k for k in grouped.keys() if k)
		self.subject_combo["values"] = subjects

		if not subjects:
			self.subject_var.set("")
			self.source_file_var.set("")
			self.source_combo["values"] = []
			self.status_var.set("Khong con file trong source de nhap moi (tat ca da co cau hoi).")
			return

		self.status_var.set("Ready")

		if not self.file_path_var.get().strip() and md_files:
			default_subject = subjects[0] if subjects else ""
			self.subject_var.set(default_subject)
			self._update_file_combo_for_subject(default_subject)
			default_file = grouped[default_subject][0]
			self.source_file_var.set(self._display_name_for_rel(default_file, default_subject))
			self.file_path_var.set(default_file)
			return

		self._sync_source_selection_from_path()

	def _on_subject_selected(self, _event: tk.Event[tk.Misc]) -> None:
		subject = self.subject_var.get().strip()
		self._update_file_combo_for_subject(subject)
		files = self.files_by_subject.get(subject, [])
		if files:
			selected = files[0]
			self.source_file_var.set(self._display_name_for_rel(selected, subject))
			self.file_path_var.set(selected)

	def _on_source_file_selected(self, _event: tk.Event[tk.Misc]) -> None:
		selected_name = self.source_file_var.get().strip()
		if not selected_name:
			return

		rel = self.file_display_to_rel.get(selected_name)
		if rel:
			self.file_path_var.set(rel)

	def _on_submit(self, _event: tk.Event[tk.Misc]) -> str:
		self._save_question()
		return "break"

	def _collect_form(self) -> tuple[str, str]:
		raw_block = self.raw_block_text.get("1.0", "end").strip()
		selected = [label for label, checked in self.answer_choice_states.items() if checked]
		raw_answer = ", ".join(selected)
		return raw_block, raw_answer

	def _parse_raw_block(self, raw_block: str) -> tuple[str, list[tuple[str, str]]]:
		stem_lines: list[str] = []
		option_parts: dict[str, list[str]] = {}
		option_order: list[str] = []
		current_option: str | None = None

		for raw_line in raw_block.splitlines():
			line = raw_line.strip()
			if not line:
				continue

			match = OPTION_LINE_RE.match(line)
			if match:
				label = match.group(1).upper()
				text = _normalize_ws(match.group(2))
				if label not in option_parts:
					option_parts[label] = []
					option_order.append(label)
				option_parts[label].append(text)
				current_option = label
				continue

			if current_option is not None:
				option_parts[current_option].append(_normalize_ws(line))
			else:
				numbered = NUMBERED_STEM_RE.match(line)
				stem_lines.append(numbered.group(1) if numbered else line)

		stem = _normalize_ws(" ".join(stem_lines))
		if not stem:
			raise ValueError("Không nhận diện được nội dung câu hỏi.")

		if len(option_order) < 2:
			raise ValueError("Can it nhat 2 options (vi du A, B).")

		parsed_options: list[tuple[str, str]] = []
		for label in option_order:
			text = _normalize_ws(" ".join(option_parts.get(label, [])))
			if not text:
				raise ValueError(f"Noi dung option {label} dang rong.")
			parsed_options.append((label, text))

		return stem, parsed_options

	def _validate(self, raw_block: str, raw_answer: str) -> bool:
		if not self.file_path_var.get().strip():
			messagebox.showerror("Missing file", "Please provide a markdown file path.")
			return False

		if not raw_block:
			messagebox.showerror("Missing input", "Please paste full question block.")
			return False

		try:
			_, options = self._parse_raw_block(raw_block)
		except ValueError as err:
			messagebox.showerror("Parse failed", str(err))
			return False

		answer_keys = _parse_answer_keys(raw_answer)
		if not answer_keys:
			messagebox.showerror("Invalid answer", "Nhap dap an dung: B hoac A,B")
			return False

		option_labels = {label for label, _ in options}
		unknown = [key for key in answer_keys if key not in option_labels]
		if unknown:
			messagebox.showerror(
				"Invalid answer",
				f"Dap an {', '.join(unknown)} khong ton tai trong options hien tai.",
			)
			return False

		return True

	def _render_raw_block(self, question: str, options: list[tuple[str, str]], answer_keys: list[str]) -> str:
		lines = [question, ""]
		for label, text in options:
			lines.append(f"{label}. {text}")
			lines.append("")
		lines.append(f"Đáp án: {', '.join(answer_keys)}")
		lines.append("")
		return "\n".join(lines)

	def _save_question(self) -> None:
		raw_block, raw_answer = self._collect_form()
		if not self._validate(raw_block, raw_answer):
			return

		question, options = self._parse_raw_block(raw_block)
		answer_keys = _parse_answer_keys(raw_answer)

		target = Path(self.file_path_var.get().strip())
		if not target.is_absolute():
			target = Path.cwd() / target

		block = self._render_raw_block(question, options, answer_keys)

		try:
			target.parent.mkdir(parents=True, exist_ok=True)
			existing = target.read_text(encoding="utf-8") if target.exists() else ""
			candidate = f"{existing.rstrip()}\n\n{block}" if existing.strip() else block
			normalized = refactor_markdown_text(candidate)

			tmp = target.with_suffix(target.suffix + ".tmp")
			tmp.write_text(normalized, encoding="utf-8")
			tmp.replace(target)

			# Best-effort: ensure diacritics are applied to the final file as well.
			# Some environments may not run the live restoration; apply one more pass here.
			try:
				final_text = target.read_text(encoding="utf-8")
				restored_final = restore_vietnamese_diacritics(final_text)
				if restored_final != final_text:
					# overwrite with restored content (no separate backup here because
					# caller already received a .tmp replacement). This is conservative
					# and rare; we update preview to reflect final state.
					target.write_text(restored_final, encoding="utf-8")
					normalized = restored_final
			except Exception:
				# swallow errors - restoration is best-effort
				pass
		except (OSError, ValueError) as err:
			messagebox.showerror("Save failed", str(err))
			self.status_var.set(f"Failed: {err}")
			return

		self._update_preview(normalized)
		self._clear_inputs()
		self.status_var.set(f"Saved and refactored: {target}")
		self._refresh_source_files()

	def _update_preview(self, content: str) -> None:
		self.preview.configure(state="normal")
		self.preview.delete("1.0", "end")
		self.preview.insert("1.0", content)
		# Keep the newest appended question in view.
		self.preview.see("end-1c")
		self.preview.yview_moveto(1.0)
		self.preview.configure(state="disabled")

	def _clear_inputs(self) -> None:
		self.raw_block_text.delete("1.0", "end")
		for label in list(self.answer_choice_states.keys()):
			self.answer_choice_states[label] = False
		self._set_answer_choices([])
		self.raw_block_text.focus_set()


def main() -> None:
	root = tk.Tk()
	app = QuestionInputApp(root)
	root.bind("<Control-Return>", app._on_submit)
	root.mainloop()


if __name__ == "__main__":
	main()
