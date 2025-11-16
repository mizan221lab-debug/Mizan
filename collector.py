"""Simple data collection CLI program.

This script allows the user to collect simple personal data entries and
persist them to a JSON file. The code is intentionally small and easy to
modify for educational purposes.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import List

DEFAULT_STORAGE = Path("collected_data.json")


@dataclass
class Record:
    """Represents a single data entry collected from the user."""

    name: str
    age: int
    email: str
    phone: str
    notes: str
    timestamp: str


class DataCollector:
    """Handles reading and writing data records from disk."""

    def __init__(self, storage_path: Path | str = DEFAULT_STORAGE) -> None:
        self.storage_path = Path(storage_path)
        self.records: List[Record] = self._load()

    def _load(self) -> List[Record]:
        if not self.storage_path.exists():
            return []
        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
        return [Record(**item) for item in data]

    def add_record(self, *, name: str, age: int, email: str, phone: str, notes: str) -> Record:
        record = Record(
            name=name,
            age=age,
            email=email,
            phone=phone,
            notes=notes,
            timestamp=datetime.now().isoformat(timespec="seconds"),
        )
        self.records.append(record)
        self._save()
        return record

    def _save(self) -> None:
        self.storage_path.write_text(
            json.dumps([asdict(record) for record in self.records], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def _prompt(prompt: str, *, cast=str, allow_empty: bool = False):
    while True:
        value = input(prompt).strip()
        if not value and not allow_empty:
            print("กรุณากรอกข้อมูล (input required).\n")
            continue
        if not value and allow_empty:
            return cast(value)
        try:
            return cast(value)
        except ValueError:
            print("รูปแบบข้อมูลไม่ถูกต้อง ลองใหม่อีกครั้ง\n")


def run_cli(storage_path: Path | str = DEFAULT_STORAGE) -> None:
    collector = DataCollector(storage_path)
    print("ระบบเก็บข้อมูลผู้ติดต่ออย่างง่าย\n")
    while True:
        name = _prompt("ชื่อ: ")
        age = _prompt("อายุ: ", cast=int)
        email = _prompt("อีเมล: ")
        phone = _prompt("เบอร์โทรศัพท์: ")
        notes = _prompt("หมายเหตุ (กด Enter ข้ามได้): ", allow_empty=True)

        record = collector.add_record(name=name, age=age, email=email, phone=phone, notes=notes)
        print("\nบันทึกข้อมูลเรียบร้อยแล้ว: ")
        print(record)
        print(f"ข้อมูลทั้งหมดถูกเก็บไว้ที่ {collector.storage_path.resolve()}\n")

        should_continue = input("ต้องการกรอกข้อมูลเพิ่มเติมหรือไม่? (y/n): ").strip().lower()
        if should_continue != "y":
            print("\nจบการทำงาน ขอบคุณ!\n")
            break


if __name__ == "__main__":
    run_cli()
