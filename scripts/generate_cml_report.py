#!/usr/bin/env python3
"""
Script to generate a CML report from metrics files.
Reads train and evaluation metrics and creates a Markdown report.
"""

import json
import os
from pathlib import Path


def load_json(filepath):
    """Load JSON file and return its content."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {filepath} not found")
        return None
    except json.JSONDecodeError:
        print(f"Warning: {filepath} is not valid JSON")
        return None


def generate_report():
    """Generate CML report from metrics files."""
    
    # Paths to metrics files
    train_metrics_path = "metrics/train_metrics.json"
    eval_metrics_path = "metrics/eval_metrics.json"
    report_path = "reports/cml_report.md"
    
    # Load metrics
    train_metrics = load_json(train_metrics_path)
    eval_metrics = load_json(eval_metrics_path)
    
    # Build markdown report
    markdown_lines = []
    
    # Header
    markdown_lines.append("# 🤖 ML Pipeline Report\n")
    markdown_lines.append("## 📊 Model Performance Metrics\n")
    
    # Training metrics
    if train_metrics:
        markdown_lines.append("### Training Metrics\n")
        markdown_lines.append("| Metric | Value |")
        markdown_lines.append("|--------|-------|")
        
        for key, value in train_metrics.items():
            if isinstance(value, float):
                markdown_lines.append(f"| {key} | {value:.4f} |")
            else:
                markdown_lines.append(f"| {key} | {value} |")
        
        markdown_lines.append("\n")
    
    # Evaluation metrics
    if eval_metrics:
        markdown_lines.append("### Evaluation Metrics\n")
        markdown_lines.append("| Metric | Value |")
        markdown_lines.append("|--------|-------|")
        
        # Display main accuracy
        if 'accuracy_full_data' in eval_metrics:
            acc = eval_metrics['accuracy_full_data']
            markdown_lines.append(f"| Accuracy (Full Data) | {acc:.4f} |")
        
        markdown_lines.append("\n")
        
        # Display classification report if available
        if 'classification_report' in eval_metrics:
            markdown_lines.append("### Classification Report\n")
            markdown_lines.append("```")
            markdown_lines.append(eval_metrics['classification_report'])
            markdown_lines.append("```\n")
    
    # Add model configuration section
    markdown_lines.append("### Model Configuration\n")
    if train_metrics:
        markdown_lines.append("| Parameter | Value |")
        markdown_lines.append("|-----------|-------|")
        
        config_keys = ['n_estimators', 'max_depth', 'test_size', 'random_state']
        for key in config_keys:
            if key in train_metrics:
                markdown_lines.append(f"| {key} | {train_metrics[key]} |")
        
        markdown_lines.append("\n")
    
    # Add summary
    markdown_lines.append("---\n")
    markdown_lines.append("*Report generated automatically by CML*\n")
    
    # Write report to file
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as f:
        f.write('\n'.join(markdown_lines))
    
    print(f"✅ CML report generated successfully: {report_path}")
    
    # Also print to console for GitHub Actions
    print("\n" + "\n".join(markdown_lines))


if __name__ == "__main__":
    generate_report()
