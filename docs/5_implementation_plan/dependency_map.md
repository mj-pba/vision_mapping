# Task Dependency Map: PBA Vision Mapping

## Visual Dependency Graph

```mermaid
graph LR
    T1["ITB-TASK-001<br/>Dot Grid Scanning<br/>✅ Done"] --> T2["ITB-TASK-002<br/>UI for Scan Input<br/>✅ Done"]
    T1 --> T3["ITB-TASK-003<br/>Glass Certificate<br/>✅ Done"]
    T3 --> T4["ITB-TASK-004<br/>Error Matrix<br/>✅ Done"]
    T4 --> T5["ITB-TASK-005<br/>Correction Test<br/>✅ Done"]
    T4 --> T6["ITB-TASK-006<br/>Error Map Viz<br/>✅ Done"]
    T6 --> T7["ITB-TASK-007<br/>Y-Data Refactor<br/>✅ Done"]

    T1 --> T8["ITB-TASK-008<br/>Full UI Integration<br/>🔄 To Do"]
    T3 --> T8
    T4 --> T8
    T5 --> T8
    T6 --> T8
    T7 --> T8

    T2 --> T9["ITB-TASK-009<br/>UI Progress Feedback<br/>🔄 To Do"]
    T8 --> T9

    T8 --> T10["ITB-TASK-010<br/>Document & Test All<br/>📋 To Do"]
    T9 --> T10

    classDef done fill:#1a7f37,stroke:#fff,color:#fff;
    classDef todo fill:#d29922,stroke:#fff,color:#fff;
    class T1,T2,T3,T4,T5,T6,T7 done;
    class T8,T9,T10 todo;
```

## Dependency List

- ITB-TASK-002 depends on ITB-TASK-001
- ITB-TASK-003 depends on ITB-TASK-001
- ITB-TASK-004 depends on ITB-TASK-003
- ITB-TASK-005 depends on ITB-TASK-004
- ITB-TASK-006 depends on ITB-TASK-004
- ITB-TASK-007 depends on ITB-TASK-006
- ITB-TASK-008 depends on ITB-TASK-001, ITB-TASK-003, ITB-TASK-004, ITB-TASK-005, ITB-TASK-006, ITB-TASK-007
- ITB-TASK-009 depends on ITB-TASK-002, ITB-TASK-008
- ITB-TASK-010 depends on all previous tasks

*See `task_backlog.md` for task details.*

---

## Related Links

- [Implementation Plan](./implementation_plan.md)
- [Task Backlog](./task_backlog.md)
- [Main Project README](../../README.md)
