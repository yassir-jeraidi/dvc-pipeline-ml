#!/usr/bin/env python3
"""
Script to deploy the best model based on evaluation metrics.
Compares current model accuracy with the best known accuracy
and promotes the model to production if it performs better.
"""

import json
import shutil
import os
from pathlib import Path


def load_json(filepath):
    """
    Load JSON file and return its content.
    Returns None if file doesn't exist or is invalid.
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Info: Could not load {filepath}: {e}")
        return None


def save_json(data, filepath):
    """Save data to JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"✅ Saved: {filepath}")


def deploy_model():
    """
    Main deployment logic:
    1. Load current evaluation metrics
    2. Load best known metrics
    3. Compare accuracies
    4. Deploy if current is better
    """
    
    # Define paths
    eval_metrics_path = "metrics/eval_metrics.json"
    best_metrics_path = "metrics/best_metrics.json"
    current_model_path = "models/random_forest.pkl"
    production_model_path = "models/production_model.pkl"
    
    # Load current evaluation metrics
    eval_metrics = load_json(eval_metrics_path)
    if not eval_metrics:
        print("❌ Error: Could not load evaluation metrics")
        return
    
    # Get current accuracy
    current_accuracy = eval_metrics.get('accuracy_full_data', 0.0)
    print(f"📊 Current model accuracy: {current_accuracy:.4f}")
    
    # Load best known metrics
    best_metrics = load_json(best_metrics_path)
    
    # Initialize best accuracy
    if best_metrics:
        best_accuracy = best_metrics.get('best_accuracy', 0.0)
        print(f"🏆 Best known accuracy: {best_accuracy:.4f}")
    else:
        # First run - no previous best
        best_accuracy = 0.0
        print("ℹ️  No previous best model found - this will be the first production model")
    
    # Compare and deploy if better
    if current_accuracy > best_accuracy:
        print(f"\n🎉 New best model! Accuracy improved from {best_accuracy:.4f} to {current_accuracy:.4f}")
        print(f"📦 Deploying model to production...")
        
        # Copy current model to production
        shutil.copy2(current_model_path, production_model_path)
        print(f"✅ Model deployed: {current_model_path} -> {production_model_path}")
        
        # Update best metrics
        best_metrics = {
            "best_accuracy": current_accuracy,
            "deployed_from": eval_metrics_path,
            "full_metrics": eval_metrics
        }
        save_json(best_metrics, best_metrics_path)
        
        print(f"\n✨ Deployment completed successfully!")
        print(f"   - Production model: {production_model_path}")
        print(f"   - Best metrics updated: {best_metrics_path}")
        
    elif current_accuracy == best_accuracy:
        print(f"\n➡️  Current accuracy equals best accuracy ({current_accuracy:.4f})")
        print(f"   No deployment needed - keeping existing production model")
        
    else:
        print(f"\n⚠️  Current accuracy ({current_accuracy:.4f}) is lower than best ({best_accuracy:.4f})")
        print(f"   No deployment - production model unchanged")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"DEPLOYMENT SUMMARY")
    print(f"{'='*60}")
    print(f"Current Accuracy:     {current_accuracy:.4f}")
    print(f"Best Accuracy:        {best_accuracy:.4f}")
    print(f"Production Model:     {'UPDATED ✅' if current_accuracy > best_accuracy else 'UNCHANGED'}")
    print(f"{'='*60}")


if __name__ == "__main__":
    print("🚀 Starting model deployment process...\n")
    deploy_model()
