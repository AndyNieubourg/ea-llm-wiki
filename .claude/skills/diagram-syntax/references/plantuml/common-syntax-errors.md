<!-- Adapted from tractorjuice/arc-kit, plugins/arckit-claude/skills/plantuml-syntax (MIT); ArcKit adapted it from SpillwaveSolutions/plantuml. -->

# PlantUML Common Syntax Errors Reference

A catalogue of frequently encountered PlantUML syntax errors, their causes, and fixes. Organised by diagram type.

> **Renderer this file was checked against.** `java -jar wiki/.obsidian/plantuml/plantuml.jar -version` reports:
>
> ```
> PlantUML version 1.2026.5 / e0f0ce5 [2026-05-27 17:39:27 UTC]
> Build Version: 1.2026.5
> Git Commit: e0f0ce5
> GraphViz: dot - graphviz version 15.0.0 (20260523.1842)
> Installation seems OK. File generation OK
> PLANTUML_LIMIT_SIZE: 4096
> ```
>
> Everything below marked "moot at 1.2026.5" was tested against that JAR, not inferred from changelogs.

---

## Universal Errors (All Diagram Types)

| Error | Cause | Fix |
|-------|-------|-----|
| No diagram rendered | Missing `@startuml` / `@enduml` | Always wrap code in `@startuml` and `@enduml` |
| "Syntax Error?" message | Invalid character in diagram body | Check for unescaped special characters: `{`, `}`, `<`, `>` in labels |
| Blank output | Empty diagram body or only comments | Ensure at least one element is declared between `@startuml` and `@enduml` |
| "Cannot find skin" | Invalid skinparam name | Check spelling of skinparam names (case-sensitive) |
| Encoding issues | Non-ASCII characters in source | Use UTF-8 encoding; avoid copy-pasted curly quotes, use straight quotes |
| Unexpected layout | Too many elements without layout hints | Add directional arrows (`-down->`, `-right->`) or `Lay_*` constraints |
| "File not found" on `!include` | Wrong path, or a remote URL that cannot be reached | Prefer the local stdlib form (`!include <C4/C4_Container>`), which never touches the network |

## C4-PlantUML Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Unknown function Person" | Missing or wrong `!include` | Include the local C4 stdlib: `!include <C4/C4_Context>` (or `<C4/C4_Container>`, `<C4/C4_Component>`, `<C4/C4_Deployment>`, `<C4/C4_Dynamic>`) |
| Whole diagram is an error box, source looks fine | Remote `!include https://raw.githubusercontent.com/...` blocked by firewall or offline | Switch to the local stdlib include. See `c4-plantuml.md` section 1 |
| Elements overlap | Conflicting `Lay_*` and `Rel_*` directions | Make every `Rel_*` direction consistent with the `Lay_*` constraint on the same pair. See the layout conflict rules, Rules 1 to 3 |
| Random element placement | Using generic `Rel` without direction hints | Replace `Rel(a, b, ...)` with `Rel_Down(a, b, ...)` or `Rel_Right(a, b, ...)` |
| Boundary renders empty | No elements inside the boundary block | Put at least one element inside every `System_Boundary` or `Container_Boundary` |
| "Syntax error: )" on an element macro | Almost never a parameter *count* problem | Trailing parameters are optional: `Container(c2, "Two args")` renders. Look for an unescaped comma or unbalanced quote inside a label, or a stray `)`. See `c4-plantuml.md` section 2 |
| Invisible relationships | `Lay_*` used where `Rel_*` was intended | `Lay_Right`, `Lay_Down` draw nothing. Use `Rel_Right`, `Rel_Down` for visible arrows |

## Sequence Diagram Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Missing participant | Participant referenced but not declared | Declare all participants before the first message |
| "Unknown arrow" | Invalid arrow syntax | Use `->` (solid), `-->` (dashed), `->>` (async), `-->>` (async dashed) |
| Misaligned activation | `activate`/`deactivate` mismatch | Match every `activate` with a `deactivate`, or use the `++`/`--` shorthand |
| "alt" without "end" | Missing closing `end` for a grouping block | Close every `alt`, `opt`, `loop`, `par`, `group` with `end` |
| Overlapping boxes | Box declarations conflict | Keep `box` groupings disjoint; each participant belongs to at most one box |

## Class Diagram Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Relationship direction wrong | Arrow drawn in an unexpected direction | Use `-up-\|>`, `-down-\|>`, `-left-\|>`, `-right-\|>` for explicit direction |
| Duplicate class | Same class name declared twice | Use aliases: `class "Name" as alias1` |
| "Cannot find class" | Referencing an undeclared class in a relationship | Declare all classes before defining relationships |
| Visibility icons missing | `skinparam classAttributeIconSize 0` is set | Remove or adjust this skinparam |

## Activity Diagram Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Unexpected token" | Missing `;` at the end of an activity | Activities end with `;`: `:Do something;` |
| Infinite loop in render | Unclosed `while` or `repeat` | Every `while` needs `endwhile`, every `repeat` needs `repeat while` |
| Missing swimlane content | Empty swimlane partition | Add at least one activity in each swimlane |
| "if" without "endif" | Missing closing `endif` | Close every `if` block with `endif` |

## State Diagram Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Cannot parse" | Activity diagram syntax used in a state diagram | State transitions use `-->` between state names, not `:activity;` syntax |
| Missing final state | No path to the `[*]` end state | At least one state transitions to `[*]` |
| Nested state rendering issues | Too many nesting levels | Keep nesting to 2 or 3 levels; split complex state machines across diagrams |

## ER Diagram Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Relationship lines missing | Wrong cardinality syntax | Use the `\|\|--o{` notation (pipe, pipe, dash, dash, o, curly brace) |
| Entity renders as class | Using `class` instead of `entity` | Use `entity "Name" as alias` |
| Attributes not showing | Missing attribute block format | Use `entity Name { * field : type }`, with `*` marking mandatory fields |

## Component Diagram Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Component renders as class | Wrong syntax | Use `component [Name]` or `component "Name" as alias` |
| Interface not connecting | Wrong interface syntax | Provided: `-()` (lollipop); required: `-(` (socket) |
| Package overlap | Nested packages sharing a name | Give every package a unique name or alias |

## Version-Specific Issues

Checked against the bundled JAR at v1.2026.5. The first two rows are inherited from upstream documentation written for much older releases and no longer apply here. They are kept because pasted snippets and Stack Overflow answers still repeat them.

| PlantUML Version | Issue | Status at 1.2026.5 |
|-----------------|-------|--------------------|
| < 1.2023.1 | C4-PlantUML `!include` of a URL may fail; upstream advice was to use `!includeurl` | **Moot.** Irrelevant twice over: this wiki uses the local `!include <C4/...>` stdlib form, which never resolves a URL. `!includeurl` is still parsed by the JAR (it fails on a missing target, not on an unknown directive), so a legacy snippet will not break, but there is no reason to write it |
| < 1.2022.0 | `ContainerQueue` not available; workaround was `Container` with a `<<queue>>` stereotype | **Moot.** Verified: `ContainerQueue`, `ContainerQueue_Ext` and `SystemQueue` all render from `<C4/C4_Container>` on this JAR. `ComponentQueue` needs `<C4/C4_Component>`; calling it under a Container-level include is a genuine error, not a version gap |
| All versions | Large diagrams (more than about 50 elements) hit the image size cap and render truncated or blank | **Still applies.** The cap is `PLANTUML_LIMIT_SIZE`, which defaults to 4096 pixels per side on this JAR. It is a **dimension limit, not a timeout**: upstream text calling it a timeout is wrong. Raise it with `-DPLANTUML_LIMIT_SIZE=8192`, which PlantUML reads from its own argument list, so either position works: `java -DPLANTUML_LIMIT_SIZE=8192 -jar plantuml.jar -tpng diagram.puml` and `java -jar plantuml.jar -tpng diagram.puml -DPLANTUML_LIMIT_SIZE=8192` are equivalent. Verified on a 40-node `left to right` chain: the default run capped the PNG at 4096 px wide, and both flag positions produced the same 10408 px width. Splitting the diagram is usually the better fix |
| All versions | Remote `!include` blocked by firewall | **Still applies to anything using the URL form.** Neutralised here by the local stdlib include. If a diagram genuinely needs a non-stdlib remote file, vendor it locally and `!include` the path |

Two further capabilities were checked on this JAR because the debugging tips below depend on them: `!pragma layout smetana` renders, and `!theme cerulean` renders.

## Debugging Tips

1. **Start minimal.** Begin with 2 or 3 elements and add incrementally.
2. **Render locally, do not eyeball.** `java -jar wiki/.obsidian/plantuml/plantuml.jar -tpng /tmp/diagram.puml`, then open the PNG. A malformed block only shows as an error box at view time, and a text diff never catches it.
3. **Read the error message.** PlantUML reports the offending line number, and it is usually right.
4. **Comment out sections.** Use the `' comment` syntax to isolate the problem.
5. **Check `!include` targets.** For the stdlib form, confirm the package exists in the JAR: `unzip -l plantuml.jar | grep stdlib/c4`.
6. **Try `!pragma layout smetana`.** An alternative layout engine bundled in the JAR, no GraphViz needed. It sometimes untangles a diagram GraphViz lays out badly.
7. **Confirm the toolchain first.** `java -jar plantuml.jar -version` ends with `Installation seems OK. File generation OK` and reports the GraphViz version. If GraphViz is missing, every non-sequence diagram fails for a reason that has nothing to do with your syntax.
