---
name: codebase-reader
description: .codebase のドキュメントとCSVインデックスを使って、コードベースを効率よく読み込む
---

# Codebase Reader

## 目的

`.codebase/` に生成済みのドキュメントとCSVインデックスを使い、必要な実コードを効率よく特定して読み込む。

このスキルはコードベース全体を最初から読むためではなく、`.codebase/` を地図として使い、作業対象に関係するコードへ素早く到達するために使う。

## 入力

- ユーザーの作業依頼
- `.codebase/` ディレクトリ
- 実コード

## 読む順番

原則として以下の順番で読む。

1. `.codebase/README.md`
2. `.codebase/architecture.md`
3. `.codebase/flows.md`
4. 作業内容に関係する `.codebase/modules/*.md`
5. `.codebase/indexes/modules.csv`
6. `.codebase/indexes/files.csv`
7. `.codebase/indexes/classes.csv`
8. `.codebase/indexes/symbols.csv`
9. `.codebase/indexes/dependencies.csv`
10. `.codebase/indexes/flows.csv`
11. 必要な実コード

`.codebase/` の一部が存在しない場合は、存在するファイルだけを地図として使い、不足している情報は実コードを読んで補う。

## CSVの使い方

### modules.csv

対象領域のモジュールを絞るために使う。

見る列:

- `module`
- `path`
- `responsibility`
- `importance`
- `main_files`

### files.csv

対象ファイルを探すために使う。

見る列:

- `path`
- `module`
- `type`
- `responsibility`
- `importance`
- `depends_on`

### classes.csv

関連するクラス・型を探すために使う。

見る列:

- `class`
- `file`
- `module`
- `responsibility`
- `key_methods`
- `dependencies`
- `importance`

### symbols.csv

関数・定数・exportを探すために使う。

見る列:

- `symbol`
- `kind`
- `file`
- `module`
- `description`
- `exported`
- `importance`

### dependencies.csv

依存元・依存先を追うために使う。

見る列:

- `source`
- `target`
- `dependency_type`
- `description`
- `confidence`

### flows.csv

作業対象の処理フローを探すために使う。

見る列:

- `flow`
- `summary`
- `entrypoint`
- `main_modules`
- `importance`
- `related_files`

## 調査ルール

- `.codebase/` は地図として使う
- 最終判断は必ず実コードで確認する
- `.codebase/` と実コードが矛盾する場合は実コードを正とする
- `.codebase/` の情報が古い可能性を前提に、重要な判断は実ファイルの現在状態で検証する
- 最初から全ファイルを読まない
- 重要度 `high` のファイルから優先して読む
- 作業対象に関係ない `low` のファイルは後回しにする
- 不明点は推測で断定しない

## 作業手順

1. ユーザーの依頼内容から対象領域を推定する
2. `.codebase/README.md` で全体像を把握する
3. `.codebase/flows.md` または `flows.csv` で関連フローを探す
4. `.codebase/modules/` または `modules.csv` で関連モジュールを確認する
5. `files.csv`、`classes.csv`、`symbols.csv` で読むべき実コードを絞る
6. `dependencies.csv` で依存先・呼び出し元を確認する
7. 重要度 `high` の関連ファイルから実コードを読む
8. 必要なら依存先・呼び出し元を追加で読む
9. 実コードを根拠に回答する

## 回答ルール

回答には必要に応じて以下を含める。

- 読んだ `.codebase` ファイル
- 確認した実コード
- 関連するクラス・関数
- 修正候補ファイル
- `.codebase/` と実コードの差分
- 未確認事項

## 完了条件

以下を満たしたら完了。

- 作業対象に関係するファイルが特定できている
- 必要な実コードを確認している
- 回答が `.codebase/` だけに依存していない
- 不明点や未確認事項が明記されている
