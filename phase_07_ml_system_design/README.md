# Phase 7: ML Fundamentals & System Design (Days 69-71)

Many AI Engineer loops still include one classic-ML round. v2 keeps it short and gives it a security
flavour, since anomaly and fraud detection is where classic ML and security meet.

> **v1 reference:** [../archive/v1/phase_03_system_design_ml/](../archive/v1/phase_03_system_design_ml/) for the fuller 5-day version.

## Days

- **Day 69: Classic ML crash course.** Bias-variance, L1/L2, bagging/boosting, precision/recall/F1/ROC-AUC/PR-AUC,
  calibration, class imbalance. *Build:* Isolation Forest anomaly detection on your Phase 1 gateway auth logs.
- **Day 70: DL refresher + ML system design.** Backprop, Adam, layer norm, overfitting controls. Then the ML design
  framework (data → features → training → serving → monitoring → feedback) applied to **fraud/abuse detection for
  an agent marketplace** (adversarial drift, label delay, cost of false positives).
- **Day 71: 🎯🎯 Two timed mocks.** (1) a GenAI-security prompt, e.g. *"Design prompt-injection defense for an email
  assistant with send permissions"*. (2) a marketplace prompt, e.g. *"Design the vetting pipeline for a public MCP
  registry"*. Write both up in [../system_design/](../system_design/README.md).

## Resources

- [Chip Huyen: Designing ML Systems notes](https://huyenchip.com/machine-learning-systems-design/toc.html)
- [Google ML Crash Course](https://developers.google.com/machine-learning/crash-course)
