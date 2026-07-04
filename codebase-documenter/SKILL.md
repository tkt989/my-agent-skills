---
name: codebase-documenter
description: 調査済みのコードベース情報を、AIと人間が読みやすいドキュメントとCSVインデックスとして整理する
---

# Codebase Documenter

## 目的

調査済みのコードベース情報を、構造化されたドキュメントとして整理する。

このスキルはコード調査そのものではなく、調査結果を `.codebase/` 形式で出力するために使う。

## 出力先

出力先が指定されていない場合は、以下へ直接出力する。

```text
.codebase/
```

`output_dir` が指定された場合は、そのディレクトリへ直接出力する。

## 出力構成

```text
<output_dir>/
├── README.md
├── architecture.md
├── flows.md
├── glossary.md
├── decisions.md
├── indexes/
│   ├── files.csv
│   ├── classes.csv
│   ├── symbols.csv
│   ├── modules.csv
│   ├── dependencies.csv
│   └── flows.csv
└── modules/
    ├── <module-name>.md
    └── ...
```

## テンプレート

出力ファイルは `templates/` 配下のテンプレートを基準に生成する。

- `templates/README.md`
- `templates/architecture.md`
- `templates/flow.md`
- `templates/glossary.md`
- `templates/decisions.md`
- `templates/modules.md`
- `templates/indexes.md`

テンプレートは固定文ではなく、調査済み情報に合わせて内容を埋める。不要な見出しは削除してよい。

## 生成するMarkdown

- `README.md`: 全体概要
- `architecture.md`: 構成・依存関係
- `flows.md`: 主要な処理フロー
- `glossary.md`: 用語集
- `decisions.md`: 設計判断
- `modules/*.md`: モジュール別説明

Markdownは読み物として簡潔にまとめる。

## 生成するCSV

- `indexes/files.csv`: ファイル索引
- `indexes/classes.csv`: クラス・型索引
- `indexes/symbols.csv`: シンボル索引
- `indexes/modules.csv`: モジュール索引
- `indexes/dependencies.csv`: 依存関係索引
- `indexes/flows.csv`: 処理フロー索引

CSVは網羅的な一覧として使う。

## 記述ルール

- コードを転載しない
- 実装詳細より責務を書く
- Markdownに一覧を詰め込みすぎない
- 網羅的な情報はCSVに出す
- 事実と推測を分ける
- 推測は「推測:」と書く
- 不明点は「未確認:」と書く
- CSVはUTF-8で出力し、必ずヘッダーを含める

## 完了条件

- Markdown一式が生成されている
- CSVインデックス一式が生成されている
- `.codebase/` だけを読めば、次のAIが調査を始められる
